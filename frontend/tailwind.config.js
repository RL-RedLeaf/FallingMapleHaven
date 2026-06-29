export default {
  content: ['./index.html', './src/**/*.{vue,js,ts}'],
  theme: {
    extend: {
      colors: {
        maple: {
          50: '#FFF8F0', 100: '#FFEAD5', 200: '#FFD4A8',
          300: '#FFB875', 400: '#F5A623', 500: '#E88A1E',
          600: '#C73B1D', 700: '#A32E16', 800: '#7A2210',
          900: '#52160B',
        },
        text: { primary: '#2D2D2D', secondary: '#8C8C8C' },
        border: '#E8DDD4',
      },
      fontFamily: {
        sans: ['"Noto Sans SC"', '"PingFang SC"', '"Microsoft YaHei"', 'sans-serif'],
      },
    },
  },
}
