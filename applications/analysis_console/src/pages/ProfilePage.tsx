import { useState } from "react";
import { Link } from "react-router-dom";
import { PageHeader } from "../components/PageHeader";
import { useLibrary } from "../state/library";

export function ProfilePage() {
  const { profile, updateProfile, charts, customers } = useLibrary();
  const [saved, setSaved] = useState(false);

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <PageHeader
        eyebrow="Account"
        title="User Profile"
        description="Identity shown on the project dashboard and included in library exports."
        actions={
          <Link
            to="/settings"
            className="rounded-xl border border-[var(--line)] px-4 py-2.5 text-sm font-semibold transition hover:border-[var(--accent)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent)]"
          >
            Settings
          </Link>
        }
      />

      <section className="surface rounded-2xl p-6" aria-label="Profile summary">
        <div className="flex items-center gap-4">
          <div
            className="flex h-14 w-14 items-center justify-center rounded-full bg-[var(--accent-soft)] font-display text-2xl font-semibold text-[var(--accent)]"
            aria-hidden
          >
            {profile.display_name.slice(0, 1).toUpperCase()}
          </div>
          <div>
            <h2 className="font-display text-2xl font-semibold">
              {profile.display_name}
            </h2>
            <p className="text-sm text-[var(--muted)]">
              {profile.role} · {profile.organization}
            </p>
          </div>
        </div>
        <dl className="mt-5 grid grid-cols-2 gap-3 text-sm">
          <div>
            <dt className="text-[var(--muted)]">Charts</dt>
            <dd className="font-semibold">{charts.length}</dd>
          </div>
          <div>
            <dt className="text-[var(--muted)]">Customers</dt>
            <dd className="font-semibold">{customers.length}</dd>
          </div>
        </dl>
      </section>

      <form
        className="surface space-y-5 rounded-2xl p-6"
        onSubmit={(event) => {
          event.preventDefault();
          setSaved(true);
          window.setTimeout(() => setSaved(false), 1800);
        }}
      >
        {(
          [
            ["display_name", "Display name"],
            ["email", "Email"],
            ["role", "Role"],
            ["organization", "Organization"],
            ["locale", "Locale"],
          ] as const
        ).map(([key, label]) => (
          <label key={key} className="block space-y-2 text-sm">
            <span className="text-[var(--muted)]">{label}</span>
            <input
              className="w-full rounded-xl border border-[var(--line)] bg-transparent px-3 py-2.5 outline-none focus-visible:border-[var(--accent)] focus-visible:ring-2 focus-visible:ring-[var(--accent)]/30"
              value={profile[key]}
              onChange={(event) => updateProfile({ [key]: event.target.value })}
            />
          </label>
        ))}
        <label className="block space-y-2 text-sm">
          <span className="text-[var(--muted)]">Bio</span>
          <textarea
            rows={4}
            className="w-full rounded-xl border border-[var(--line)] bg-transparent px-3 py-2.5 outline-none focus-visible:border-[var(--accent)] focus-visible:ring-2 focus-visible:ring-[var(--accent)]/30"
            value={profile.bio}
            onChange={(event) => updateProfile({ bio: event.target.value })}
          />
        </label>
        <button
          type="submit"
          className="rounded-xl bg-[var(--accent)] px-4 py-2.5 text-sm font-semibold text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent)]"
        >
          Save profile
        </button>
        {saved ? (
          <p className="text-sm text-[var(--accent)]" role="status">
            Profile saved locally.
          </p>
        ) : null}
      </form>
    </div>
  );
}
