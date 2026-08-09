import { memo } from "react";
import type { HeroModel } from "../../adapter/PortalResultModel";
import { Badge } from "../Shared/Badge";

export const Hero = memo(function Hero({ model }: { model: HeroModel }) {
  const tone =
    model.status === "error" ? "danger" : model.status === "ready" ? "success" : "warning";
  return (
    <header className="rv2-hero rv2-section" id="rv2-Hero" tabIndex={-1}>
      <p className="rv2-hero__name">{model.name}</p>
      <h1 className="rv2-hero__headline">{model.headline}</h1>
      <p className="rv2-hero__summary">{model.one_line_summary}</p>
      <Badge tone={tone}>{model.status_label}</Badge>
    </header>
  );
});
