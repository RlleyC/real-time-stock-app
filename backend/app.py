from flask import Flask, jsonify, request, render_template
import yfinance as yf
import logging
import pandas as pd

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, static_folder='static', template_folder='templates')

# Serve the index.html from the templates folder
@app.route('/')
def serve_index():
    return render_template('index.html')  # Render the HTML file from the templates folder

# API endpoint to fetch stock data from Yahoo Finance
@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    try:
        # Get the period from the query parameters (default is "1d")
        period = request.args.get('period', default='1d', type=str)
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
        period = request.args.get('period', default='1d', type=str)  # Get period for comparison
        
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

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
