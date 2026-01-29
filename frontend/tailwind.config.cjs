/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        navy: {
          950: '#070A1C',
          900: '#0A0E27',
          800: '#11183A'
        }
      },
      boxShadow: {
        glass: '0 20px 60px rgba(0,0,0,0.35)',
        glow: '0 20px 60px rgba(99,102,241,0.25)'
      },
      borderRadius: {
        '2xl': '1.25rem',
        '3xl': '1.75rem'
      }
    }
  },
  plugins: []
};
