import { memo } from "react";
import type { AppendixModel } from "../../adapter/PortalResultModel";
import { showAppendix } from "../../utils/visibility";
import { SectionHeader } from "../Shared/SectionHeader";

export const Appendix = memo(function Appendix({
  title,
  model,
}: {
  title: string;
  model: AppendixModel | null;
}) {
  if (!showAppendix(model) || !model) return null;
  return (
    <section
      className="rv2-section"
      id="rv2-Appendix"
      tabIndex={-1}
      aria-labelledby="rv2-appx-title"
    >
      <SectionHeader id="rv2-appx-title">{title}</SectionHeader>
      {model.scope ? <p className="rv2-prose">{model.scope}</p> : null}
      {model.reread ? <p className="rv2-prose">{model.reread}</p> : null}
      {model.limits ? <p className="rv2-prose">{model.limits}</p> : null}
    </section>
  );
});
