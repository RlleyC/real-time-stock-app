// app.js

// Function to fetch stock data from the backend
function fetchStockData() {
    const stockSymbol = document.getElementById('stockSymbol').value;

    // Ensure the user has entered a stock symbol
    if (!stockSymbol) {
        alert("Please enter a stock symbol.");
        return;
    }

    // Make the GET request to the Flask API endpoint to get stock data
    fetch(`/api/stock/${stockSymbol}`)
        .then(response => response.json())
        .then(data => {
            // If there's an error (like no data for the stock symbol), show the error
            if (data.error) {
                document.getElementById('result').innerHTML = `<p class="error">${data.error}</p>`;
            } else {
                // Display the stock data if available
                document.getElementById('result').innerHTML = `
                    <h2>Stock Data for ${data.symbol}</h2>
                    <p><strong>Price:</strong> $${data.price}</p>
                    <p><strong>High:</strong> $${data.high}</p>
                    <p><strong>Low:</strong> $${data.low}</p>
                    <p><strong>Volume:</strong> ${data.volume}</p>
                `;
            }
        })
        .catch(error => {
            // Handle any network or other errors
            document.getElementById('result').innerHTML = `<p class="error">Error fetching stock data. Please try again later.</p>`;
            console.error("Error:", error);
        });
}
