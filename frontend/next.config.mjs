import withPWA from "next-pwa";

const nextConfig = withPWA({
  dest: "public",
  register: true,
  skipWaiting: true,
})({
  reactStrictMode: true,

  // Allow Edge runtime + Worker proxy
  experimental: {
    webVitalsAttribution: ["CLS", "LCP", "FID"],
    optimizePackageImports: ["lucide-react", "recharts", "reactflow"]
  },

  // Where backend APIs live
  async rewrites() {
    return [
      {
        source: "/api/proxy/:path*",
        destination: "http://localhost:8000/:path*" // placeholder, replaced by env
      }
    ];
  },

  // Path aliases for @/*
  webpack(config) {
    config.resolve.alias = {
      ...(config.resolve.alias || {}),
      "@": require("path").resolve(__dirname, "./src")
    };
    return config;
  },

  // Allow Next to bundle workers correctly
  compiler: {
    removeConsole: process.env.NODE_ENV === "production"
  }
});

export default nextConfig;
