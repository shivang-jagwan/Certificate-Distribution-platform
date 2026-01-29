import Background from './Background.jsx';

export default function AppShell({ children }) {
  return (
    <div className="relative min-h-screen text-white">
      <Background />
      <div className="relative z-10">{children}</div>
    </div>
  );
}
