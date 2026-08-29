/**
 * Phase A visual fixture for Interpretation. Not production content.
 */

import { INTERPRETATION_TITLE, INTERPRETATION_ZONE_LABELS } from "./cards";
import type { InterpretationView } from "./types";

/** Deterministic consultant layout sample. Isolated from live narrative. */
export const INTERPRETATION_VISUAL_FIXTURE: InterpretationView = {
  title: INTERPRETATION_TITLE,
  available: true,
  lead: "Lá số này nổi bật ở khả năng định khung: nội lực có, trách nhiệm rõ, và thành công đến khi giữ nhịp vừa đủ.",
  leadExtra: "",
  leadSource: "visual-fixture",
  zones: [
    {
      id: "observation",
      label: INTERPRETATION_ZONE_LABELS.observation,
      body: "Điều nổi bật nhất là nền tảng ổn định, nghiêng về vai trò chịu trách nhiệm hơn là bung sức ngắn hạn.",
      extra: "",
      source: "visual-fixture",
    },
    {
      id: "reasoning",
      label: INTERPRETATION_ZONE_LABELS.reasoning,
      body: "Cấu trúc mệnh cục và mức lực cùng hướng về một trục: đặt khung trước, rồi mới mở rộng.",
      extra: "",
      source: "visual-fixture",
    },
    {
      id: "impact",
      label: INTERPRETATION_ZONE_LABELS.impact,
      body: "Cách làm việc thiên về chủ động và chịu tải. Trong môi trường phù hợp, quyết định rõ hơn khi trách nhiệm được khoanh đúng.",
      extra: "",
      source: "visual-fixture",
    },
    {
      id: "recommendation",
      label: INTERPRETATION_ZONE_LABELS.recommendation,
      body: "Giữ khung vừa đủ để việc chạy. Không chồng thêm lớp kiểm soát khi nền đã vững.",
      extra: "Mở một việc nhỏ sau pha ủ để nhịp không bị kín.",
      source: "visual-fixture",
    },
  ],
  closing: "Đây là cấu trúc có nền để phát triển bền. Giữ trọng tâm và kỷ luật nhịp sẽ rõ hơn trong trung hạn.",
  closingSource: "visual-fixture",
};
