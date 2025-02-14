from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Basic route to serve the frontend
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to fetch stock data
@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    # Fetch stock data from an external API
    api_key = "YOUR_STOCK_API_KEY"
    response = requests.get(f'https://api.example.com/stock/{symbol}?apikey={api_key}')
    data = response.json()
    return jsonify(data)

# Endpoint to compare multiple stocks
@app.route('/api/compare', methods=['GET'])
def compare_stocks():
    symbols = request.args.get('symbols').split(',')
    prices = {}
    for symbol in symbols:
        response = requests.get(f'https://api.example.com/stock/{symbol}?apikey=YOUR_API_KEY')
        prices[symbol] = response.json()
    return jsonify(prices)

if __name__ == "__main__":
    app.run(debug=True)
