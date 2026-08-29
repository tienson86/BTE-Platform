/**
 * Phase A visual fixture for Action Plan. Not production content.
 */

import { ACTION_PLAN_EMPTY, ACTION_PLAN_TITLE } from "./cards";
import type { ActionPlanView } from "./types";

/** Deterministic practical layout sample. Isolated from live recommendations. */
export const ACTION_PLAN_VISUAL_FIXTURE: ActionPlanView = {
  title: ACTION_PLAN_TITLE,
  available: true,
  emptyMessage: ACTION_PLAN_EMPTY,
  priority: {
    title: "Dựng khung vận hành vừa đủ để việc chạy",
    detail: "Giữ trách nhiệm rõ, không chồng thêm lớp kiểm soát.",
    domain: "Lãnh đạo",
    source: "visual-fixture",
  },
  actions: [
    {
      title: "Giữ một nền học và dưỡng",
      detail: "Không bọc mọi việc vào cùng một khung.",
      domain: "",
      source: "visual-fixture",
    },
    {
      title: "Ra một việc nhỏ sau pha ủ",
      detail: "Để nhịp không bị kín.",
      domain: "",
      source: "visual-fixture",
    },
    {
      title: "Mở một kênh thoát có phép",
      detail: "Giữ nhịp, không bồi thêm lực khi nền đã vững.",
      domain: "",
      source: "visual-fixture",
    },
  ],
  extraActions: [
    {
      title: "Khoanh đúng biên trách nhiệm",
      detail: "Một việc rõ còn hơn nhiều việc chồng.",
      domain: "",
      source: "visual-fixture",
    },
  ],
  warnings: [
    {
      title: "Không ôm thêm tải vì còn sức",
      detail: "Ủ có hạn; ra một việc rồi mới mở.",
      domain: "",
      source: "visual-fixture",
    },
  ],
  watch: [
    {
      title: "Theo dõi nhịp gánh trong giai đoạn hiện tại",
      detail: "Giữ khung ổn định trước khi mở rộng.",
      domain: "",
      source: "visual-fixture",
    },
  ],
};
