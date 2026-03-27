import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        paper: "#f6f4ef",
        ink: "#111111",
        accent: "#1f6f78",
      },
      fontFamily: {
        sans: ["'Manrope'", "'Avenir Next'", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
