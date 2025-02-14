from flask import Flask, jsonify, render_template, request
import yfinance as yf

app = Flask(__name__)

# Basic route to serve the frontend
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to fetch stock data from Yahoo Finance
@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    try:
        # Fetch stock data from Yahoo Finance using yfinance
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        
        # Handle cases where no data is available
        if data.empty:
            return jsonify({'error': 'Stock data not available'}), 404
        
        stock_info = {
            'symbol': symbol,
            'price': data['Close'][-1],  # Get the latest closing price
            'high': data['High'][-1],    # Latest high price
            'low': data['Low'][-1],      # Latest low price
            'volume': data['Volume'][-1] # Latest trading volume
        }
        return jsonify(stock_info)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to compare multiple stocks
@app.route('/api/compare', methods=['GET'])
def compare_stocks():
    try:
        symbols = request.args.get('symbols').split(',')
        stock_data = {}
        
        for symbol in symbols:
            stock = yf.Ticker(symbol)
            data = stock.history(period="1d")
            
            # Handle cases where no data is available
            if data.empty:
                stock_data[symbol] = {'error': 'Data not available'}
                continue
            
            stock_data[symbol] = {
                'price': data['Close'][-1],
                'high': data['High'][-1],
                'low': data['Low'][-1],
                'volume': data['Volume'][-1]
            }
        
        return jsonify(stock_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
