import type { InputHTMLAttributes } from "react";

type SearchFieldProps = Omit<
  InputHTMLAttributes<HTMLInputElement>,
  "type"
> & {
  label?: string;
};

export function SearchField({
  label = "Search charts",
  id = "chart-search",
  className = "",
  ...props
}: SearchFieldProps) {
  return (
    <label className="block w-full space-y-2 text-sm" htmlFor={id}>
      <span className="sr-only">{label}</span>
      <input
        id={id}
        type="search"
        enterKeyHint="search"
        autoComplete="off"
        className={`w-full rounded-xl border border-[var(--line)] bg-[var(--bg-elevated)] px-4 py-2.5 text-sm outline-none transition focus-visible:border-[var(--accent)] focus-visible:ring-2 focus-visible:ring-[var(--accent)]/30 ${className}`}
        {...props}
      />
    </label>
  );
}
