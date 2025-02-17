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
        logging.debug(f"Fetching stock data for symbol: {symbol}")
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        
        if data.empty:
            logging.error(f"No data found for symbol: {symbol}")
            return jsonify({'error': 'Stock data not available'}), 404
        
        logging.debug(f"Received data: {data.head()}")  # Log the first few rows of data for inspection
        logging.debug(f"Index type: {type(data.index)}")  # Log the type of the index

        # Check if the index is a DatetimeIndex
        if isinstance(data.index, pd.DatetimeIndex):
            logging.debug("Index is a DatetimeIndex.")
            # Handle timezone conversion
            if data.index.tz is None:  # If the datetime index is naive (without timezone)
                logging.debug("Index is naive, localizing to UTC.")
                data.index = data.index.tz_localize('UTC')  # Set to UTC if naive
            else:  # If the datetime index already has a timezone
                logging.debug("Index is timezone-aware, converting to UTC.")
                data.index = data.index.tz_convert('UTC')  # Convert it to UTC if aware
        else:
            logging.error(f"Unexpected index type: {type(data.index)}. Expected DatetimeIndex.")
            return jsonify({'error': 'Unexpected index type, expected DatetimeIndex'}), 500

        # Reset the index so that the datetime is treated as a regular column
        data_reset = data.reset_index()
        logging.debug(f"Data after reset_index: {data_reset.head()}")

        # Convert data to native Python types to avoid serialization issues
        stock_info = {
            'symbol': symbol,
            'price': float(data['Close'][-1]),  # Convert to float
            'high': float(data['High'][-1]),    # Convert to float
            'low': float(data['Low'][-1]),      # Convert to float
            'volume': int(data['Volume'][-1])   # Convert to int
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
        stock_data = {}
        
        for symbol in symbols:
            stock = yf.Ticker(symbol)
            data = stock.history(period="1d")
            
            if data.empty:
                stock_data[symbol] = {'error': 'Data not available'}
                continue
            
            # Convert data to native Python types to avoid serialization issues
            stock_data[symbol] = {
                'price': f"${round(data['Close'][-1], 4):,.4f}",  # Round to 4 decimals and add commas
                'high': f"${round(data['High'][-1], 4):,.4f}",    # Round to 4 decimals and add commas
                'low': f"${round(data['Low'][-1], 4):,.4f}",      # Round to 4 decimals and add commas
                'volume': f"{int(data['Volume'][-1]):,}"  # Add commas to volume
            }

            # Debugging output
            print(f"Price: {data['Close'][-1]}")
            print(f"High: {data['High'][-1]}")
            print(f"Low: {data['Low'][-1]}")
            print(f"Volume: {data['Volume'][-1]}")
        
        return jsonify(stock_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
