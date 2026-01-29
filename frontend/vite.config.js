import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const backend = env.VITE_BACKEND_ORIGIN || 'http://localhost:8000';

  return {
    plugins: [react()],
    server: {
      port: 5173,
      proxy: {
        '^/verify$': backend,
        '^/certificate$': backend,
        '^/generate-all$': backend,
        '^/health$': backend,
        '/static': backend
      }
    }
  };
});
