from flask import Flask, jsonify, render_template
import yfinance as yf

app = Flask(__name__)

# Basic route to serve the frontend
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to fetch stock data from Yahoo Finance
@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    # Fetch stock data from Yahoo Finance using yfinance
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d")  # Fetch daily data
    stock_info = {
        'symbol': symbol,
        'price': data['Close'][-1],  # Get the latest closing price
        'high': data['High'][-1],    # Latest high price
        'low': data['Low'][-1],      # Latest low price
        'volume': data['Volume'][-1] # Latest trading volume
    }
    return jsonify(stock_info)

# Endpoint to compare multiple stocks
@app.route('/api/compare', methods=['GET'])
def compare_stocks():
    symbols = request.args.get('symbols').split(',')
    stock_data = {}
    
    for symbol in symbols:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        stock_data[symbol] = {
            'price': data['Close'][-1],
            'high': data['High'][-1],
            'low': data['Low'][-1],
            'volume': data['Volume'][-1]
        }
    
    return jsonify(stock_data)

if __name__ == "__main__":
    app.run(debug=True)
