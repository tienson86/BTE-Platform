import type { DomainKey } from "../../../adapter/PortalResultModel";

export type ResultIconName =
  | DomainKey
  | "summary"
  | "recommendation"
  | "warning"
  | "chart"
  | "knowledge"
  | "technical"
  | "appendix"
  | "footer"
  | "expand"
  | "empty"
  | "error"
  | "status";

const PATHS: Record<ResultIconName, string> = {
  summary:
    "M5 7h14M5 12h10M5 17h12",
  recommendation:
    "M12 4v3M12 17v3M4 12h3M17 12h3M8.2 8.2l2 2M13.8 13.8l2 2M8.2 15.8l2-2M13.8 10.2l2-2M14.2 12a2.2 2.2 0 1 1-4.4 0 2.2 2.2 0 0 1 4.4 0z",
  warning:
    "M12 5.2 4.8 18.5h14.4L12 5.2zM12 10.2v4M12 16.4h.01",
  career:
    "M8 9V7.8A2.8 2.8 0 0 1 10.8 5h2.4A2.8 2.8 0 0 1 16 7.8V9M5.5 9h13A1.5 1.5 0 0 1 20 10.5v7A1.5 1.5 0 0 1 18.5 19h-13A1.5 1.5 0 0 1 4 17.5v-7A1.5 1.5 0 0 1 5.5 9zM4.5 13h15",
  wealth:
    "M12 6.5v11M8.5 9.2c.8-1.2 2-1.8 3.5-1.8 2.2 0 3.6 1.2 3.6 2.8s-1.5 2.6-4.2 3c-2.4.4-4 1.4-4 3s1.6 2.8 4.1 2.8c1.7 0 3-.7 3.8-1.8",
  relationship:
    "M8.2 10.2a2.4 2.4 0 1 0 0-4.8 2.4 2.4 0 0 0 0 4.8zM15.8 10.2a2.4 2.4 0 1 0 0-4.8 2.4 2.4 0 0 0 0 4.8zM4.8 18.2c.4-2.4 2.2-3.8 4.4-3.8h.2c1.2 0 2.2.4 3 1.1M12.6 15.5c.8-.7 1.8-1.1 3-1.1h.2c2.2 0 4 1.4 4.4 3.8",
  health:
    "M12 20s-6.5-4.1-8.2-8.1C2.6 9.4 3.8 6.5 6.6 6.1c1.6-.2 3.1.5 4 1.8.9-1.3 2.4-2 4-1.8 2.8.4 4 3.3 2.8 5.8C18.5 15.9 12 20 12 20z",
  luck:
    "M7 8.5A4 4 0 0 1 14.5 7M17 15.5A4 4 0 0 1 9.5 17M14.2 6.2 15.2 4M14.2 6.2l2.2.4M9.8 17.8 8.8 20M9.8 17.8l-2.2-.4",
  chart:
    "M5 18V11M10 18V7M15 18v-5M20 18V9",
  knowledge:
    "M5 6.5h6.2A2.3 2.3 0 0 1 13.5 8.8V18a2 2 0 0 0-2-2H5zM19 6.5h-6.2A2.3 2.3 0 0 0 10.5 8.8V18a2 2 0 0 1 2-2H19z",
  technical:
    "M12 8.2a3.8 3.8 0 1 0 0 7.6 3.8 3.8 0 0 0 0-7.6zM12 4.5V6M12 18v1.5M4.5 12H6M18 12h1.5M6.6 6.6l1.1 1.1M16.3 16.3l1.1 1.1M6.6 17.4l1.1-1.1M16.3 7.7l1.1-1.1",
  appendix:
    "M7 5.5h7.2L19 10.2V18.5A1.5 1.5 0 0 1 17.5 20h-10A1.5 1.5 0 0 1 6 18.5v-12A1.5 1.5 0 0 1 7 5.5zM14 5.8V10h4.2",
  footer:
    "M12 5l2.4 4.8 5.3.8-3.8 3.7.9 5.3L12 17.1 7.2 19.6l.9-5.3L4.3 10.6l5.3-.8z",
  expand:
    "M7 10l5 5 5-5",
  empty:
    "M7 8h10M7 12h6M6 18.5h12A1.5 1.5 0 0 0 19.5 17V7A1.5 1.5 0 0 0 18 5.5H6A1.5 1.5 0 0 0 4.5 7v10A1.5 1.5 0 0 0 6 18.5z",
  error:
    "M12 8v5M12 16.2h.01M12 4.8A7.2 7.2 0 1 0 12 19.2 7.2 7.2 0 0 0 12 4.8z",
  status:
    "M6.5 12.2 10.2 16l7.3-8",
};

export function ResultIcon({
  name,
  decorative = true,
}: {
  name: ResultIconName;
  decorative?: boolean;
}) {
  return (
    <svg
      className="rv2-icon"
      viewBox="0 0 24 24"
      width="20"
      height="20"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden={decorative ? true : undefined}
      focusable="false"
    >
      <path d={PATHS[name]} />
    </svg>
  );
}
