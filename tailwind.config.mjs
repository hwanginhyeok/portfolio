/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Noto Sans KR"', '"Apple SD Gothic Neo"', 'sans-serif'],
      },
      colors: {
        primary: '#1a1a2e',
        accent: '#0066ff',
        surface: '#f8f9fa',
        muted: '#6b7280',
      },
    },
  },
  plugins: [],
};
