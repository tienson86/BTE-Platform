/**
 * Phase A visual fixture for Life Consulting. Not production content.
 */

import { adaptLifeConsulting } from "./lifeConsultingAdapter";
import type { LifeConsultingView } from "./types";

/** Deterministic sample structure. Not a named production case. */
export const LIFE_CONSULTING_VISUAL_FIXTURE: LifeConsultingView = adaptLifeConsulting({
  identity: { person: { gender: "male" } },
  ten_gods: {
    visible: [
      { pillar: "year", ten_god: "Thất Sát" },
      { pillar: "month", ten_god: "Kiếp Tài" },
      { pillar: "day", ten_god: "Nhật Chủ" },
      { pillar: "hour", ten_god: "Thiên Ấn" },
    ],
    hidden: [
      { pillar: "year", ten_god: "Thiên Tài" },
      { pillar: "month", ten_god: "Chính Ấn" },
    ],
    visible_labels: ["Thất Sát", "Kiếp Tài", "Nhật Chủ", "Thiên Ấn"],
  },
  pattern: { cach_cuc: "Chính Ấn" },
  strength: { strength_level: "strong" },
  useful_god: { useful_display: "Thủy · Nhâm · Thực Thần" },
});
