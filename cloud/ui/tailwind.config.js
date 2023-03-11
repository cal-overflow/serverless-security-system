// Lots of the styling for this project is taken from the https://github.com/cal-overflow/portfolio developer website template

module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Poppins"', 'sans-serif'],
      },
      colors: {
        footer: '#292929', // Background color of footer
        'main-light': '#FFFFFF', // Page background color in light mode
        'main-dark': '#191919', // Page background color in dark mode
        'menu-light': '#E0E0E1', // Background color of menu bar in light mode
        'menu-dark': '#1F1F1F', // Background color of menu bar in dark mode
        'card-light': '#EAEAEB', // Background color of each card in light mode
        'card-dark': '#262626', // Background color of each card in dark mode
        'primary-light': '#A61E17', // Primary color in light mode (red)
        'primary-dark': '#00B4E6', // Primary color in dark mode (light blue)
        'extra-gray-light': '#D5D5D7', // Extra gray color in light mode
        'extra-gray-dark': '#5A5A5E', // Extra gray color in dark mode
        'shadow-dark': '#212121', // Dark shadow color
      },
      keyframes: {
        'blur-in': {
          '0%': {
            filter: 'blur(1rem)',
          },
          '100%': {
            filter: 'blur(0px)',
          },
        },
        'fade-in': {
          '0%': {
            opacity: '0%',
          },
          '100%': {
            opacity: '100%',
          },
        },
        'zoom-in': {
          '0%': {
            transform: 'scale(0%)',
          },
          '100%': {
            transform: 'scale(100%)',
          },
        },
      },
      animation: {
        'blur-fade-in-fast': 'blur-in 0.5s ease-in-out',
        'blur-fade-in': 'blur-in 1s ease-in-out',
        'blur-fade-in-slow': 'blur-in 1.5s ease-in-out',
        'fade-in-fast': 'fade-in 0.25s ease-in-out',
        'fade-in': 'fade-in 1s ease-in-out',
        'fade-in-slow': 'fade-in 1.5s ease-in-out',
        'zoom-in-slow': 'zoom-in 1.5s ease-in-out',
        'zoom-in': 'zoom-in 1s ease-in-out',
        'zoom-in-fast': 'zoom-in 0.5s ease-in-out',
        'zoom-out-slow': 'zoom-in reverse 1.5s ease-in-out',
        'zoom-out': 'zoom-in reverse 1s ease-in-out',
        'zoom-out-fast': 'zoom-in reverse 0.5s ease-in-out',
        'rotate-upside-down': 'rotate-upside-down 0.25s ease-in-out',
      },
    },
  },
  darkMode: 'media',
};
