import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  turbopack: { root: process.cwd() },
  devIndicators: false,
  agentRules: false
};

export default nextConfig;
