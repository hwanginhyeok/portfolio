/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Pretendard', '"Apple SD Gothic Neo"', '"Noto Sans KR"', 'sans-serif'],
        display: ['"Outfit"', 'Pretendard', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'Pretendard', 'monospace'],
      },
      colors: {
        primary: '#1a1a2e',
        accent:  '#0066ff',
        'accent-dark': '#7ab8ff',
        surface: '#f8f9fa',
        muted:   '#6b7280',
        ink: {
          900: '#0f172a',
          700: '#334155',
          500: '#64748b',
          300: '#cbd5e1',
          100: '#f1f5f9',
          50:  '#f8fafc',
        },
        success: '#16a34a',
        warning: '#d97706',
        error:   '#dc2626',
        info:    '#0284c7',
      },
    },
  },
  plugins: [],
};
