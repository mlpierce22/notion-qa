"use client"
import React, { useState, useEffect } from 'react';
import { Sun, Moon } from 'lucide-react';

const Toggle = () => {
    const [isDarkMode, setIsDarkMode] = useState(false);

    useEffect(() => {
        const htmlTag = document.documentElement;
        if (isDarkMode) {
            htmlTag.classList.add('dark');
        } else {
            htmlTag.classList.remove('dark');
        }
    }, [isDarkMode]);

    const toggleDarkMode = () => setIsDarkMode(!isDarkMode);

    return (
        <div className='flex justify-end space-y-4 max-w-5xl w-full'>
            <button onClick={toggleDarkMode} className='mr-5'>
                {isDarkMode ? <Sun /> : <Moon />}
            </button>
        </div>
    );
};

export default Toggle;


