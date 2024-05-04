/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        myyellow:'#fc8038',
        mygreen: '#53845b',
        headings:'#d75a1b',
        accent: '#6aa574'
      }
    }
  },
  plugins: [require('daisyui'),],
}

