import React, { useState, useEffect } from 'react';

const DarkMode = () => {
    const [darkMode, setDarkMode] = useState(localStorage.getItem('theme') === 'dark');

    useEffect(() => {
        if (darkMode) {
            document.body.classList.add('dark-mode');
            localStorage.setItem('theme', 'dark');
        } else {
            document.body.classList.remove('dark-mode');
            localStorage.setItem('theme', 'light');
        }
    }, [darkMode]);

    return (
        <button onClick={() => setDarkMode(!darkMode)}>
            Switch to {darkMode ? 'Light' : 'Dark'} Mode
        </button>
    );
};

export default DarkMode;
