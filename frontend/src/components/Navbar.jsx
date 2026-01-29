import { motion } from 'framer-motion';
import { useState } from 'react';

function Brand({ src, fallbackLetter, title }) {
  const [failed, setFailed] = useState(false);

  return (
    <div className="flex items-center gap-3">
      <div className="grid h-10 w-10 place-items-center overflow-hidden rounded-xl bg-gradient-to-br from-indigo-500 to-violet-500 shadow-glow ring-1 ring-white/10">
        {failed ? (
          <span className="text-sm font-extrabold text-white">{fallbackLetter}</span>
        ) : (
          <img
            src={src}
            alt={title}
            className="h-10 w-10 bg-white object-contain p-1"
            onError={() => setFailed(true)}
            loading="eager"
          />
        )}
      </div>
      <span className="hidden text-sm font-semibold tracking-tight text-white/90 sm:inline">
        {title}
      </span>
    </div>
  );
}

export default function Navbar() {
  return (
    <motion.header
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.55, ease: [0.22, 1, 0.36, 1] }}
      className="fixed left-0 right-0 top-0 z-50"
    >
      <div className="mx-auto max-w-7xl px-5 sm:px-8">
        <div className="mt-5 grid grid-cols-3 items-center rounded-3xl border border-white/10 bg-white/5 px-5 py-3 shadow-glass backdrop-blur-xl">
          <Brand
            src="/college-logo.jpg"
            fallbackLetter="G"
            title="Graphic Era College"
          />

          <div className="flex justify-center">
            <div className="relative">
              <div className="pointer-events-none absolute -inset-x-4 -inset-y-2 -z-10 rounded-2xl bg-gradient-to-r from-indigo-500/25 to-violet-500/25 blur-xl" />
              <div className="bg-gradient-to-r from-indigo-200 via-white to-violet-200 bg-clip-text text-center text-sm font-extrabold tracking-tight text-transparent sm:text-base">
                Certificate Portal
              </div>
            </div>
          </div>

          <div className="flex justify-end">
            <Brand src="/co-dev-logo.png" fallbackLetter="C" title="Co-Dev Club" />
          </div>
        </div>
      </div>
    </motion.header>
  );
}
