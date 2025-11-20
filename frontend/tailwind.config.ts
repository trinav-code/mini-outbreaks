import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Background colors from Figma
        navy: {
          900: "#0F172A",
          800: "#1E293B",
          700: "#334155",
        },
        slate: {
          600: "#475569",
          500: "#64748B",
          400: "#94A3B8",
          300: "#CBD5E1",
          200: "#E2E8F0",
        },
        // Accent colors
        emerald: {
          DEFAULT: "#10B981",
          dark: "#059669",
        },
        // Status colors
        danger: "#EF4444",
        warning: "#F59E0B",
        success: "#10B981",
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-dark": "linear-gradient(to bottom, #0F172A, #1E293B)",
      },
      boxShadow: {
        "card": "0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2)",
        "card-hover": "0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -2px rgba(0, 0, 0, 0.3)",
        "inner-lg": "inset 0 2px 4px 0 rgba(0, 0, 0, 0.3)",
      },
      borderRadius: {
        "card": "12px",
        "input": "8px",
      },
      fontSize: {
        "hero": ["3.5rem", { lineHeight: "1.1", fontWeight: "600" }],
        "section": ["2.5rem", { lineHeight: "1.2", fontWeight: "600" }],
        "subtitle": ["1.125rem", { lineHeight: "1.7", fontWeight: "400" }],
      },
    },
  },
  plugins: [],
};

export default config;
