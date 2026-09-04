/**
 * Customer Ten Gods combination consulting assets.
 * Lookup published visible names only. Does not calculate Ten Gods.
 */

const TRADITIONAL_ORDER = [
  "Tỷ Kiên",
  "Kiếp Tài",
  "Thực Thần",
  "Thương Quan",
  "Thiên Tài",
  "Chính Tài",
  "Thất Sát",
  "Chính Quan",
  "Thiên Ấn",
  "Chính Ấn",
] as const;

export type TenGodCombinationAsset = {
  readonly title: string;
  readonly insight: string;
  readonly capability: string;
  readonly income: string;
  readonly career: string;
  readonly leadership: string;
  readonly growth: string;
  readonly risk: string;
  readonly recommendation: string;
};

const COMBOS: Readonly<Record<string, TenGodCombinationAsset>> = {
  "Thực Thần|Thiên Tài": {
    title: "Đổi cửa lệch thành món thấy được",
    insight:
      "Bạn tạo giá trị khi bắt một cơ hội không cố định và biến nó thành sản phẩm người khác nhận được.",
    capability: "Bạn vừa thấy cửa phụ, vừa đưa tay nghề thành món có hạn. Thiếu chốt thì cửa lệch chỉ còn là ý.",
    income:
      "Tiền đến khi dự án lệch được đóng thành hàng, buổi, gói có thù lao. Để cửa mở hoài thì không thành sổ.",
    career: "Bạn hợp việc dự án, đa kênh có đầu ra. Ngồi một tuyến cố định làm lãng phí phản xạ cửa.",
    leadership: "Cầm việc bằng hai cửa có hạn chốt, neo một nghĩa vụ chính. Không bung mọi ý cùng lúc.",
    growth: "Mở rộng khi một món đã chốt thù lao. Thêm cửa lệch trước khi ra hàng làm loãng nguồn.",
    risk: "Săn cơ không ra món. Xả sức trên cửa không đo được làm mỏng nền trước khi tiền về.",
    recommendation: "Giữ tối đa hai cửa lệch. Mỗi cửa phải có một thành phẩm và một kỳ hạn chốt.",
  },
  "Thương Quan|Thiên Tài": {
    title: "Sửa khung bằng cửa không cố",
    insight: "Bạn tạo giá trị khi thấy lỗ hệ thống và mở một lối đi ngoài tuyến đang kẹt.",
    capability: "Bạn vừa chất vấn quy trình giả ổn, vừa giữ option ngoài hợp đồng thẳng.",
    income: "Tiền đến từ gỡ nút cổ chai và kênh phụ. Đụng cấp giữ phép hoặc không chốt cửa thì nguồn đứng.",
    career: "Bạn hợp việc rà soát luồng, mở kênh mới. Môi trường thứ bậc cứng sẽ chặn phản biện.",
    leadership: "Cầm việc bằng bản thay tối thiểu trước khi phá. Giữ một neo chính để cửa lệch không nuốt lịch.",
    growth: "Nâng quy mô khi bản thay đã chạy một vòng. Phá thêm tầng trước khi chốt cửa làm mất chữ tín.",
    risk: "Phá khung trước khi có bản thay. Nhiều option khiến không cam kết được cửa đang đòi độc.",
    recommendation: "Đưa phản biện vào kênh có người nhận. Mỗi cửa lệch phải có hạn chốt.",
  },
  "Chính Quan|Chính Ấn": {
    title: "Chạy việc trong khung có nền",
    insight: "Bạn tạo giá trị khi việc chạy vì có chuẩn, và có chỗ ủ trước khi bung.",
    capability: "Bạn chịu được quy trình và chỗ dựa có khuôn. Thiếu điểm ra thì khung thành bọc kín.",
    income: "Tiền đến theo phép và chậm: duyệt, chức, nguồn được nâng. Chờ quá lâu hoặc ủ mãi thì sổ đứng.",
    career: "Bạn hợp môi trường có cấp bậc và chương chuẩn. Cửa mở ngắn sẽ làm bạn chậm hơn nhịp thị trường.",
    leadership: "Cầm việc bằng một khung gọn, ủ có hạn, rồi ra một thành phẩm. Không thêm tầng duyệt.",
    growth: "Leo bậc khi một thành phẩm đã ra. Ủ thêm chương trước khi mở cửa làm chậm sổ.",
    risk: "Khung nuốt sáng kiến. Nền che mất cửa lưu thông đang cần chảy.",
    recommendation: "Giữ một việc được tự quyết. Ủ trong chương có hạn, rồi phải mở một cửa lưu thông.",
  },
  "Kiếp Tài|Thất Sát": {
    title: "Mở cửa khi việc đang khó",
    insight: "Bạn tạo giá trị khi bứt cửa hiểm đúng lúc nguồn đang kẹt, rồi trả phần cho người giữ sổ.",
    capability: "Bạn vừa chịu được hạn chót, vừa phản xạ nhanh khi cửa sắp khép.",
    income: "Tiền đến từ cửa rủi có hạn và hoa hồng ngắn. Sống bằng báo động sẽ không giữ được quỹ.",
    career: "Bạn hợp việc khủng hoảng, tranh cửa, hạn ngắn. Việc giữ sổ dài làm lãng phí tốc độ.",
    leadership: "Cầm việc khi cửa đang khó. Ghi phần trước khi tranh. Trả quyền khi cửa êm.",
    growth: "Giữ nhịp sau mỗi cửa hiểm. Nhân bản cửa ngắn khi chưa có quỹ sẽ xóa sổ.",
    risk: "Áp thành nền. Hớt phần đồng sự làm mất chữ tín. Không còn quỹ dự phòng.",
    recommendation: "Đặt mốc cắt cho cửa hiểm. Dùng tốc độ để mở đường, giữ một quỹ không đụng.",
  },
  "Kiếp Tài|Thất Sát|Thiên Ấn": {
    title: "Bứt cửa hiểm bằng lối không theo khuôn",
    insight:
      "Bạn tạo giá trị khi chịu được việc khó, mở cửa đúng lúc nguồn kẹt, và đi bằng kỹ năng không nằm trên chức danh.",
    capability:
      "Bạn bứt việc người khác né, chớp nhịp ngắn, rồi tự dưỡng khi khung chính thiếu. Thiếu mốc cắt thì báo động thành nền.",
    income:
      "Tiền đến từ cửa rủi, hoa hồng nhanh, và kỹ năng khó ghi bằng. Không có bằng chứng nhỏ thì cửa lớn không chốt thù lao.",
    career:
      "Bạn hợp việc hạn chót, tranh cửa, cố vấn lệch ngành. Ngồi ghế chuẩn và giữ sổ dài làm chậm phản xạ.",
    leadership:
      "Cầm việc khi cửa đang khó, ghi phần trước khi tranh, đổi cảm thành một mốc kiểm rồi trả quyền khi cửa êm.",
    growth:
      "Nâng cửa khi đã có mốc cắt và một bằng chứng nhỏ. Nhân báo động trước khi dưỡng sẽ kiệt nền.",
    risk: "Sống trong báo động. Hớt phần làm mất chữ tín. Lối lệch không đo được khiến khó cộng tác.",
    recommendation:
      "Đặt mốc cắt cho cửa hiểm. Giữ một quỹ không đụng. Ghi một bằng chứng nhỏ trước mỗi cửa lớn.",
  },
};

function orderedNames(names: readonly string[]): string[] {
  const present = new Set(
    names.map((name) => name.trim()).filter((name) => name && name !== "Nhật Chủ"),
  );
  return TRADITIONAL_ORDER.filter((name) => present.has(name));
}

function comboKey(names: readonly string[]): string {
  return names.join("|");
}

/**
 * Copy combination consulting for a published visible set. Omits when no asset exists.
 */
export function tenGodCombinationAsset(
  names: readonly string[],
): (TenGodCombinationAsset & { readonly members: readonly string[] }) | null {
  const ordered = orderedNames(names);
  if (ordered.length < 2) return null;
  const exact = COMBOS[comboKey(ordered)];
  if (exact) return { ...exact, members: ordered };
  let bestKey = "";
  let bestLen = 1;
  for (const key of Object.keys(COMBOS)) {
    const members = key.split("|");
    if (members.length <= bestLen) continue;
    if (members.every((name) => ordered.includes(name))) {
      bestKey = key;
      bestLen = members.length;
    }
  }
  if (!bestKey) return null;
  const asset = COMBOS[bestKey];
  return asset ? { ...asset, members: bestKey.split("|") } : null;
}

const HIDDEN_SUPPORT: Readonly<Record<string, string>> = {
  "Thiên Tài|Chính Ấn":
    "Phía ẩn giữ cửa lệch và chỗ ủ. Đó là nền, chưa phải mô hình tiền đang chạy.",
};

/**
 * Quiet support copy for a published hidden set. Does not replace the visible model.
 */
export function tenGodHiddenCombinationSupport(names: readonly string[]): string {
  const ordered = orderedNames(names);
  if (ordered.length < 2) return "";
  const exact = HIDDEN_SUPPORT[comboKey(ordered)];
  if (exact) return exact;
  for (const key of Object.keys(HIDDEN_SUPPORT)) {
    const members = key.split("|");
    if (members.length >= 2 && members.every((name) => ordered.includes(name))) {
      return HIDDEN_SUPPORT[key] ?? "";
    }
  }
  return "";
}
