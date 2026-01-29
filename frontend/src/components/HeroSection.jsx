import { motion } from 'framer-motion';
import GradientButton from './GradientButton.jsx';

export default function HeroSection({ onCta }) {
  return (
    <section className="mx-auto flex min-h-screen max-w-7xl items-center px-5 pt-28 sm:px-8 sm:pt-32">
      <div className="mx-auto max-w-3xl text-center">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs font-medium text-white/80 backdrop-blur"
        >
          <span className="grid h-5 w-5 place-items-center rounded-full bg-gradient-to-br from-indigo-500 to-violet-500 text-[10px] font-bold">
            ✓
          </span>
          Official Digital Certification Platform
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.08, ease: [0.22, 1, 0.36, 1] }}
          className="mt-8 text-4xl font-extrabold tracking-tight text-white sm:text-6xl"
        >
          Co-Dev Club
          <span className="block bg-gradient-to-r from-white to-indigo-200 bg-clip-text text-transparent">
            Certificate Portal
          </span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.65, delay: 0.18, ease: [0.22, 1, 0.36, 1] }}
          className="mx-auto mt-5 max-w-2xl text-base leading-relaxed text-white/70 sm:text-lg"
        >
          Securely Download and Verify Your Official Certificates
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.28, ease: [0.22, 1, 0.36, 1] }}
          className="mx-auto mt-10 max-w-xs"
        >
          <GradientButton onClick={onCta} className="w-full">
            Get Certificate
          </GradientButton>
        </motion.div>
      </div>
    </section>
  );
}
