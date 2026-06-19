/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#66B97B',
        dark: '#222323',
        background: '#F2F2F2',
        grey: '#CBCBCB',
        'grey-dark': '#B0B0B0',
        red: '#F21D61',
        'blue-group': '#72E6EA',
        yellow: '#BCD11A',
        'blue-info': '#45C1EE',
      },
      fontFamily: {
        roboto: ['Roboto', 'sans-serif'],
        marker: ['"Permanent Marker"', 'cursive'],
      },
      borderRadius: {
        card: '8px',
        button: '20px',
        badge: '4px',
      },
      boxShadow: {
        card: '0px 2px 12px rgba(0,0,0,0.2)',
      },
    },
  },
  plugins: [],
}
