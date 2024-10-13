/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: false,
  env: {
    AIGENT_430602_JSON: process.env.AIGENT_430602_JSON,
    GOOGLE_CLOUD_PROCESSOR_ID: process.env.GOOGLE_CLOUD_PROCESSOR_ID,
  },
}

module.exports = nextConfig
