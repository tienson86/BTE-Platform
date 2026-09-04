/**
 * Authored Life Consulting profiles.
 * Lookup keys stay internal. Customer copy does not list astrology.
 */

import type { LifeConsultingEvidence, LifeConsultingGender } from "./lifeConsultingEvidence";
import type { LifeDomainId } from "./types";

export const LIFE_CONSULTING_TITLE = "LĨNH VỰC ĐỜI SỐNG";

export const LIFE_DOMAIN_ORDER: readonly LifeDomainId[] = [
  "marriage",
  "children",
  "health",
  "career",
  "finance",
  "property",
];

export type LifeDomainNeed = {
  readonly gender?: Exclude<LifeConsultingGender, "">;
  readonly visibleAny?: readonly string[];
  readonly visibleAll?: readonly string[];
  readonly hiddenAny?: readonly string[];
  readonly presentAny?: readonly string[];
  readonly patternAny?: readonly string[];
  readonly usefulAny?: readonly string[];
  readonly strengthAny?: readonly string[];
  readonly shenshaAny?: readonly string[];
  readonly climateAny?: readonly string[];
  readonly fiveElementsAny?: readonly string[];
  readonly currentLuck?: boolean;
};

export type LifeDomainProfile = {
  readonly id: string;
  readonly domain: LifeDomainId;
  readonly title: string;
  readonly insight: string;
  readonly tendency: string;
  readonly strength: string;
  readonly opportunity: string;
  readonly risk: string;
  readonly recommendation: string;
  readonly when: LifeDomainNeed;
};

function hasToken(haystack: readonly string[], needle: string): boolean {
  return haystack.some((item) => item === needle || item.includes(needle));
}

function hasAny(haystack: readonly string[], needles: readonly string[]): boolean {
  return needles.some((needle) => hasToken(haystack, needle));
}

function hasAll(haystack: readonly string[], needles: readonly string[]): boolean {
  return needles.every((needle) => hasToken(haystack, needle));
}

function presentNames(evidence: LifeConsultingEvidence): readonly string[] {
  return [...evidence.visible, ...evidence.hidden];
}

/**
 * True when every declared need is already present on published evidence.
 */
export function lifeDomainProfileMatches(
  evidence: LifeConsultingEvidence,
  need: LifeDomainNeed,
): boolean {
  if (need.gender && evidence.gender !== need.gender) return false;
  if (need.visibleAny && !hasAny(evidence.visible, need.visibleAny)) return false;
  if (need.visibleAll && !hasAll(evidence.visible, need.visibleAll)) return false;
  if (need.hiddenAny && !hasAny(evidence.hidden, need.hiddenAny)) return false;
  if (need.presentAny && !hasAny(presentNames(evidence), need.presentAny)) return false;
  if (need.patternAny && !hasAny([evidence.pattern], need.patternAny)) return false;
  if (need.usefulAny && !hasAny([evidence.usefulDisplay, ...evidence.visible], need.usefulAny)) {
    return false;
  }
  if (need.strengthAny && !hasAny([evidence.strength], need.strengthAny)) return false;
  if (need.shenshaAny && !hasAny(evidence.shensha, need.shenshaAny)) return false;
  if (need.climateAny && !hasAny([evidence.climate, evidence.climateNeed], need.climateAny)) {
    return false;
  }
  if (need.fiveElementsAny && !hasAny([evidence.fiveElementsStatus], need.fiveElementsAny)) {
    return false;
  }
  if (need.currentLuck && !evidence.hasCurrentLuck) return false;
  return true;
}

export const LIFE_DOMAIN_PROFILES: readonly LifeDomainProfile[] = [
  {
    id: "marriage_male_side_wealth",
    domain: "marriage",
    title: "Hôn nhân",
    insight:
      "Bạn dễ gắn kết quanh nguồn chưa được gọi tên rõ, hơn là quanh một thỏa thuận thẳng.",
    tendency:
      "Xu hướng hiện tại nghiêng về quan hệ có chia phần, trong đó một phía giữ nguồn chưa đưa ra mặt.",
    strength:
      "Bạn giữ được sự gắn kết khi phần của mỗi người được nói ra, dù nguồn không nằm hết trên giấy.",
    opportunity:
      "Có thể xây quan hệ bền nếu hai bên chốt phần và giữ một quỹ riêng không tranh.",
    risk: "Tranh cùng một túi tiền làm mất chữ tín. Im lặng về phần dễ biến thành nợ tình cảm.",
    recommendation:
      "Nói rõ phần trước khi chung quỹ. Giữ một khoảng riêng. Đừng biến tình cảm thành cuộc tranh nguồn.",
    when: { gender: "male", presentAny: ["Thiên Tài", "Chính Tài"] },
  },
  {
    id: "marriage_female_role_pressure",
    domain: "marriage",
    title: "Hôn nhân",
    insight:
      "Bạn dễ gắn kết quanh vai và chuẩn, hơn là quanh việc gom nguồn. Quan hệ chạy khi vai được nói rõ.",
    tendency:
      "Xu hướng hiện tại nghiêng về người giữ phép hoặc chịu việc khó. Dễ gánh vai trước khi được gọi tên.",
    strength: "Bạn chịu được nhịp chung khi vai có hạn, không khi phải ôm hết quyết định.",
    opportunity: "Có thể ổn định nếu hai bên chốt ai giữ phép, ai chịu áp, và khi nào trả vai.",
    risk: "Chịu thay người kia đến kiệt. Im về vai biến thành sức ép không phép.",
    recommendation:
      "Nói rõ vai trước khi nhận thêm. Đặt mốc trả vai sau mỗi đợt khó. Đừng lấy việc chịu hết làm bằng chứng yêu.",
    when: { gender: "female", presentAny: ["Chính Quan", "Thất Sát"] },
  },
  {
    id: "children_output",
    domain: "children",
    title: "Con cái",
    insight: "Bạn nuôi dưỡng bằng việc làm ra và chỉ lại, không bằng gom địa vị cho người mình đang nâng.",
    tendency:
      "Xu hướng hiện tại nghiêng về dạy nghề, ra thành phẩm, để người được nâng cầm được việc.",
    strength: "Bạn truyền được tay nghề khi có một đầu ra rõ, có hạn, và người kia tự chốt được.",
    opportunity:
      "Có thể đồng hành bằng một việc cùng làm có hạn: sản phẩm, buổi dạy, quy trình nhỏ.",
    risk: "Ép theo thành tích hoặc ôm hết việc giúp sẽ làm mất nhịp tự đứng của người được nâng.",
    recommendation:
      "Chọn một việc cùng làm có hạn. Để người được nâng tự chốt thành phẩm; bạn chỉ giữ nhịp.",
    when: { usefulAny: ["Thực Thần", "Thương Quan"] },
  },
  {
    id: "health_hold_load",
    domain: "health",
    title: "Sức khỏe",
    insight: "Nền đang mạnh và bạn hay giữ áp lực bên trong, nên dễ quá tải trước khi kịp nghỉ.",
    tendency: "Xu hướng hiện tại là gánh rồi mới xả. Thân còn sức nên dễ bỏ qua tín hiệu mệt.",
    strength: "Bạn chịu được đợt áp nếu có mốc cắt và một nhịp dưỡng sau đó.",
    opportunity: "Sức đang dư cho phép chỉnh lịch nghỉ trước khi kiệt, không đợi đến lúc đổ.",
    risk: "Sống trong báo động biến thành nền. Ủ mệt mà không xả làm thân kiệt bất ngờ.",
    recommendation:
      "Đặt mốc cắt sau mỗi đợt áp. Một nhịp nghỉ bắt buộc. Đừng lấy sức dư làm lý do không nghỉ.",
    when: { patternAny: ["Chính Ấn", "Thiên Ấn"], strengthAny: ["Thân vượng"] },
  },
  {
    id: "health_hold",
    domain: "health",
    title: "Sức khỏe",
    insight: "Bạn hay ủ và giữ bên trong. Thân cần một điểm ra, không chỉ một chỗ dựa.",
    tendency: "Xu hướng hiện tại nghiêng về tích rồi mới xả. Dễ trì nghỉ vì đang còn cầm được.",
    strength: "Bạn hồi được nếu ủ có hạn rồi phải ra một nhịp xả.",
    opportunity: "Có thể giữ sức bằng một chương nghỉ có hạn, rồi trở lại việc.",
    risk: "Bọc kín làm trì. Mệt nằm lại bên trong đến khi đột ngột mất nhịp.",
    recommendation: "Ủ trong một hạn rồi phải xả. Giữ một việc nhẹ bắt buộc mỗi ngày để thân không đứng.",
    when: { patternAny: ["Chính Ấn", "Thiên Ấn"] },
  },
  {
    id: "health_weak",
    domain: "health",
    title: "Sức khỏe",
    insight: "Nền đang mỏng. Bạn cần nhịp dưỡng trước khi nhận thêm đợt áp.",
    tendency: "Xu hướng hiện tại dễ kiệt nếu nhận việc khó liên tiếp không có điểm dừng.",
    strength: "Bạn giữ được nếu chia nhỏ đợt và có nghỉ thật sau mỗi khối.",
    opportunity: "Có thể hồi nền khi giảm tải có hạn, không cần đợi một kỳ nghỉ dài.",
    risk: "Gánh thêm vì chữ tín sẽ làm thân sụt trước việc.",
    recommendation: "Cắt một khối việc. Chốt giờ nghỉ như chốt hạn việc. Đừng lấy ý chí bù nền.",
    when: { strengthAny: ["Thân nhược"] },
  },
  {
    id: "health_climate_cool",
    domain: "health",
    title: "Sức khỏe",
    insight: "Cơ thể đang thiên lạnh. Bạn cần nhịp ôn và đều, không cần thêm đợt xả lạnh.",
    tendency: "Xu hướng hiện tại dễ mỏi khi lịch thất thường, ăn và ngủ lệch nhịp.",
    strength: "Bạn ổn hơn khi giữ một nhịp ấm đều: ngủ, bữa, vận động nhẹ có hạn.",
    opportunity: "Chỉnh lịch đều trước khi tăng tải. Ôn nền rồi mới nhận đợt khó.",
    risk: "Thêm việc đêm, bỏ bữa, hoặc xả sức lúc đang lạnh làm thân tụt nhanh.",
    recommendation: "Giữ giờ ngủ và bữa ổn định. Vận động nhẹ có hạn. Đừng lấy việc khó sưởi người.",
    when: { climateAny: ["Hàn", "Lương", "Cần ôn ấm"] },
  },
  {
    id: "health_climate_warm",
    domain: "health",
    title: "Sức khỏe",
    insight: "Cơ thể đang thiên nóng. Bạn cần nhịp hạ và cắt, không cần thêm đợt áp.",
    tendency: "Xu hướng hiện tại dễ bốc khi nhận hạn chót liên tiếp, ít chỗ hạ.",
    strength: "Bạn chịu được đợt ngắn nếu có mốc cắt và chỗ hạ sau đó.",
    opportunity: "Hạ nhịp trước khi nhận thêm. Cắt một đợt nóng còn đang kéo.",
    risk: "Sống trong báo động làm khô nền. Không hạ sau đợt áp sẽ kiệt đột ngột.",
    recommendation: "Đặt mốc cắt. Giữ một việc hạ nhịp mỗi ngày. Đừng chồng hạn chót.",
    when: { climateAny: ["Nhiệt", "Ôn", "Cần làm mát"] },
  },
  {
    id: "health_elements_off",
    domain: "health",
    title: "Sức khỏe",
    insight: "Phân bố đang lệch. Bạn cần nhịp đều hơn là một đợt bù thật mạnh.",
    tendency: "Xu hướng hiện tại dễ quá tải ở chỗ đang nhiều, và thiếu chỗ đang mỏng.",
    strength: "Bạn giữ được nếu không dồn hết sức vào một việc.",
    opportunity: "Chia tải, xen việc nặng với việc dưỡng, thay vì bù một mạch.",
    risk: "Bù mạnh một phía làm lệch thêm. Bỏ việc dưỡng vì việc đang thắng.",
    recommendation: "Giữ một việc dưỡng không cắt. Đừng dồn hết sức vào chỗ đang đầy.",
    when: { fiveElementsAny: ["MẤT CÂN BẰNG NHẸ", "LỆCH RÕ"] },
  },
  {
    id: "career_pressure_skill",
    domain: "career",
    title: "Sự nghiệp",
    insight:
      "Bạn tạo giá trị khi chịu được việc khó, rồi cầm việc bằng kỹ năng không nằm trên chức danh.",
    tendency:
      "Xu hướng hiện tại nghiêng về đợt hạn chót và vai không chuẩn hóa, hơn là ngồi một tuyến êm.",
    strength: "Bạn bứt được việc người khác né, nếu còn điểm dừng và cách ghi lại kỹ năng lệch chuẩn.",
    opportunity: "Việc khó có thù lao cao khi bạn vào đúng lúc, rồi trả vai khi êm.",
    risk: "Ở mãi trong khủng hoảng làm gãy thân. Kỹ năng không ghi được thì khó chốt thù lao.",
    recommendation:
      "Nhận việc khó có hạn. Ghi kỹ năng lệch chuẩn thành bằng chứng nhỏ trước khi nhận đợt lớn hơn.",
    when: { visibleAll: ["Thất Sát", "Thiên Ấn"] },
  },
  {
    id: "career_pressure",
    domain: "career",
    title: "Sự nghiệp",
    insight: "Bạn tạo giá trị khi chịu được việc khó có hạn, không khi biến báo động thành nền.",
    tendency: "Xu hướng hiện tại nghiêng về hạn chót, khủng hoảng, trách nhiệm lệch.",
    strength: "Bạn đứng được khi có mốc cắt, yếu khi việc hiểm không có điểm trả vai.",
    opportunity: "Vào đúng đợt khó, chốt thù lao, rồi trả quyền khi êm.",
    risk: "Áp không phép thành kiệt. Sống trong báo động làm gãy thân và quan hệ.",
    recommendation: "Đặt mốc cắt cho việc hiểm. Ghép một nhịp dưỡng sau mỗi đợt áp.",
    when: { visibleAny: ["Thất Sát"] },
  },
  {
    id: "career_process",
    domain: "career",
    title: "Sự nghiệp",
    insight: "Bạn tạo giá trị khi việc chạy vì có chuẩn, vai rõ, duyệt gọn.",
    tendency: "Xu hướng hiện tại nghiêng về môi trường có cấp và quy trình, hơn là tự mở đường.",
    strength: "Bạn giữ nhịp khi duyệt gọn, yếu khi thêm tầng cho chắc.",
    opportunity: "Một chuẩn gọn để chạy việc, chừa một việc được tự quyết.",
    risk: "Chuẩn nuốt sáng kiến. Sợ lệch phép đến mức đứng im khi việc đang đổi.",
    recommendation: "Dùng một chuẩn để chạy, không thêm tầng duyệt. Giữ một việc tự quyết.",
    when: { visibleAny: ["Chính Quan"] },
  },
  {
    id: "career_output",
    domain: "career",
    title: "Sự nghiệp",
    insight: "Bạn tạo giá trị khi đổi sức thành thành phẩm người khác dùng được.",
    tendency: "Xu hướng hiện tại nghiêng về ra hàng, dạy nghề, sửa quy trình đang giả ổn.",
    strength: "Bạn giỏi khi có đầu ra rõ. Yếu khi họp dài không chốt việc.",
    opportunity: "Chốt một thành phẩm có hạn mỗi đợt. Đổi tay nghề thành thù lao thấy được.",
    risk: "Bung hết sức trước khi nguồn kịp về. Lời nhiều hơn việc làm khách chờ mãi.",
    recommendation: "Chốt một thành phẩm có hạn. Giữ nhịp nghỉ sau khi ra hàng.",
    when: { usefulAny: ["Thực Thần", "Thương Quan"] },
  },
  {
    id: "career_foundation",
    domain: "career",
    title: "Sự nghiệp",
    insight: "Bạn tạo giá trị khi được ủ trong chương có hạn, rồi mới bung thành phẩm.",
    tendency: "Xu hướng hiện tại nghiêng về học, giữ nền, chậm bung.",
    strength: "Bạn vững khi có chỗ dựa chuẩn. Yếu khi bị bọc kín không có điểm ra.",
    opportunity: "Ủ có hạn rồi ra một thành phẩm. Giữ việc học, mở một kênh lưu thông.",
    risk: "Ủ mãi làm trì. Nền nuốt mất việc đang cần chảy.",
    recommendation: "Đặt hạn cho chương học. Phải ra một thành phẩm trước khi ủ tiếp.",
    when: { patternAny: ["Chính Ấn", "Thiên Ấn"] },
  },
  {
    id: "finance_short_side",
    domain: "finance",
    title: "Tài chính",
    insight: "Tiền đến từ nhịp ngắn và kênh phụ, không từ một sổ dài độc quyền.",
    tendency:
      "Xu hướng hiện tại nghiêng về chớp nguồn khi đang kẹt, cộng nguồn chưa đưa ra mặt.",
    strength: "Bạn xoay được khi kênh chính chậm, miễn là còn một quỹ không đụng.",
    opportunity: "Giữ hai kênh: một nhịp ngắn có ghi phần, một kênh phụ có hạn chốt.",
    risk: "Tranh phần và săn cơ không sổ làm mất chữ tín. Không quỹ dự phòng thì nhịp ngắn nuốt nền.",
    recommendation: "Ghi phần trước khi chung. Giữ một quỹ không đụng. Tối đa hai kênh phụ, mỗi kênh có hạn.",
    when: { visibleAny: ["Kiếp Tài"], presentAny: ["Thiên Tài", "Chính Tài"] },
  },
  {
    id: "finance_planned",
    domain: "finance",
    title: "Tài chính",
    insight: "Tiền đến theo kế hoạch: hạn mức, hợp đồng, trách nhiệm nguồn vừa với nền.",
    tendency: "Xu hướng hiện tại nghiêng về sổ có phép, không về nhịp ngắn.",
    strength: "Bạn giữ sổ được khi hạn mức còn. Yếu khi ôm mọi khoản.",
    opportunity: "Đặt trần thu-chi. Tách cam kết việc khỏi việc gánh hết người khác.",
    risk: "Biến trách nhiệm thành phải nuôi hết. Sổ quá nền làm kiệt trước khi nguồn kịp về.",
    recommendation: "Đặt hạn mức nghĩa vụ nguồn. Không nhận thêm sổ khi trần đã chạm.",
    when: { presentAny: ["Chính Tài"] },
  },
  {
    id: "finance_output",
    domain: "finance",
    title: "Tài chính",
    insight: "Tiền đến khi công thành thù lao: hàng, dịch vụ, buổi dạy có hạn.",
    tendency: "Xu hướng hiện tại nghiêng về đổi sức thành khoản tiền thấy được, không giữ ý trong đầu.",
    strength: "Bạn thu được khi đầu ra rõ. Yếu khi làm không giữ nguồn.",
    opportunity: "Chốt giá theo thành phẩm. Một việc có hạn thành một khoản về.",
    risk: "Bung hết sức trước khi tiền về. Làm không sổ làm dòng mỏng.",
    recommendation: "Chốt thành phẩm và giá trước khi làm. Giữ một quỹ sau mỗi đợt ra hàng.",
    when: { usefulAny: ["Thực Thần", "Thương Quan"] },
  },
  {
    id: "finance_imprint",
    domain: "finance",
    title: "Tài chính",
    insight: "Tiền đến chậm: giữ nguồn, ít bung. Sổ đứng nếu ủ mãi không có điểm ra.",
    tendency: "Xu hướng hiện tại nghiêng về giữ, học, chậm chi.",
    strength: "Bạn giữ được quỹ khi không bung hết. Yếu khi nền che mất việc đang cần chảy.",
    opportunity: "Ủ có hạn rồi phải có một khoản lưu thông. Giữ quỹ, mở một kênh thu nhỏ.",
    risk: "Giữ quá chặt làm đứng sổ. Bọc kín nuốt mất nguồn đang cần về.",
    recommendation: "Giữ quỹ nền. Mở một kênh thu có hạn. Đừng ủ tiền đến mức không chạy việc.",
    when: { patternAny: ["Chính Ấn", "Thiên Ấn"] },
  },
  {
    id: "property_foundation_current",
    domain: "property",
    title: "Nhà đất",
    insight: "Nhà và đất với bạn là chỗ giữ nền. Giai đoạn hiện tại nên giữ hơn nới.",
    tendency: "Xu hướng hiện tại nghiêng về củng cố chỗ đang ở, học và ủ, chưa bung thêm chỗ.",
    strength: "Nền đang mạnh nên giữ được chỗ dựa, nếu không ôm thêm nghĩa vụ quá sức.",
    opportunity: "Củng cố chỗ đang có, chốt hạn mức, rồi mới xét nới sau giai đoạn này.",
    risk: "Nới thêm chỗ khi đang ủ sẽ làm trì. Bán nền để đổi nhịp ngắn làm mất chỗ dựa.",
    recommendation: "Giữ một chỗ nền trong giai đoạn hiện tại. Đặt hạn mức trước khi nới.",
    when: {
      patternAny: ["Chính Ấn", "Chính Quan", "Thiên Ấn"],
      strengthAny: ["Thân vượng"],
      currentLuck: true,
    },
  },
  {
    id: "property_foundation",
    domain: "property",
    title: "Nhà đất",
    insight: "Nhà và đất với bạn là chỗ giữ nền, không phải chỗ bung nhanh.",
    tendency: "Xu hướng hiện tại nghiêng về giữ chỗ ở và tài sản nền, học rồi mới nới.",
    strength: "Nền đang mạnh nên giữ được chỗ dựa, nếu không ôm thêm nghĩa vụ quá sức.",
    opportunity: "Củng cố chỗ đang ở, chốt hạn mức, rồi mới xét nới.",
    risk: "Bung thêm chỗ khi nền đang ủ sẽ làm trì. Ôm nhiều chỗ làm kiệt dòng.",
    recommendation: "Giữ một chỗ nền. Đặt hạn mức trước khi nới. Đừng bán nền để đổi nhịp ngắn.",
    when: { patternAny: ["Chính Ấn", "Chính Quan", "Thiên Ấn"], strengthAny: ["Thân vượng"] },
  },
  {
    id: "property_pattern",
    domain: "property",
    title: "Nhà đất",
    insight: "Nhà đất nên là chỗ ủ và giữ, không phải chỗ xoay vòng nhanh.",
    tendency: "Xu hướng hiện tại nghiêng về giữ chỗ đang có trước khi mở thêm.",
    strength: "Bạn vững hơn khi có một chỗ dựa, yếu khi nới trước khi nền kịp.",
    opportunity: "Chốt một chỗ nền. Nới chỉ khi hạn mức còn.",
    risk: "Mở thêm chỗ vì sốt ngắn làm mất chỗ dựa.",
    recommendation: "Giữ một chỗ. Đừng nới khi chưa chốt hạn mức.",
    when: { patternAny: ["Chính Ấn", "Chính Quan", "Thiên Ấn"] },
  },
];

/**
 * First authored profile whose published needs are met. Empty when none match.
 */
export function lifeDomainProfileFor(
  domain: LifeDomainId,
  evidence: LifeConsultingEvidence,
): LifeDomainProfile | null {
  return (
    LIFE_DOMAIN_PROFILES.find(
      (profile) => profile.domain === domain && lifeDomainProfileMatches(evidence, profile.when),
    ) ?? null
  );
}
