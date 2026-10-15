/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          green: "#16813E", // primary AUSCAMP green
          "green-deep": "#0E5A2B", // gradient bottom / deep shade
          "green-dark": "#0A3D1E", // darkest, footer / text on light
          "green-mid": "#1E9C50", // lighter ray highlight
          yellow: "#FFC91A", // highlight bars / accents
          "yellow-deep": "#F4B400",
          cream: "#FAF7EC", // off-white text
        },
      },
      fontFamily: {
        sans: [
          "Plus Jakarta Sans",
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "Segoe UI",
          "Roboto",
          "Helvetica Neue",
          "Arial",
          "sans-serif",
        ],
        // Aspirational serif accent for hero eyebrow / pull phrases only.
        display: ["Fraunces", "ui-serif", "Georgia", "serif"],
      },
      boxShadow: {
        card: "0 10px 30px -12px rgba(0,0,0,0.35)",
        // Premium soft-lift for glass tiles + speaker photos.
        lift: "0 24px 60px -24px rgba(4,40,20,0.55)",
        "glass-inset": "inset 0 1px 0 0 rgba(255,255,255,0.14)",
      },
      keyframes: {
        "fade-up": {
          "0%": { opacity: "0", transform: "translateY(12px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        "pulse-dot": {
          "0%, 100%": { opacity: "1", transform: "scale(1)" },
          "50%": { opacity: "0.4", transform: "scale(0.8)" },
        },
      },
      animation: {
        "fade-up": "fade-up 0.5s ease-out both",
        "pulse-dot": "pulse-dot 1.8s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};
