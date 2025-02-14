import React, { useState, useEffect } from 'react';
import './styles.css';
import DarkMode from './DarkMode';

const App = () => {
    const [stockData, setStockData] = useState(null);

    const fetchStockData = async (symbol) => {
        const response = await fetch(`/api/stock/${symbol}`);
        const data = await response.json();
        setStockData(data);
    };

    useEffect(() => {
        fetchStockData('AAPL');  // Fetch Apple stock as an example on load
    }, []);

    return (
        <div>
            <h1>Real-Time Stock Market App</h1>
            <DarkMode />
            {stockData && (
                <div>
                    <h2>{stockData.symbol} Stock</h2>
                    <p>Price: {stockData.price}</p>
                </div>
            )}
        </div>
    );
};

export default App;
