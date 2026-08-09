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
      className="rv2-section rv2-section--reference"
      id="rv2-Appendix"
      tabIndex={-1}
      aria-labelledby="rv2-appx-title"
    >
      <SectionHeader id="rv2-appx-title" icon="appendix">
        {title}
      </SectionHeader>
      {model.scope ? <p className="rv2-prose rv2-type-note">{model.scope}</p> : null}
      {model.reread ? <p className="rv2-prose rv2-type-note">{model.reread}</p> : null}
      {model.limits ? <p className="rv2-prose rv2-type-note">{model.limits}</p> : null}
    </section>
  );
});
