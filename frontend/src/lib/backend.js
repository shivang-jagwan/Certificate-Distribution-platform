export function getBackendOrigin() {
  const origin = import.meta.env.VITE_BACKEND_ORIGIN;
  return origin && String(origin).trim().length > 0 ? String(origin).trim() : '';
}

export function withBackend(path) {
  const origin = getBackendOrigin();
  if (!origin) return path;
  if (path.startsWith('http://') || path.startsWith('https://')) return path;
  if (!path.startsWith('/')) return `${origin}/${path}`;
  return `${origin}${path}`;
}
