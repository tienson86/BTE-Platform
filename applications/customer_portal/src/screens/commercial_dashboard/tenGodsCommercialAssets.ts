/**
 * Customer Ten Gods commercial interpretation assets.
 * Lookup only. Does not calculate Ten Gods or rewrite Narrative.
 */

export type TenGodCommercialAsset = {
  readonly insight: string;
  readonly capability: string;
  readonly income: string;
  readonly career: string;
  readonly risk: string;
  readonly recommendation: string;
};

const ASSETS: Readonly<Record<string, TenGodCommercialAsset>> = {
  "Tỷ Kiên": {
    insight: "Giá trị của bạn đến từ việc tự đứng phần mình, chia việc ngang, không chờ được bọc.",
    capability: "Bạn giữ được phần việc rõ ranh. Bạn làm tốt khi được giao đúng khối, không bị hòa vào quỹ chung.",
    income: "Tiền đến khi bạn giữ quỹ riêng và đổi công đúng phần. Ủy thác hết đáy nguồn thường làm dòng tiền đứng.",
    career: "Bạn hợp nhóm ngang hàng, tự gánh đúng vai. Cầm việc kiểu chia phần, không kiểu nuốt hết quyết định.",
    risk: "So phần và lập phe làm mỏng mỗi người. Tự làm hết cửa chuyên môn ngoài vai cũng làm chậm việc.",
    recommendation: "Chốt phần việc trước khi chung quỹ. Giữ một khung ngoài để ngang hàng không thành hỗn.",
  },
  "Kiếp Tài": {
    insight: "Giá trị của bạn đến từ tốc độ mở cửa khi nguồn đang kẹt, không đến từ giữ sổ dài.",
    capability: "Bạn phản xạ nhanh khi cửa sắp khép. Bạn bứt được nhịp ngắn mà người khác còn đang cân.",
    income: "Tiền đến từ chớp nguồn ngắn, hoa hồng nhanh, cửa xoay. Giữ quỹ chung dễ bị xóa sổ vì tranh phần.",
    career: "Bạn hợp việc cần tốc độ tranh cửa. Cầm nhịp để mở đường, rồi trả phần cho người giữ sổ.",
    risk: "Hớt phần đồng sự làm mất chữ tín. Sống bằng cửa ngắn khiến không còn quỹ dự phòng.",
    recommendation: "Dùng tốc độ để mở cửa, ghi phần trước khi tranh. Giữ một quỹ không đụng.",
  },
  "Thực Thần": {
    insight: "Giá trị của bạn đến từ đổi sức thành sản phẩm thấy được, không đến từ giữ ý trong đầu.",
    capability: "Bạn đưa tay nghề thành việc người khác dùng được. Bạn giỏi khi có khung đầu ra rõ.",
    income: "Tiền đến khi công thành thù lao: hàng, dịch vụ, buổi dạy nghề. Làm không giữ nguồn thì dòng tiền mỏng.",
    career: "Bạn hợp việc ra sản phẩm, kỹ thuật, chuyển nghề thành món có hạn. Cầm việc bằng chốt thành phẩm, không bằng họp dài.",
    risk: "Bung hết sức trước khi nguồn kịp về. Lời nhiều hơn việc làm khách chờ mãi không nhận được món.",
    recommendation: "Chốt một sản phẩm có hạn mỗi đợt. Giữ nhịp nghỉ sau khi ra hàng, đừng xả hết nền.",
  },
  "Thương Quan": {
    insight: "Giá trị của bạn đến từ nhìn lỗ khung và sửa hệ thống đang giả ổn.",
    capability: "Bạn thấy chỗ lệch mà người trong khung không nói. Bạn giỏi khi được phép chất vấn quy trình.",
    income: "Tiền đến từ phá cách cũ: audit, thiết kế lại luồng, gỡ nút cổ chai. Đụng cấp giữ phép có thể mất cửa.",
    career: "Bạn hợp việc rà soát và làm lại quy trình. Cầm việc bằng bản thay thế, không bằng xé khung công.",
    risk: "Phá chuẩn trước khi có chuẩn thay. Lời sắc làm gãy quan hệ với người đang giữ cục.",
    recommendation: "Đưa phản biện vào kênh có người nhận. Chỉ phá khi đã có bản thay tối thiểu.",
  },
  "Thiên Tài": {
    insight: "Giá trị của bạn đến từ cửa lệch: cơ hội không cố định, kênh phụ khi kênh chính đang kẹt.",
    capability: "Bạn nhìn thấy nguồn ngoài hợp đồng thẳng. Bạn giữ được nhiều cửa, miễn là biết lúc chốt.",
    income: "Tiền đến từ dự án, môi giới cửa, đa kênh. Không chốt kỳ hạn thì nguồn lệch không thành sổ.",
    career: "Bạn hợp việc xoay cửa, không hợp ngồi một tuyến cố định. Cầm việc bằng hai cửa có điểm chốt, neo một nghĩa vụ chính.",
    risk: "Săn cơ không sổ làm mất chữ tín. Nhiều option khiến không cam kết được cửa đang đòi độc.",
    recommendation: "Giữ tối đa hai cửa lệch, mỗi cửa có hạn chốt. Neo một trục chính để cửa lệch không nuốt lịch.",
  },
  "Chính Tài": {
    insight: "Giá trị của bạn đến từ nguồn có phép: trách nhiệm, hợp đồng, hạn mức rõ.",
    capability: "Bạn chịu được nghĩa vụ nguồn vừa. Bạn giữ sổ được khi hạn mức còn, không khi ôm mọi khoản.",
    income: "Tiền đến theo kế hoạch: lương, hợp đồng, thu-chi có trần. Ôm nợ nghĩa vụ làm kiệt nền.",
    career: "Bạn hợp việc có thu-chi và trách nhiệm nguồn. Cầm việc bằng hạn mức, không bằng nhận mọi sổ.",
    risk: "Biến trách nhiệm thành phải nuôi hết. Sổ quá nền làm thân kiệt trước khi nguồn kịp về.",
    recommendation: "Đặt hạn mức nghĩa vụ nguồn. Tách cam kết việc khỏi việc gánh hết người khác.",
  },
  "Thất Sát": {
    insight: "Giá trị của bạn đến từ chịu được cửa hiểm có hạn: việc khó, hạn ngắn, sức ép không đều.",
    capability: "Bạn bứt được việc người khác né. Bạn đứng được khi có mốc cắt, không khi báo động thành nền.",
    income: "Tiền đến từ cửa rủi có thù lao cao và hạn chót. Đánh đổi sức không kiểm sẽ không giữ được dòng tiền.",
    career: "Bạn hợp việc khủng hoảng, hạn chót, chịu trách nhiệm lệch. Cầm việc khi cửa đang khó, rồi trả quyền khi cửa êm.",
    risk: "Áp không phép thành kiệt. Sống trong báo động làm gãy thân và quan hệ.",
    recommendation: "Đặt mốc cắt cho việc hiểm. Ghép một nhịp dưỡng sau mỗi cửa áp, đừng để sát tự hồi nền.",
  },
  "Chính Quan": {
    insight: "Giá trị của bạn đến từ khung phép và thứ bậc rõ, việc chạy vì có chuẩn.",
    capability: "Bạn chịu được quy trình và vai rõ. Bạn giữ nhịp khi duyệt gọn, không khi thêm tầng cho chắc.",
    income: "Tiền đến theo phép: chức, hợp đồng chuẩn, nguồn được duyệt. Chờ duyệt quá lâu làm lỡ cửa ngắn.",
    career: "Bạn hợp môi trường có cấp bậc và quy trình. Cầm việc bằng một khung gọn, chừa kênh góp ý trong khung.",
    risk: "Khung nuốt sáng kiến. Sợ lệch phép đến mức đứng im khi cửa đang đổi.",
    recommendation: "Dùng một khung phép để chạy việc, không thêm tầng duyệt. Giữ một việc được tự quyết.",
  },
  "Thiên Ấn": {
    insight: "Giá trị của bạn đến từ dưỡng lệch khuôn: kỹ năng không nằm trên chức danh, lối đi ngoài chương chuẩn.",
    capability: "Bạn tự dưỡng được khi khung chính thiếu. Bạn dẫn được người khác bằng lối không theo lề, nếu còn đo được.",
    income: "Tiền đến từ kỹ năng khó ghi bằng. Thiếu bằng chứng nhỏ thì cửa lớn không chốt được thù lao.",
    career: "Bạn hợp vai cố vấn không chức, việc tự học lệch ngành. Cầm việc bằng ghi chép lối lệch, đổi cảm thành một mốc kiểm trước khi quyết lớn.",
    risk: "Dựa chỗ không đo được làm trì quyết. Lối lệch thành bí truyền khiến khó cộng tác.",
    recommendation: "Giữ một kênh dưỡng lệch có ghi. Đổi trực giác thành một bằng chứng nhỏ trước cửa lớn.",
  },
  "Chính Ấn": {
    insight: "Giá trị của bạn đến từ nền có khuôn: ủ được, học có khung, rồi mới bung.",
    capability: "Bạn giữ được chỗ dựa chuẩn. Bạn vững khi được ủ trong chương có hạn, yếu khi bị bọc kín không có điểm ra.",
    income: "Tiền đến chậm: giữ nguồn, ít bung. Ấn che mất cửa lưu thông thì sổ đứng.",
    career: "Bạn hợp môi trường có người nâng và chương chuẩn. Cầm việc bằng ủ có hạn rồi ra một thành phẩm, không ủ mãi.",
    risk: "Bọc kín làm trì. Nền nuốt mất cửa nguồn đang cần chảy.",
    recommendation: "Ủ trong một chương có hạn, rồi phải ra một thành phẩm. Giữ cửa học, mở một cửa lưu thông bắt buộc.",
  },
};

/**
 * Copy published Ten God commercial fields. Empty when the name has no asset.
 */
export function tenGodCommercialAsset(name: string): TenGodCommercialAsset | null {
  const key = name.trim();
  if (!key || key === "Nhật Chủ") return null;
  return ASSETS[key] ?? null;
}
