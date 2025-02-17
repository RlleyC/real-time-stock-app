// Function to fetch stock data from the backend
function fetchStockData() {
    const stockSymbol = document.getElementById('stockSymbol').value.trim().toUpperCase();
    const timePeriodSlider = document.getElementById('timePeriodSlider');
    const timePeriodValue = timePeriodSlider.value;

    // Ensure the user has entered a stock symbol
    if (!stockSymbol) {
        alert("Please enter a stock symbol.");
        return;
    }

    // Map slider value to actual time period (1d, 3d, 10d, etc.)
    const timePeriods = ['1d', '3d', '10d', '30d', '60d', '90d', '1y'];
    const selectedPeriod = timePeriods[timePeriodValue - 1]; // Adjust index to match the slider
    console.log(`/api/stock/${stockSymbol}?period=${selectedPeriod}`);  // Log the request URL

    // Make the GET request to the Flask API endpoint to get stock data
    fetch(`/api/stock/${stockSymbol}?period=${selectedPeriod}`)
        .then(response => response.json())
        .then(data => {
            // If there's an error (like no data for the stock symbol), show the error
            if (data.error) {
                document.getElementById('result').innerHTML = `<p class="error">${data.error}</p>`;
            } else {
                // Display the stock data if available
                document.getElementById('result').innerHTML = `
                    <h2>Stock Data for ${data.symbol} (${selectedPeriod})</h2>
                    <p><strong>Current Price:</strong> $${data.price}</p>
                    <p><strong>Period High:</strong> $${data.high}</p>
                    <p><strong>Period Low:</strong> $${data.low}</p>
                    <p><strong>Volume:</strong> ${data.volume}</p>
                `;
            }
            // Show the result div
            document.getElementById('result').style.display = 'block';
        })
        .catch(error => {
            // Handle any network or other errors
            document.getElementById('result').innerHTML = `<p class="error">Error fetching stock data. Please try again later.</p>`;
            console.error("Error:", error);
        });
}

// Debounce function to limit the rate at which the `fetchStockData` is called
let debounceTimeout;
function debounceFetchStockData() {
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(fetchStockData, 500); // 500ms delay after the user stops sliding
}

// Update function to adjust period on slider change
document.getElementById('timePeriodSlider').addEventListener('input', debounceFetchStockData);

// Function to toggle light/dark mode
function toggleMode() {
    const darkMode = document.body.classList.toggle('dark-mode');
    
    // Save the current theme to localStorage
    localStorage.setItem('theme', darkMode ? 'dark' : 'light');
}

// Check the stored theme on page load and apply it
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.remove('dark-mode');
    }
});
