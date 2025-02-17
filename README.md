# real-time-stock-app

## Program Intent

The **real-time-stock-app** allows users to track top stock gainers and losers from the S&P 500, retrieve historical stock data, and view trends. This tool helps users monitor market changes by displaying the top 20 Large Market Cap S&P 500 stock symbols with their current price movements and percentage changes over time. Users can specify the time period for the stock data and dynamically update the top gainers and losers based on real-time data. Additionally, users can input a single stock symbol to fetch detailed data on that specific stock.

## Features
- Uses yfinance for free stock integration.
- Display the top 20 Large Market Cap S&P 500 stocks for the selected time period.
- View of top gainers and top losers, based on percentage change.
- Historical stock data retrieval (current price, high, low, volume).
- Customizable time periods via slider (1d, 3d, 10d, 30d, etc.).
- Responsive interface with real-time updates.
- Light and Dark mode preferences.
- Option to input a single stock symbol to view its data.

## Prerequisites

To run this program, you need the following:
- Python 3.x
- `pip` (Python package installer)
- Virtual environment (optional, but recommended)

## Setup Instructions

Follow these steps to set up the program on your local machine:

### 1. Clone the Repository

Open a terminal or Command Prompt and clone the repository using `git`:
```bash
git clone https://github.com/RlleyC/real-time-stock-app.git
```
### 2. Create and Activate a Virtual Environment
## Navigate to the project directory:
```bash
cd real-time-stock-app
```
## Create a virtual environment:
```bash
python -m venv venv
```
## Activate the virtual environment:
#### Windows CMD
```bash
venv\Scripts\activate
```
#### Windows (Git Bash)
```bash
source venv/Scripts/activate
```
#### macOS/Linux
```bash
source venv/bin/activate
```
## Navigate to the backend directory
```bash
cd backend
```
## Install Dependencies
```bash
pip install -r requirements.txt
```
## Run the Program
```bash
python app.py
```
# Demo Screenshots
![MarketCheckLight](https://github.com/user-attachments/assets/fc2a7b8b-d571-492d-af19-a43eaad01928)
![MarketCheckDark](https://github.com/user-attachments/assets/0751e5bc-bde9-453c-90c9-be8dcc777da0)
![MarketCheckDarkLoad](https://github.com/user-attachments/assets/9389327a-4ecb-403a-9200-7f75aefe4ae5)
## Quit Virtual Environment
```bash
Ctrl + C or deactivate
```
