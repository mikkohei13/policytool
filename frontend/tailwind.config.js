const defaultTheme = require('tailwindcss/defaultTheme')

/** @type {import("@types/tailwindcss/tailwind-config").TailwindConfig } */
module.exports = {
    content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
    theme: {
        colors: {
            transparent: 'transparent',
            current: 'currentColor',
            blue: {
                DEFAULT: '#0C86C6',
                dark: '#205692',
            },
            yellow: '#ffd85d',
            grey: {
                lighter: '#f4f4f1',
                light: '#e9e8e3',
                DEFAULT: '#d9d9df',
                dark: '#b4b4bf',
                darker: '#868696',
            },
            white: '#ffffff',
            status: {
                new: '#10c1ff',
                handled: '#f7a112',
                approved: '#3dca77',
                denied: '#e74c3c',
                resolved: '#b4b4bf',
            }
        },
        extend: {
            fontFamily: {
                sans: [
                    '"Titillium Web"',
                    '"Open Sans"',
                    ...defaultTheme.fontFamily.sans],
            },
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/line-clamp'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
