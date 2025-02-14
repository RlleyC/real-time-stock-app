from flask import Flask, jsonify, request, send_from_directory
import yfinance as yf
import os

app = Flask(__name__, static_folder='public', template_folder='templates')

# Serve the index.html from the public folder
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# API endpoint to fetch stock data from Yahoo Finance
@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        
        if data.empty:
            return jsonify({'error': 'Stock data not available'}), 404
        
        stock_info = {
            'symbol': symbol,
            'price': data['Close'][-1],
            'high': data['High'][-1],
            'low': data['Low'][-1],
            'volume': data['Volume'][-1]
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
    app.run(debug=True, host="127.0.0.1", port=5000)
