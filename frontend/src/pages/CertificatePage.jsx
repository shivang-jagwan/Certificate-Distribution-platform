import { motion, AnimatePresence } from 'framer-motion';
import { useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import AppShell from '../components/AppShell.jsx';
import Navbar from '../components/Navbar.jsx';
import PageTransition from '../components/PageTransition.jsx';
import GlassCard from '../components/GlassCard.jsx';
import InputField from '../components/InputField.jsx';
import GradientButton from '../components/GradientButton.jsx';
import CertificatePreview from '../components/CertificatePreview.jsx';
import { withBackend } from '../lib/backend.js';

function Message({ type, text }) {
  const styles =
    type === 'success'
      ? 'border-emerald-400/30 bg-emerald-500/10 text-emerald-200'
      : 'border-rose-400/30 bg-rose-500/10 text-rose-200';

  return (
    <motion.div
      initial={{ opacity: 0, y: -8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -6 }}
      transition={{ duration: 0.25, ease: 'easeOut' }}
      className={`mt-5 rounded-2xl border px-4 py-3 text-sm ${styles}`}
    >
      {text}
    </motion.div>
  );
}

export default function CertificatePage() {
  const [studentName, setStudentName] = useState('');
  const [studentId, setStudentId] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  const canSubmit = useMemo(
    () => studentName.trim().length > 0 && studentId.trim().length > 0 && !loading,
    [studentName, studentId, loading]
  );

  async function onSubmit(e) {
    e.preventDefault();
    setMessage(null);

    const name = studentName.trim();
    const sid = studentId.trim();

    if (!name || !sid) {
      setMessage({ type: 'error', text: 'Please enter both name and student ID.' });
      return;
    }

    setLoading(true);

    try {
      const verifyUrl = withBackend(
        `/verify?name=${encodeURIComponent(name)}&student_id=${encodeURIComponent(sid)}`
      );
      const verifyResponse = await fetch(verifyUrl);

      if (!verifyResponse.ok) {
        throw new Error('Student not found. Please check your name and student ID.');
      }

      const data = await verifyResponse.json();

      setMessage({
        type: 'success',
        text: `Certificate found for ${data.name}. Download starting...`
      });

      const downloadUrl = withBackend(
        `/certificate?name=${encodeURIComponent(name)}&student_id=${encodeURIComponent(sid)}`
      );
      window.location.href = downloadUrl;
    } catch (err) {
      setMessage({ type: 'error', text: err?.message || 'Something went wrong.' });
    } finally {
      setLoading(false);
    }
  }

  return (
    <AppShell>
      <Navbar />

      <PageTransition className="mx-auto max-w-7xl px-5 pt-28 sm:px-8 sm:pt-32">
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
              Find Your Certificate
            </h2>
            <p className="mt-2 text-sm text-white/60">
              Enter your workshop name + ID exactly as submitted.
            </p>
          </div>

          <Link
            to="/"
            className="hidden rounded-2xl border border-white/10 bg-white/5 px-4 py-2 text-sm font-medium text-white/70 backdrop-blur transition hover:text-white md:inline"
          >
            Back
          </Link>
        </div>

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2 lg:gap-10">
          <GlassCard className="p-6 sm:p-8" hover>
            <form onSubmit={onSubmit} className="space-y-4">
              <InputField
                label="Student Name"
                name="studentName"
                value={studentName}
                onChange={(e) => setStudentName(e.target.value)}
                autoComplete="name"
              />
              <InputField
                label="Student ID"
                name="studentId"
                value={studentId}
                onChange={(e) => setStudentId(e.target.value)}
                inputMode="numeric"
                autoComplete="off"
              />

              <div className="pt-2">
                <GradientButton type="submit" disabled={!canSubmit}>
                  {loading ? 'Verifying…' : 'Download Certificate'}
                </GradientButton>
              </div>

              <AnimatePresence>
                {message ? <Message type={message.type} text={message.text} /> : null}
              </AnimatePresence>

              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.15, duration: 0.5 }}
                className="pt-2 text-xs text-white/45"
              >
                Tip: Name matching is case-insensitive, but spacing matters.
              </motion.div>
            </form>
          </GlassCard>

          <CertificatePreview />
        </div>
      </PageTransition>
    </AppShell>
  );
}
