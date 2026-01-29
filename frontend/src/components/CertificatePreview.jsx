import { motion, useMotionValue, useSpring, useTransform } from 'framer-motion';
import { useRef } from 'react';

export default function CertificatePreview() {
  const ref = useRef(null);

  const mx = useMotionValue(0);
  const my = useMotionValue(0);

  const rx = useTransform(my, [-0.5, 0.5], [10, -10]);
  const ry = useTransform(mx, [-0.5, 0.5], [-12, 12]);

  const rotateX = useSpring(rx, { stiffness: 140, damping: 18 });
  const rotateY = useSpring(ry, { stiffness: 140, damping: 18 });

  function onMove(e) {
    const el = ref.current;
    if (!el) return;

    const r = el.getBoundingClientRect();
    const px = (e.clientX - r.left) / r.width - 0.5;
    const py = (e.clientY - r.top) / r.height - 0.5;

    mx.set(px);
    my.set(py);
  }

  function onLeave() {
    mx.set(0);
    my.set(0);
  }

  return (
    <div className="hidden lg:block">
      <motion.div
        initial={{ opacity: 0, x: 18 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
        className="relative"
      >
        <motion.div
          ref={ref}
          onMouseMove={onMove}
          onMouseLeave={onLeave}
          style={{ rotateX, rotateY, transformStyle: 'preserve-3d' }}
          animate={{ y: [0, -10, 0] }}
          transition={{ duration: 6.5, repeat: Infinity, ease: 'easeInOut' }}
          className="overflow-hidden rounded-3xl border border-white/10 bg-white/5 shadow-[0_35px_90px_rgba(0,0,0,0.45)] backdrop-blur-xl"
        >
          <div className="relative" style={{ transform: 'translateZ(26px)' }}>
            <img
              src="/certificate-template.jpg"
              alt="Certificate template"
              className="block h-auto w-full select-none"
              draggable={false}
              loading="eager"
            />

            <div className="pointer-events-none absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-black/35 to-transparent" />
          </div>
        </motion.div>

        <div className="absolute -inset-6 -z-10 rounded-[2rem] bg-gradient-to-r from-indigo-500/20 to-violet-500/20 blur-2xl" />
      </motion.div>
    </div>
  );
}
