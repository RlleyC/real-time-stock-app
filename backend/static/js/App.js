// Function to show the loader in the respective result section
function showLoader(sectionId) {
    const loaderWrapper = document.querySelector(`#${sectionId} .loader-wrapper`);
    if (loaderWrapper) {
        loaderWrapper.style.display = 'flex'; // Show the loader
    }
    document.getElementById(sectionId).innerHTML = ''; // Clear previous content
}

// Function to hide the loader
function hideLoader(sectionId) {
    const loaderWrapper = document.querySelector(`#${sectionId} .loader-wrapper`);
    if (loaderWrapper) {
        loaderWrapper.style.display = 'none'; // Hide the loader
    }
}

// Function to fetch stock data from the backend
// Function to fetch stock data from the backend
function fetchStockData() {
    const stockSymbol = document.getElementById('stockSymbol').value.trim().toUpperCase();
    const timePeriodSlider = document.getElementById('timePeriodSlider');
    const timePeriodValue = timePeriodSlider.value;

    // Map slider value to actual time period (1d, 3d, 10d, etc.)
    const timePeriods = ['1d', '3d', '10d', '30d', '60d', '90d', '1y'];
    const selectedPeriod = timePeriods[timePeriodValue - 1]; // Adjust index to match the slider

    // If a stock symbol is entered, fetch stock data
    if (stockSymbol) {
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

    // Always update top gainers and losers with the new period, even without a stock symbol
    fetchTopGainersAndLosers(selectedPeriod);
}

// Debounce function to limit the rate at which the `fetchStockData` is called
let debounceTimeout;
function debounceFetchStockData() {
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(fetchStockData, 500); // 500ms delay after the user stops sliding
}

// Update function to adjust period on slider change
document.getElementById('timePeriodSlider').addEventListener('input', debounceFetchStockData);

// Function to fetch top gainers and losers from the backend
function fetchTopGainersAndLosers(selectedPeriod) {
    console.log('Fetching top gainers and losers...');
    
    // Show loaders for top gainers and top losers while fetching data
    document.getElementById('topGainers').innerHTML = '<div class="loader"></div>';
    document.getElementById('topLosers').innerHTML = '<div class="loader"></div>';

    // Fetch the top gainers and losers with the selected period
    fetch(`/api/top-gainers-losers?period=${selectedPeriod}`)
    .then(response => response.json())
    .then(data => {
        console.log('Top Gainers and Losers Data:', data);

        // Handle the top gainers
        if (data.gainers && data.gainers.length > 0) {
            let gainersHtml = '<ul>';
            data.gainers.forEach(stock => {
                const colorClass = stock.color === 'green' ? 'positive' : 'negative';
                gainersHtml += `
                    <li><strong>${stock.symbol}</strong>   <span class="${colorClass}">+${stock.price_change.toFixed(2)}%</span>   <span>$${stock.price.toFixed(2)}</span></li>
                `;
            });
            gainersHtml += '</ul>';
            document.getElementById('topGainers').innerHTML = gainersHtml;
        } else {
            document.getElementById('topGainers').innerHTML = '<p>No data available for timeperiod.</p>';
        }

        // Handle the top losers
        if (data.losers && data.losers.length > 0) {
            let losersHtml = '<ul>';
            data.losers.forEach(stock => {
                const colorClass = stock.color === 'green' ? 'positive' : 'negative';
                losersHtml += `
                    <li><strong>${stock.symbol}</strong>   <span class="${colorClass}">${stock.price_change.toFixed(2)}%</span>   <span>$${stock.price.toFixed(2)}</span></li>
                `;
            });
            losersHtml += '</ul>';
            document.getElementById('topLosers').innerHTML = losersHtml;
        } else {
            document.getElementById('topLosers').innerHTML = '<p>No data available for timeperiod.</p>';
        }
    })
    .catch(error => {
        console.error("Error fetching top gainers and losers:", error);
        document.getElementById('topGainers').innerHTML = '<p class="error">Error fetching top gainers. Please try again later.</p>';
        document.getElementById('topLosers').innerHTML = '<p class="error">Error fetching top losers. Please try again later.</p>';
    });
}

// Consolidated function to run when the page is loaded
document.addEventListener('DOMContentLoaded', function () {
    console.log('Page is fully loaded');
    // Fetch top gainers and losers
    fetchTopGainersAndLosers('30d'); // Use default period for initial fetch

    // Set a timer to update every 10 minutes (600000 ms)
    setInterval(() => fetchTopGainersAndLosers('30d'), 600000); // 10 minutes

    // Apply saved theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.remove('dark-mode');
    }
});
