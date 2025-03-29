/** @type {import('next').NextConfig} */
const nextConfig = {
  allowedDevOrigins: process.env.ALLOWEDDEVORIGINS
    ? process.env.ALLOWEDDEVORIGINS.split(",")
    : ["localhost"],
  experimental: {
    serverActions: {
      bodySizeLimit: 5 * 1024 * 1024, // Increase limit to 5 MB
    },
  },
};

export default nextConfig;
