import { motion } from 'framer-motion';

export default function GradientButton({
  children,
  className = '',
  type = 'button',
  onClick,
  disabled
}) {
  return (
    <motion.button
      type={type}
      onClick={onClick}
      disabled={disabled}
      whileHover={disabled ? undefined : { scale: 1.02 }}
      whileTap={disabled ? undefined : { scale: 0.99 }}
      transition={{ duration: 0.25, ease: 'easeOut' }}
      className={`group relative inline-flex w-full items-center justify-center gap-2 rounded-2xl bg-gradient-to-r from-indigo-500 to-violet-500 px-6 py-3.5 text-sm font-semibold text-white shadow-glow outline-none ring-1 ring-white/10 transition hover:shadow-[0_18px_70px_rgba(99,102,241,0.35)] disabled:cursor-not-allowed disabled:opacity-60 ${className}`}
    >
      <span className="absolute inset-0 -z-10 rounded-2xl bg-gradient-to-r from-indigo-500/50 to-violet-500/50 blur-xl opacity-70 transition group-hover:opacity-100" />
      {children}
    </motion.button>
  );
}
