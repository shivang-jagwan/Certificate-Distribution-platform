import { motion } from 'framer-motion';
import { useId, useMemo, useState } from 'react';

export default function InputField({
  label,
  value,
  onChange,
  type = 'text',
  autoComplete,
  inputMode,
  name,
  placeholder
}) {
  const reactId = useId();
  const id = useMemo(() => `${name || 'field'}-${reactId}`, [name, reactId]);
  const [focused, setFocused] = useState(false);

  const hasValue = String(value ?? '').length > 0;

  return (
    <div className="relative">
      <motion.div
        animate={{
          boxShadow: focused
            ? '0 0 0 4px rgba(99,102,241,0.16)'
            : '0 0 0 0px rgba(99,102,241,0)'
        }}
        transition={{ duration: 0.25, ease: 'easeOut' }}
        className="rounded-2xl"
      >
        <input
          id={id}
          name={name}
          value={value}
          onChange={onChange}
          type={type}
          autoComplete={autoComplete}
          inputMode={inputMode}
          placeholder={placeholder || ' '}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          className="peer w-full rounded-2xl border border-white/12 bg-white/5 px-4 pb-3 pt-5 text-sm text-white/90 outline-none transition placeholder:text-transparent focus:border-indigo-400/40"
        />

        <label
          htmlFor={id}
          className={`pointer-events-none absolute left-4 top-4 origin-left text-sm text-white/60 transition-all duration-200 ease-out peer-focus:-translate-y-2 peer-focus:scale-90 peer-focus:text-white/70 ${
            hasValue ? '-translate-y-2 scale-90 text-white/70' : ''
          }`}
        >
          {label}
        </label>
      </motion.div>
    </div>
  );
}
