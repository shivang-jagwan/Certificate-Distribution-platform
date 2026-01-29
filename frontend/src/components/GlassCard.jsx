import { motion } from 'framer-motion';

export default function GlassCard({ children, className = '', hover = true }) {
  return (
    <motion.div
      whileHover={hover ? { y: -2 } : undefined}
      transition={{ duration: 0.35, ease: 'easeOut' }}
      className={`rounded-3xl border border-white/12 bg-white/6 shadow-glass backdrop-blur-xl ${className}`}
    >
      {children}
    </motion.div>
  );
}
