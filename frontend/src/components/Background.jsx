import { motion } from 'framer-motion';

function Shape({ className, delay = 0 }) {
  return (
    <motion.div
      className={className}
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{
        opacity: 1,
        scale: 1,
        x: [0, 60, -40, 0],
        y: [0, -40, 50, 0]
      }}
      transition={{
        opacity: { duration: 0.8, delay },
        scale: { duration: 0.8, delay },
        x: { duration: 18, repeat: Infinity, ease: 'easeInOut', delay },
        y: { duration: 22, repeat: Infinity, ease: 'easeInOut', delay }
      }}
    />
  );
}

export default function Background() {
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden">
      <div className="absolute inset-0 opacity-70">
        <div className="absolute -left-40 -top-40 h-[520px] w-[520px] rounded-full bg-indigo-500/25 blur-[90px]" />
        <div className="absolute -right-40 -bottom-40 h-[520px] w-[520px] rounded-full bg-violet-500/25 blur-[90px]" />
        <div className="absolute left-1/2 top-1/2 h-[420px] w-[420px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-sky-400/15 blur-[90px]" />
      </div>

      <Shape
        className="absolute -left-56 top-24 h-[520px] w-[520px] rounded-full bg-gradient-to-br from-indigo-500/25 to-violet-500/0 blur-[95px]"
        delay={0.1}
      />
      <Shape
        className="absolute -right-52 bottom-16 h-[480px] w-[480px] rounded-full bg-gradient-to-br from-violet-500/25 to-indigo-500/0 blur-[95px]"
        delay={0.3}
      />
      <Shape
        className="absolute left-1/2 top-[30%] h-[360px] w-[360px] -translate-x-1/2 rounded-full bg-gradient-to-br from-sky-400/20 to-indigo-500/0 blur-[90px]"
        delay={0.5}
      />

      <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_10%,rgba(99,102,241,0.10),transparent_40%),radial-gradient(circle_at_80%_80%,rgba(124,58,237,0.10),transparent_38%)]" />
    </div>
  );
}
