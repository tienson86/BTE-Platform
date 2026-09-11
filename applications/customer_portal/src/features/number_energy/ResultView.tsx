import type { ReactNode } from "react";

import {
  DOMINANT_HEADING,
  ENDING_HEADING,
  ENDING_PAIR_LABEL,
  GROUPS_HEADING,
  NO_OCCURRENCES,
  PAIRS_HEADING,
  SUMMARY_HEADING,
  TECHNICAL_HEADING,
  TRIPLETS_HEADING,
} from "./labels";
import type { NumberEnergyData } from "./types";
import type { NumberEnergyPairChip, NumberEnergyReading } from "./readingTypes";

function ForceMeter({ level, label }: { level: number; label: string }): ReactNode {
  const filled = Math.min(4, Math.max(0, level));
  return (
    <span className="ne-force" title={label} aria-label={label}>
      {[1, 2, 3, 4].map((slot) => (
        <span key={slot} className={slot <= filled ? "is-on" : undefined} />
      ))}
    </span>
  );
}

function PairChip({ item }: { item: NumberEnergyPairChip }): ReactNode {
  return (
    <li className="ne-chip" data-testid="pair-chip">
      <span className="ne-chip__pair">{item.pair_digits}</span>
      <span className="ne-chip__name">{item.display_name}</span>
      {item.force_label ? (
        <ForceMeter level={item.force_level || 0} label={item.force_label} />
      ) : null}
      {item.expression ? <span className="muted ne-chip__note">{item.expression}</span> : null}
    </li>
  );
}

export function NumberEnergyResultView({ data }: { data: NumberEnergyData }): ReactNode {
  const reading: NumberEnergyReading = data.reading || {};
  const narrative = data.narrative || {};
  const metadata = data.metadata || {};
  const pairs = reading.pairs || [];
  const groups = reading.groups || [];
  const triplets = reading.triplets || [];
  const notices = reading.notices || [];
  const forceNotes = reading.force_notes || [];
  const summary = reading.summary || narrative.summary || "";
  const ending = reading.ending;
  const dominant = reading.dominant;

  return (
    <div className="ne-result" data-testid="number-energy-result">
      <section className="bte-card" data-testid="pairs-card">
        <h2>{PAIRS_HEADING}</h2>
        {pairs.length ? (
          <ul className="ne-chip-row">
            {pairs.map((item, index) => (
              <PairChip key={`${item.pair_digits}-${index}`} item={item} />
            ))}
          </ul>
        ) : (
          <p className="muted">{NO_OCCURRENCES}</p>
        )}
      </section>

      <section className="bte-card" data-testid="sim-summary">
        <h2>{SUMMARY_HEADING}</h2>
        {reading.leading_zero_note ? (
          <p className="muted" data-testid="leading-zero-note">
            {reading.leading_zero_note}
          </p>
        ) : null}
        {reading.interior_zero_note ? (
          <p data-testid="interior-zero-note">{reading.interior_zero_note}</p>
        ) : null}
        <p data-testid="narrative-summary">{summary || "—"}</p>
        {reading.supportive_balance_note ? (
          <p data-testid="supportive-balance">{reading.supportive_balance_note}</p>
        ) : null}
        {reading.consecutive_challenging_note ? (
          <p data-testid="consecutive-challenging">{reading.consecutive_challenging_note}</p>
        ) : null}
        {reading.lifted_note ? (
          <p data-testid="lifted-note">{reading.lifted_note}</p>
        ) : null}
        {forceNotes.map((item) => (
          <p key={item} data-testid="force-note">
            {item}
          </p>
        ))}
        <dl className="ne-kv">
          <dt>Sim đang luận</dt>
          <dd data-testid="display-number">{reading.display_number || metadata.input_raw || "—"}</dd>
          <dt>Nhóm cát tinh</dt>
          <dd data-testid="supportive-count">{reading.supportive_group_count ?? "—"}</dd>
          <dt>Nhóm cần lưu ý</dt>
          <dd data-testid="challenging-count">{reading.challenging_group_count ?? "—"}</dd>
        </dl>
      </section>

      {groups.length ? (
        <section className="bte-card" data-testid="energy-groups">
          <h2>{GROUPS_HEADING}</h2>
          {groups.map((group) => (
            <article key={group.display_name} className="ne-group" data-testid="energy-group">
              <h3>
                {group.display_name}:{" "}
                {group.pairs.map((pair, index) => (
                  <span key={`${pair}-${index}`} className="ne-inline-pair">
                    {pair}
                  </span>
                ))}
              </h3>
              {group.meaning ? <p>{group.meaning}</p> : null}
              {group.watchout ? (
                <p className="muted">
                  Điểm cần lưu ý: {group.watchout}
                </p>
              ) : null}
            </article>
          ))}
        </section>
      ) : null}

      {triplets.length ? (
        <section className="bte-card" data-testid="triplets-card">
          <h2>{TRIPLETS_HEADING}</h2>
          <ul className="ne-triplet-list">
            {triplets.map((item) => (
              <li key={item.digits} data-testid="triplet-item">
                {item.digits} = {item.left_name} + {item.right_name}
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      <section className="bte-card" data-testid="dominant-energy">
        <h2>{DOMINANT_HEADING}</h2>
        {dominant ? (
          <p>
            {dominant.display_name}
            {dominant.pairs?.length ? ` — ${dominant.pairs.join(", ")}` : ""}
          </p>
        ) : (
          <p className="muted">Chưa đủ dữ liệu V1 để luận phần này</p>
        )}
      </section>

      <section className="bte-card" data-testid="ending-energy">
        <h2>{ENDING_HEADING}</h2>
        {ending?.pair_digits && ending.display_name ? (
          <p data-testid="ending-pair">
            {ENDING_PAIR_LABEL}: {ending.pair_digits} — {ending.display_name}
          </p>
        ) : (
          <p data-testid="ending-pair">Chưa đủ dữ liệu V1 để kết luận năng lượng kết.</p>
        )}
        {ending?.note ? <p className="muted">{ending.note}</p> : null}
      </section>

      {notices
        .filter(
          (item) =>
            item !== reading.leading_zero_note &&
            item !== reading.interior_zero_note &&
            item !== reading.consecutive_challenging_note &&
            item !== reading.lifted_note &&
            !(forceNotes.includes(item)),
        )
        .map((item) => (
          <p key={item} className="muted" data-testid="reading-notice">
            {item}
          </p>
        ))}

      {reading.purpose_note ? (
        <p className="muted" data-testid="purpose-note">
          {reading.purpose_note}
        </p>
      ) : null}
      {reading.cccd_note ? (
        <p className="muted" data-testid="cccd-note">
          {reading.cccd_note}
        </p>
      ) : null}
      {narrative.health_disclaimer ? (
        <p className="ne-disclaimer" data-testid="health-disclaimer">
          {narrative.health_disclaimer}
        </p>
      ) : null}

      <details className="bte-card ne-tech" data-testid="technical-details">
        <summary>{TECHNICAL_HEADING}</summary>
        <dl className="ne-kv">
          <dt>Dãy nhập</dt>
          <dd>{reading.display_number || "—"}</dd>
          <dt>Phần luận</dt>
          <dd data-testid="analyzed-number">{reading.analyzed_number || "—"}</dd>
          <dt>Phiên bản knowledge</dt>
          <dd data-testid="knowledge-version">{metadata.knowledge_version || "—"}</dd>
        </dl>
      </details>
    </div>
  );
}
