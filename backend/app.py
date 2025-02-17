from flask import Flask, jsonify, request, render_template
import yfinance as yf
import logging
import pandas as pd
from bs4 import BeautifulSoup
import requests

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, static_folder='static', template_folder='templates')

# Serve the index.html from the templates folder
@app.route('/')
def serve_index():
    return render_template('index.html')  # Render the HTML file from the templates folder

# Function to get the top 20 S&P 500 tickers dynamically from Wikipedia
def get_top_20_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', {'class': 'wikitable'})
    if not table:
        print("Could not find the table.")
        return []

    tickers = []
    rows = table.find_all('tr')[1:21]  # Fetch top 20 rows (skip the header row)
    if not rows:
        print("No rows found in the table.")
        return []

    for row in rows:
        columns = row.find_all('td')
        if columns:
            ticker = columns[0].text.strip()  # Ticker is usually in the first column
            tickers.append(ticker)

    return tickers

# API endpoint to fetch stock data from Yahoo Finance
@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    try:
        # Get the period from the query parameters (default is "1d")
        period = request.args.get('period', default='30d', type=str)
        logging.debug(f"Fetching stock data for symbol: {symbol} with period: {period}")
        
        stock = yf.Ticker(symbol)
        data = stock.history(period=period)
        
        if data.empty:
            logging.error(f"No data found for symbol: {symbol}")
            return jsonify({'error': 'Stock data not available'}), 404
        
        logging.debug(f"Received data: {data.head()}")  # Log the first few rows of data for inspection

        # Reset the index so that the datetime is treated as a regular column
        data_reset = data.reset_index()

        # Find the highest and lowest values for the period
        period_high = round(data['High'].max(), 2)
        period_low = round(data['Low'].min(), 2)

        # Sum up the volume over the selected period
        total_volume = data['Volume'].sum()

        # Prepare the stock information
        stock_info = {
            'symbol': symbol,
            'price': f"{round(float(data['Close'][-1]), 2):,.2f}",
            'high': f"{period_high:,.2f}",  # Maximum High for the period
            'low': f"{period_low:,.2f}",    # Minimum Low for the period
            'volume': f"{total_volume:,}"  # Total volume over the period
        }
        logging.debug(f"Stock info: {stock_info}")
        return jsonify(stock_info)
    
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

# Endpoint to compare multiple stocks
@app.route('/api/compare', methods=['GET'])
def compare_stocks():
    try:
        symbols = request.args.get('symbols').split(',')
        period = request.args.get('period', default='30d', type=str)  # Get period for comparison
        
        stock_data = {}
        
        for symbol in symbols:
            stock = yf.Ticker(symbol)
            data = stock.history(period=period)
            
            if data.empty:
                stock_data[symbol] = {'error': 'Data not available'}
                continue
            
            # Convert data to native Python types to avoid serialization issues
            stock_data[symbol] = {
                'price': f"{round(float(data['Close'][-1]), 2):,.2f}",
                'high': f"{round(float(data['High'][-1]), 2):,.2f}",
                'low': f"{round(float(data['Low'][-1]), 2):,.2f}",
                'volume': f"{int(data['Volume'][-1]):,}"
            }
        
        return jsonify(stock_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to fetch top gainers and losers
@app.route('/api/top-gainers-losers')
def top_gainers_losers():
    # Get the period from the query parameters (default is "1d")
    period = request.args.get('period', default='30d', type=str)
    
    gainers = []
    losers = []

    # Create a DataFrame to hold stock data
    stock_data = []

    # Fetch stock data using yfinance for the top 20 tickers
    top_20_tickers = get_top_20_sp500_tickers()
    
    for ticker in top_20_tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)  # Use the dynamic period passed from the frontend

        # Ensure there is data available for the stock
        if hist.empty or len(hist) < 2:
            logging.warning(f"Not enough data for {ticker}")
            continue

        # Calculate the price change percentage (close price vs open price)
        price_change = (hist['Close'].iloc[-1] - hist['Open'].iloc[0]) / hist['Open'].iloc[0] * 100
        current_price = hist['Close'].iloc[-1]

        # Determine the color based on the price change
        if price_change > 0:
            color = 'green'  # Green for gain
        elif price_change < 0:
            color = 'red'  # Red for loss
        else:
            color = 'gray'  # Gray for no change

        stock_data.append({
            'symbol': ticker,
            'price_change': price_change,
            'price': current_price,
            'color': color
        })

    # Sort stocks into gainers and losers based on the price change
    sorted_stock_data = sorted(stock_data, key=lambda x: x['price_change'], reverse=True)

    # Separate the top gainers and losers
    for stock in sorted_stock_data:
        if stock['price_change'] > 0:
            gainers.append(stock)
        else:
            losers.append(stock)

    # Limit the results to top 5 gainers and losers for display
    top_gainers = gainers[:5]
    top_losers = losers[:5]

    return jsonify({'gainers': top_gainers, 'losers': top_losers})

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
