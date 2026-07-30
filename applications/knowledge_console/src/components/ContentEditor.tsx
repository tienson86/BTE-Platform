import type { ReactNode } from "react";
import type { AssetType } from "../api/types";

type Props = {
  assetType: AssetType;
  content: Record<string, unknown>;
  onChange: (next: Record<string, unknown>) => void;
  disabled?: boolean;
};

function Field({
  label,
  children,
}: {
  label: string;
  children: ReactNode;
}) {
  return (
    <label className="block space-y-1.5">
      <span className="text-xs font-medium uppercase tracking-wide text-[var(--muted)]">
        {label}
      </span>
      {children}
    </label>
  );
}

const inputClass =
  "w-full rounded-md border border-[var(--line)] bg-transparent px-3 py-2 text-sm text-[var(--fg)]";

export function ContentEditor({
  assetType,
  content,
  onChange,
  disabled,
}: Props) {
  const set = (key: string, value: unknown) =>
    onChange({ ...content, [key]: value });

  if (assetType === "rule") {
    return (
      <div className="grid gap-4 md:grid-cols-2">
        <Field label="Rule ID">
          <input
            className={inputClass}
            disabled={disabled}
            value={String(content.rule_id ?? "")}
            onChange={(e) => set("rule_id", e.target.value)}
          />
        </Field>
        <Field label="Priority">
          <input
            className={inputClass}
            type="number"
            disabled={disabled}
            value={Number(content.priority ?? 0)}
            onChange={(e) => set("priority", Number(e.target.value))}
          />
        </Field>
        <Field label="Condition">
          <textarea
            className={`${inputClass} min-h-24 font-mono text-xs`}
            disabled={disabled}
            value={String(content.condition ?? "")}
            onChange={(e) => set("condition", e.target.value)}
          />
        </Field>
        <Field label="Action">
          <textarea
            className={`${inputClass} min-h-24 font-mono text-xs`}
            disabled={disabled}
            value={String(content.action ?? "")}
            onChange={(e) => set("action", e.target.value)}
          />
        </Field>
      </div>
    );
  }

  if (assetType === "sentence") {
    return (
      <div className="grid gap-4">
        <div className="grid gap-4 md:grid-cols-2">
          <Field label="Sentence ID">
            <input
              className={inputClass}
              disabled={disabled}
              value={String(content.sentence_id ?? "")}
              onChange={(e) => set("sentence_id", e.target.value)}
            />
          </Field>
          <Field label="Section ID">
            <input
              className={inputClass}
              disabled={disabled}
              value={String(content.section_id ?? "")}
              onChange={(e) => set("section_id", e.target.value)}
            />
          </Field>
        </div>
        <Field label="Template">
          <textarea
            className={`${inputClass} min-h-32`}
            disabled={disabled}
            value={String(content.template ?? "")}
            onChange={(e) => set("template", e.target.value)}
          />
        </Field>
        <Field label="Placeholders (comma-separated)">
          <input
            className={inputClass}
            disabled={disabled}
            value={
              Array.isArray(content.placeholders)
                ? content.placeholders.join(", ")
                : ""
            }
            onChange={(e) =>
              set(
                "placeholders",
                e.target.value
                  .split(",")
                  .map((s) => s.trim())
                  .filter(Boolean),
              )
            }
          />
        </Field>
      </div>
    );
  }

  if (assetType === "phrase") {
    return (
      <div className="grid gap-4">
        <div className="grid gap-4 md:grid-cols-2">
          <Field label="Phrase ID">
            <input
              className={inputClass}
              disabled={disabled}
              value={String(content.phrase_id ?? "")}
              onChange={(e) => set("phrase_id", e.target.value)}
            />
          </Field>
          <Field label="Type">
            <input
              className={inputClass}
              disabled={disabled}
              value={String(content.type ?? "")}
              onChange={(e) => set("type", e.target.value)}
            />
          </Field>
        </div>
        <Field label="Text">
          <textarea
            className={`${inputClass} min-h-28`}
            disabled={disabled}
            value={String(content.text ?? "")}
            onChange={(e) => set("text", e.target.value)}
          />
        </Field>
        <Field label="Tags (comma-separated)">
          <input
            className={inputClass}
            disabled={disabled}
            value={
              Array.isArray(content.tags) ? content.tags.join(", ") : ""
            }
            onChange={(e) =>
              set(
                "tags",
                e.target.value
                  .split(",")
                  .map((s) => s.trim())
                  .filter(Boolean),
              )
            }
          />
        </Field>
      </div>
    );
  }

  return (
    <div className="grid gap-4 md:grid-cols-2">
      <Field label="Term ID">
        <input
          className={inputClass}
          disabled={disabled}
          value={String(content.term_id ?? "")}
          onChange={(e) => set("term_id", e.target.value)}
        />
      </Field>
      <Field label="Domain">
        <input
          className={inputClass}
          disabled={disabled}
          value={String(content.domain ?? "")}
          onChange={(e) => set("domain", e.target.value)}
        />
      </Field>
      <Field label="Display name">
        <input
          className={inputClass}
          disabled={disabled}
          value={String(content.display_name ?? "")}
          onChange={(e) => set("display_name", e.target.value)}
        />
      </Field>
      <Field label="Status">
        <input
          className={inputClass}
          disabled={disabled}
          value={String(content.status ?? "active")}
          onChange={(e) => set("status", e.target.value)}
        />
      </Field>
    </div>
  );
}
