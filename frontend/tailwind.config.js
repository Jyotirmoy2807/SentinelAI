/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#172033",
        surface: "#f7f9fc",
        line: "#d8dee9",
        brand: "#1d4ed8",
        teal: "#0f766e",
        amber: "#b45309",
        danger: "#b91c1c"
      },
      boxShadow: {
        soft: "0 10px 30px rgba(23, 32, 51, 0.08)"
      }
    }
  },
  plugins: []
};
