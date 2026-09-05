/**
 * Phase A visual fixture for Luck. Not production content.
 */

import { LUCK_TITLE } from "./cards";
import type { LuckCycleView, LuckView } from "./types";

const CYCLES: readonly LuckCycleView[] = [
  { ganZhi: "Canh Tý", yearRange: "1992–2001", ageRange: "5–14 tuổi", isCurrent: false },
  { ganZhi: "Tân Sửu", yearRange: "2002–2011", ageRange: "15–24 tuổi", isCurrent: false },
  { ganZhi: "Nhâm Dần", yearRange: "2012–2021", ageRange: "25–34 tuổi", isCurrent: false },
  { ganZhi: "Ất Tỵ", yearRange: "2022–2031", ageRange: "35–44 tuổi", isCurrent: true },
  { ganZhi: "Đinh Mùi", yearRange: "2032–2041", ageRange: "45–54 tuổi", isCurrent: false },
  { ganZhi: "Mậu Thân", yearRange: "2042–2051", ageRange: "55–64 tuổi", isCurrent: false },
  { ganZhi: "Kỷ Dậu", yearRange: "2052–2061", ageRange: "65–74 tuổi", isCurrent: false },
  { ganZhi: "Canh Tuất", yearRange: "2062–2071", ageRange: "75–84 tuổi", isCurrent: false },
  { ganZhi: "Tân Hợi", yearRange: "2072–2081", ageRange: "85–94 tuổi", isCurrent: false },
  { ganZhi: "Nhâm Tý", yearRange: "2082–2091", ageRange: "95–104 tuổi", isCurrent: false },
];

/** Deterministic timeline sample. Not the production validation case. */
export const LUCK_VISUAL_FIXTURE: LuckView = {
  title: LUCK_TITLE,
  available: true,
  current: CYCLES[3],
  direction: "Thuận",
  startAge: "5 tuổi",
  cycles: CYCLES,
  next: CYCLES[4],
  trend: "Đây là giai đoạn có xu hướng phát triển.",
  activation: null,
  interaction: null,
};
