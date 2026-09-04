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

export type TenGodCombinationCatalogEntry = {
  readonly members: readonly string[];
  readonly title: string;
};

const COMBOS: Readonly<Record<string, TenGodCombinationAsset>> = {
  "Tỷ Kiên|Thực Thần": {
    title: "Tự gánh phần mình và ra thành phẩm rõ",
    insight:
      "Bạn tạo giá trị khi giữ đúng khối việc của mình và biến sức làm thành sản phẩm người khác nhận được.",
    capability:
      "Bạn vừa đứng được phần riêng, vừa chốt được đầu ra. Thiếu hạn chót thì phần việc rõ vẫn chưa thành hàng.",
    income:
      "Tiền đến khi công đổi thành thù lao: sản phẩm, dịch vụ, buổi giao việc. Làm hết phần mà không giữ nguồn thì dòng tiền mỏng.",
    career:
      "Bạn hợp nhóm ngang hàng có đầu ra cụ thể. Ngồi họp dài hoặc hòa hết vào quỹ chung làm chậm nhịp ra hàng.",
    leadership:
      "Cầm việc bằng chia phần trước, rồi chốt một thành phẩm. Không nuốt hết quyết định của người cùng vai.",
    growth:
      "Mở rộng khi một thành phẩm đã có thù lao. Ôm thêm phần trước khi ra hàng làm loãng sức.",
    risk:
      "So phần với đồng sự. Tự làm hết việc ngoài vai. Bung sức trước khi tiền về.",
    recommendation:
      "Chốt phần việc trước khi chung quỹ. Mỗi đợt chỉ ra một thành phẩm có hạn.",
  },
  "Tỷ Kiên|Chính Tài": {
    title: "Giữ phần việc rõ và nguồn tiền có hạn mức",
    insight:
      "Bạn tạo giá trị khi tự đứng phần mình và chịu được nghĩa vụ nguồn vừa, không chờ được bọc.",
    capability:
      "Bạn giữ ranh việc và hạn mức thu-chi. Bạn yếu khi hòa hết vào quỹ chung hoặc nhận mọi khoản.",
    income:
      "Tiền đến khi đổi công đúng phần, theo hợp đồng và trần rõ. Ủy thác hết đáy nguồn hoặc ôm nợ nghĩa vụ làm dòng tiền đứng.",
    career:
      "Bạn hợp việc có vai ngang và trách nhiệm nguồn. Không hợp môi trường nuốt quyết định hoặc bắt nuôi hết người khác.",
    leadership:
      "Cầm việc bằng chia phần và hạn mức. Không nhận mọi sổ chỉ vì thấy mình chịu được.",
    growth:
      "Tăng quy mô khi phần việc và trần nguồn còn khớp. Thêm nghĩa vụ trước khi có quỹ dự phòng sẽ kiệt sức.",
    risk:
      "So phần, lập phe, biến trách nhiệm thành phải nuôi hết.",
    recommendation:
      "Chốt phần việc trước khi chung quỹ. Đặt hạn mức nghĩa vụ nguồn và giữ một quỹ không đụng.",
  },
  "Kiếp Tài|Thương Quan": {
    title: "Gỡ chỗ kẹt bằng tốc độ và phản biện",
    insight:
      "Bạn tạo giá trị khi thấy quy trình đang giả ổn và chớp đúng lúc nguồn sắp khép.",
    capability:
      "Bạn vừa phản xạ nhanh, vừa dám chất vấn chỗ lệch. Thiếu bản thay thì tốc độ chỉ phá việc đang chạy.",
    income:
      "Tiền đến từ gỡ nút cổ chai và hoa hồng ngắn. Đụng cấp giữ phép hoặc sống bằng nhịp báo động sẽ làm nguồn đứng.",
    career:
      "Bạn hợp việc rà soát luồng, mở hướng khi chỗ cũ kẹt. Môi trường thứ bậc cứng và giữ sổ dài sẽ chặn bạn.",
    leadership:
      "Cầm việc bằng một bản thay tối thiểu, ghi phần trước khi tranh. Trả lại nhịp khi việc đã thông.",
    growth:
      "Nhân bản khi một vòng sửa đã chạy. Phá thêm tầng trước khi chốt sẽ mất chữ tín.",
    risk:
      "Hớt phần đồng sự. Phá chuẩn trước khi có chuẩn thay. Không còn quỹ dự phòng.",
    recommendation:
      "Đưa phản biện vào kênh có người nhận. Dùng tốc độ để mở đường, giữ một quỹ không đụng.",
  },
  "Kiếp Tài|Thiên Tài": {
    title: "Xoay nguồn nhanh, không phụ thuộc một kênh",
    insight:
      "Bạn tạo giá trị khi chớp nguồn ngắn và giữ thêm kênh phụ lúc kênh chính đang kẹt.",
    capability:
      "Bạn thấy cơ hội ngoài hợp đồng thẳng và phản xạ trước khi nguồn khép. Thiếu hạn chốt thì nhiều kênh không thành thu nhập.",
    income:
      "Tiền đến từ hoa hồng nhanh, dự án, đa kênh. Giữ quỹ chung dễ bị xóa vì tranh phần; không chốt kỳ hạn thì nguồn phụ không vào sổ thu.",
    career:
      "Bạn hợp việc xoay kênh, tranh nhịp ngắn. Ngồi một tuyến cố định và giữ sổ dài làm lãng phí tốc độ.",
    leadership:
      "Cầm việc bằng tối đa hai kênh phụ có hạn chốt, neo một nghĩa vụ chính. Ghi phần trước khi tranh.",
    growth:
      "Mở thêm kênh khi một kênh đã chốt thù lao. Nhân bản nhịp ngắn khi chưa có quỹ sẽ mất nền tảng.",
    risk:
      "Săn cơ không cam kết. Hớt phần. Nhiều hướng khiến không giữ được chữ tín.",
    recommendation:
      "Giữ tối đa hai kênh phụ, mỗi kênh một kỳ hạn. Neo một trục chính. Giữ một quỹ không đụng.",
  },
  "Kiếp Tài|Thất Sát": {
    title: "Chớp việc khó đúng lúc nguồn đang kẹt",
    insight:
      "Bạn tạo giá trị khi chịu được hạn chót và phản xạ nhanh lúc nguồn sắp hết, rồi trả phần cho người giữ sổ thu.",
    capability:
      "Bạn vừa đứng được việc người khác né, vừa bứt nhịp ngắn. Thiếu mốc cắt thì báo động thành nhịp sống.",
    income:
      "Tiền đến từ việc rủi có hạn và hoa hồng nhanh. Sống bằng báo động sẽ không giữ được quỹ.",
    career:
      "Bạn hợp việc khủng hoảng, hạn ngắn, tranh nhịp. Việc giữ sổ dài làm lãng phí tốc độ.",
    leadership:
      "Cầm việc khi việc đang khó. Ghi phần trước khi tranh. Trả lại quyền điều phối khi việc đã êm.",
    growth:
      "Giữ nhịp nghỉ sau mỗi đợt áp lực. Nhân bản việc ngắn khi chưa có quỹ sẽ xóa sổ thu.",
    risk:
      "Áp lực thành nền tảng. Hớt phần đồng sự làm mất chữ tín. Không còn quỹ dự phòng.",
    recommendation:
      "Đặt mốc cắt cho việc khó. Dùng tốc độ để mở đường, giữ một quỹ không đụng.",
  },
  "Thực Thần|Thương Quan": {
    title: "Ra sản phẩm và chỉ ra chỗ hệ thống đang giả ổn",
    insight:
      "Bạn tạo giá trị khi đổi tay nghề thành đầu ra thấy được, đồng thời thấy lỗ quy trình mà người trong cuộc không nói.",
    capability:
      "Bạn vừa ra hàng, vừa chất vấn chỗ lệch. Thiếu bản thay thì phản biện làm gãy việc đang chạy.",
    income:
      "Tiền đến từ sản phẩm, dịch vụ và gỡ nút cổ chai. Lời nhiều hơn hàng, hoặc phá chuẩn trước khi có chuẩn thay, làm khách chờ.",
    career:
      "Bạn hợp việc kỹ thuật có đầu ra và rà soát luồng. Môi trường cấm chất vấn sẽ chặn cả hai thế mạnh.",
    leadership:
      "Cầm việc bằng chốt thành phẩm và một bản thay tối thiểu. Không xé quy trình công.",
    growth:
      "Nâng quy mô khi một thành phẩm và một vòng sửa đã chạy. Bung thêm ý trước khi ra hàng làm loãng nguồn.",
    risk:
      "Phá chuẩn chưa có cái thay. Xả sức trước khi tiền về. Lời sắc làm gãy quan hệ với người đang giữ việc.",
    recommendation:
      "Mỗi đợt một thành phẩm có hạn. Chỉ sửa khi đã có bản thay tối thiểu và người nhận phản biện.",
  },
  "Thực Thần|Thiên Tài": {
    title: "Biến cơ hội không cố định thành sản phẩm có hạn",
    insight:
      "Bạn tạo giá trị khi bắt một cơ hội không nằm trên hợp đồng thẳng và đóng nó thành sản phẩm người khác nhận được.",
    capability:
      "Bạn vừa thấy kênh phụ, vừa đưa tay nghề thành đầu ra có hạn. Thiếu chốt thì cơ hội chỉ còn là ý.",
    income:
      "Tiền đến khi dự án phụ được đóng thành hàng, buổi, gói có thù lao. Để việc mở hoài thì không thành thu nhập.",
    career:
      "Bạn hợp việc dự án, đa kênh có đầu ra. Ngồi một tuyến cố định làm lãng phí phản xạ cơ hội.",
    leadership:
      "Cầm việc bằng hai hướng có hạn chốt, neo một nghĩa vụ chính. Không bung mọi ý cùng lúc.",
    growth:
      "Mở rộng khi một sản phẩm đã chốt thù lao. Thêm hướng mới trước khi ra hàng làm loãng nguồn.",
    risk:
      "Săn cơ không ra hàng. Xả sức trên việc không đo được làm mỏng nền tảng trước khi tiền về.",
    recommendation:
      "Giữ tối đa hai hướng phụ. Mỗi hướng phải có một thành phẩm và một kỳ hạn chốt.",
  },
  "Thực Thần|Chính Tài": {
    title: "Đổi tay nghề thành thu nhập có kế hoạch",
    insight:
      "Bạn tạo giá trị khi biến sức làm thành sản phẩm thấy được, rồi thu theo hợp đồng và hạn mức rõ.",
    capability:
      "Bạn ra hàng được và chịu được nghĩa vụ nguồn vừa. Bạn yếu khi làm không giữ nguồn, hoặc ôm mọi khoản.",
    income:
      "Tiền đến từ hàng, dịch vụ, lương và hợp đồng có trần. Bung hết sức trước khi nguồn về, hoặc ôm nợ nghĩa vụ, làm dòng tiền mỏng.",
    career:
      "Bạn hợp việc kỹ thuật, sản phẩm, thu-chi có trách nhiệm. Không hợp nhận mọi sổ hoặc họp dài không chốt hàng.",
    leadership:
      "Cầm việc bằng chốt thành phẩm và hạn mức nguồn. Tách cam kết việc khỏi việc gánh hết người khác.",
    growth:
      "Tăng quy mô khi một sản phẩm đã có thù lao và trần nguồn còn khớp. Thêm nghĩa vụ trước khi có quỹ sẽ kiệt sức.",
    risk:
      "Làm không giữ nguồn. Biến trách nhiệm thành phải nuôi hết. Sổ thu quá sức trước khi tiền kịp về.",
    recommendation:
      "Chốt một sản phẩm có hạn mỗi đợt. Đặt hạn mức nghĩa vụ nguồn. Giữ nhịp nghỉ sau khi ra hàng.",
  },
  "Thực Thần|Chính Quan": {
    title: "Làm ra hàng trong môi trường có quy trình",
    insight:
      "Bạn tạo giá trị khi đổi tay nghề thành đầu ra, và việc chạy được vì có chuẩn, vai rõ.",
    capability:
      "Bạn chịu được quy trình và vẫn chốt được thành phẩm. Thiếu điểm tự quyết thì chuẩn nuốt mất nhịp ra hàng.",
    income:
      "Tiền đến theo sản phẩm được duyệt, chức, hợp đồng chuẩn. Chờ duyệt quá lâu hoặc họp dài làm lỡ nhịp thị trường.",
    career:
      "Bạn hợp tổ chức có cấp bậc và đầu ra cụ thể. Cấm tự quyết một việc nhỏ sẽ làm bạn chậm.",
    leadership:
      "Cầm việc bằng một quy trình gọn và một thành phẩm mỗi đợt. Không thêm tầng duyệt cho chắc.",
    growth:
      "Leo bậc khi một thành phẩm đã được nhận. Thêm tầng duyệt trước khi ra hàng làm chậm sổ thu.",
    risk:
      "Chuẩn nuốt sáng kiến. Sợ lệch phép đến mức đứng im khi việc đang đổi.",
    recommendation:
      "Giữ một việc được tự quyết. Mỗi đợt ra một thành phẩm, không thêm tầng duyệt.",
  },
  "Thực Thần|Thiên Ấn": {
    title: "Đưa kỹ năng riêng thành việc người khác dùng được",
    insight:
      "Bạn tạo giá trị khi kỹ năng không nằm trên chức danh được đóng thành sản phẩm, buổi, gói người khác nhận được.",
    capability:
      "Bạn tự bồi dưỡng khi tổ chức chính thiếu, rồi vẫn ra được đầu ra. Thiếu bằng chứng nhỏ thì kỹ năng riêng khó chốt thù lao.",
    income:
      "Tiền đến từ tay nghề và kỹ năng khó ghi bằng. Làm không giữ nguồn, hoặc không có bằng chứng, thì thù lao không chốt được.",
    career:
      "Bạn hợp việc kỹ thuật, cố vấn không chức, chuyển nghề thành hàng có hạn. Ngồi ghế chuẩn mà không ra sản phẩm làm lãng phí.",
    leadership:
      "Cầm việc bằng ghi chép kỹ năng riêng, đổi cảm thành một mốc kiểm, rồi chốt thành phẩm.",
    growth:
      "Nâng quy mô khi đã có một bằng chứng nhỏ và một thành phẩm. Ủ mãi không ra hàng làm chậm thu.",
    risk:
      "Dựa chỗ không đo được. Kỹ năng riêng thành bí truyền, khó cộng tác. Xả sức trước khi tiền về.",
    recommendation:
      "Giữ một kênh bồi dưỡng có ghi. Mỗi đợt đổi trực giác thành một bằng chứng nhỏ và một thành phẩm.",
  },
  "Thực Thần|Thương Quan|Chính Quan": {
    title: "Ra sản phẩm, phản biện, vẫn chạy được trong tổ chức",
    insight:
      "Bạn tạo giá trị khi làm ra hàng, chỉ ra chỗ quy trình giả ổn, và vẫn giữ việc chạy trong môi trường có cấp bậc.",
    capability:
      "Bạn vừa ra đầu ra, vừa chất vấn, vừa chịu được chuẩn. Thiếu bản thay hoặc thiếu một việc tự quyết thì hoặc phá tổ chức, hoặc bị chuẩn nuốt.",
    income:
      "Tiền đến từ sản phẩm được nhận, gỡ nút cổ chai, và nguồn được duyệt. Chờ duyệt quá lâu hoặc phá trước khi có cái thay sẽ làm nguồn đứng.",
    career:
      "Bạn hợp việc có đầu ra trong tổ chức, rà soát luồng, cải tiến quy trình. Cấm phản biện hoặc cấm ra hàng đều làm lệch mô hình.",
    leadership:
      "Cầm việc bằng một thành phẩm, một bản thay tối thiểu, một quy trình gọn. Không thêm tầng duyệt. Không xé việc công.",
    growth:
      "Nâng quy mô khi một vòng ra hàng và một vòng sửa đã chạy. Thêm tầng trước khi chốt sẽ mất chữ tín.",
    risk:
      "Phá chuẩn chưa có cái thay. Chuẩn nuốt sáng kiến. Lời sắc làm gãy quan hệ với người đang giữ việc.",
    recommendation:
      "Giữ một việc tự quyết. Mỗi đợt một thành phẩm và một bản thay tối thiểu, đưa vào kênh có người nhận.",
  },
  "Thương Quan|Thiên Tài": {
    title: "Sửa quy trình kém và mở kênh phụ",
    insight:
      "Bạn tạo giá trị khi thấy lỗ hệ thống và giữ một hướng ngoài tuyến đang kẹt.",
    capability:
      "Bạn vừa chất vấn quy trình giả ổn, vừa giữ hướng phụ ngoài hợp đồng thẳng.",
    income:
      "Tiền đến từ gỡ nút cổ chai và kênh phụ. Đụng cấp giữ phép hoặc không chốt hạn thì nguồn đứng.",
    career:
      "Bạn hợp việc rà soát luồng, mở kênh mới. Môi trường thứ bậc cứng sẽ chặn phản biện.",
    leadership:
      "Cầm việc bằng bản thay tối thiểu trước khi phá. Giữ một neo chính để hướng phụ không nuốt lịch.",
    growth:
      "Nâng quy mô khi bản thay đã chạy một vòng. Phá thêm tầng trước khi chốt sẽ mất chữ tín.",
    risk:
      "Phá quy trình trước khi có bản thay. Nhiều hướng khiến không cam kết được việc đang đòi tập trung.",
    recommendation:
      "Đưa phản biện vào kênh có người nhận. Mỗi hướng phụ phải có hạn chốt.",
  },
  "Thiên Tài|Chính Tài": {
    title: "Giữ nguồn chính, vẫn chốt được cơ hội phụ",
    insight:
      "Bạn tạo giá trị khi chịu được nguồn có phép, đồng thời không bỏ kênh phụ lúc kênh chính đang chậm.",
    capability:
      "Bạn giữ sổ thu có hạn mức và vẫn thấy nguồn ngoài hợp đồng thẳng. Thiếu hạn chốt thì kênh phụ phá kế hoạch.",
    income:
      "Tiền đến theo lương, hợp đồng, và dự án phụ có kỳ hạn. Ôm nợ nghĩa vụ hoặc săn cơ không chốt đều làm dòng tiền lệch.",
    career:
      "Bạn hợp việc có thu-chi rõ, kèm dự án. Ngồi một tuyến cố định sẽ lãng phí kênh phụ; nhận mọi sổ sẽ kiệt sức.",
    leadership:
      "Cầm việc bằng hạn mức nguồn chính và tối đa hai kênh phụ có hạn chốt.",
    growth:
      "Mở kênh phụ khi nguồn chính còn trần. Thêm nghĩa vụ trước khi có quỹ sẽ kiệt nền tảng.",
    risk:
      "Biến trách nhiệm thành phải nuôi hết. Nhiều hướng phụ khiến không cam kết được việc đang đòi độc.",
    recommendation:
      "Neo một nguồn chính có trần. Giữ tối đa hai kênh phụ, mỗi kênh một kỳ hạn. Tách cam kết việc khỏi gánh hết người khác.",
  },
  "Chính Tài|Chính Quan": {
    title: "Chạy nguồn tiền trong tổ chức có chuẩn",
    insight:
      "Bạn tạo giá trị khi nguồn đi theo hợp đồng, hạn mức, và việc chạy vì có vai, có duyệt.",
    capability:
      "Bạn chịu được nghĩa vụ nguồn vừa và quy trình. Bạn yếu khi ôm mọi khoản hoặc thêm tầng duyệt cho chắc.",
    income:
      "Tiền đến theo phép: lương, hợp đồng chuẩn, nguồn được duyệt. Chờ duyệt quá lâu hoặc ôm nợ nghĩa vụ làm lỡ nhịp.",
    career:
      "Bạn hợp môi trường có cấp bậc, thu-chi, trách nhiệm nguồn. Không hợp nhận mọi sổ hoặc việc không có chuẩn.",
    leadership:
      "Cầm việc bằng hạn mức và một quy trình gọn. Giữ một việc được tự quyết. Không thêm tầng duyệt.",
    growth:
      "Leo bậc khi một khoản nguồn đã chạy đúng trần. Thêm nghĩa vụ hoặc thêm tầng duyệt sẽ làm chậm thu.",
    risk:
      "Chuẩn nuốt sáng kiến. Biến trách nhiệm thành phải nuôi hết. Sợ lệch phép đến mức đứng im.",
    recommendation:
      "Đặt hạn mức nghĩa vụ nguồn. Dùng một quy trình gọn. Giữ một việc tự quyết.",
  },
  "Chính Tài|Chính Ấn": {
    title: "Nuôi nguồn ổn định nhờ nền tảng có kỷ luật",
    insight:
      "Bạn tạo giá trị khi nguồn đi theo kế hoạch, và có chỗ tích lũy, học có hạn, rồi mới bung.",
    capability:
      "Bạn giữ sổ thu có trần và chỗ dựa có chuẩn. Bạn yếu khi ủ mãi không ra, hoặc ôm mọi khoản.",
    income:
      "Tiền đến chậm: lương, hợp đồng, giữ nguồn. Ủ quá lâu hoặc ôm nợ nghĩa vụ thì sổ thu đứng.",
    career:
      "Bạn hợp môi trường có người nâng, chương chuẩn, trách nhiệm nguồn. Việc mở ngắn sẽ làm bạn chậm hơn nhịp thị trường.",
    leadership:
      "Cầm việc bằng hạn mức, ủ có hạn, rồi ra một thành phẩm. Không ủ mãi. Không nhận mọi sổ.",
    growth:
      "Tăng quy mô khi một thành phẩm đã ra và trần nguồn còn khớp. Ủ thêm chương trước khi mở việc làm chậm thu.",
    risk:
      "Nền tảng che mất việc đang cần chạy. Biến trách nhiệm thành phải nuôi hết.",
    recommendation:
      "Ủ trong một chương có hạn, rồi phải ra một thành phẩm. Đặt hạn mức nghĩa vụ nguồn.",
  },
  "Thất Sát|Thiên Ấn": {
    title: "Gánh việc áp lực bằng kỹ năng khó chuẩn hóa",
    insight:
      "Bạn tạo giá trị khi chịu được việc khó, hạn ngắn, và đi bằng kỹ năng không nằm trên chức danh.",
    capability:
      "Bạn bứt việc người khác né, rồi tự bồi dưỡng khi tổ chức chính thiếu. Thiếu mốc cắt thì báo động thành nhịp sống.",
    income:
      "Tiền đến từ việc rủi có thù lao cao và kỹ năng khó ghi bằng. Không có bằng chứng nhỏ thì việc lớn không chốt thù lao.",
    career:
      "Bạn hợp việc hạn chót, chịu trách nhiệm lệch, cố vấn không chức. Ngồi ghế chuẩn và giữ sổ dài làm chậm phản xạ.",
    leadership:
      "Cầm việc khi việc đang khó, đổi cảm thành một mốc kiểm, rồi trả lại quyền điều phối khi việc đã êm.",
    growth:
      "Nâng việc khi đã có mốc cắt và một bằng chứng nhỏ. Nhân báo động trước khi bồi dưỡng sẽ kiệt sức.",
    risk:
      "Sống trong báo động. Kỹ năng riêng không đo được khiến khó cộng tác. Áp lực không phép thành kiệt.",
    recommendation:
      "Đặt mốc cắt cho việc khó. Ghi một bằng chứng nhỏ trước mỗi việc lớn. Ghép một nhịp nghỉ sau mỗi đợt áp lực.",
  },
  "Chính Quan|Chính Ấn": {
    title: "Làm việc có chuẩn, có chỗ tích lũy trước khi bung",
    insight:
      "Bạn tạo giá trị khi việc chạy vì có chuẩn, và có chỗ ủ có hạn trước khi bung.",
    capability:
      "Bạn chịu được quy trình và chỗ dựa có kỷ luật. Thiếu điểm ra thì chuẩn thành bọc kín.",
    income:
      "Tiền đến theo phép và chậm: duyệt, chức, nguồn được nâng. Chờ quá lâu hoặc ủ mãi thì sổ thu đứng.",
    career:
      "Bạn hợp môi trường có cấp bậc và chương chuẩn. Việc mở ngắn sẽ làm bạn chậm hơn nhịp thị trường.",
    leadership:
      "Cầm việc bằng một quy trình gọn, ủ có hạn, rồi ra một thành phẩm. Không thêm tầng duyệt.",
    growth:
      "Leo bậc khi một thành phẩm đã ra. Ủ thêm chương trước khi mở việc làm chậm thu.",
    risk:
      "Chuẩn nuốt sáng kiến. Nền tảng che mất việc đang cần chạy.",
    recommendation:
      "Giữ một việc được tự quyết. Ủ trong chương có hạn, rồi phải mở một hướng lưu thông.",
  },
  "Kiếp Tài|Thất Sát|Thiên Ấn": {
    title: "Gánh việc khó theo cách linh hoạt, có điểm dừng",
    insight:
      "Bạn tạo giá trị khi chịu được việc khó, phản ứng đúng lúc nguồn kẹt, và dùng kỹ năng không nằm trên chức danh.",
    capability:
      "Bạn bứt việc người khác né, chớp nhịp ngắn, rồi tự bồi dưỡng khi tổ chức chính thiếu. Thiếu mốc cắt thì báo động thành nhịp sống.",
    income:
      "Tiền đến từ việc rủi, hoa hồng nhanh, và kỹ năng khó ghi bằng. Không có bằng chứng nhỏ thì việc lớn không chốt thù lao.",
    career:
      "Bạn hợp việc hạn chót, tranh nhịp, cố vấn lệch ngành. Ngồi ghế chuẩn và giữ sổ dài làm chậm phản xạ.",
    leadership:
      "Cầm việc khi việc đang khó, ghi phần trước khi tranh, đổi cảm thành một mốc kiểm rồi trả lại quyền điều phối khi việc đã êm.",
    growth:
      "Nâng việc khi đã có mốc cắt và một bằng chứng nhỏ. Nhân báo động trước khi bồi dưỡng sẽ kiệt sức.",
    risk:
      "Sống trong báo động. Hớt phần làm mất chữ tín. Cách làm riêng không đo được khiến khó cộng tác.",
    recommendation:
      "Đặt mốc cắt cho việc khó. Giữ một quỹ không đụng. Ghi một bằng chứng nhỏ trước mỗi việc lớn.",
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
 * Published combination library. Lookup only. Does not calculate Ten Gods.
 */
export function listTenGodCombinationCatalog(): readonly TenGodCombinationCatalogEntry[] {
  return Object.keys(COMBOS).map((key) => ({
    members: key.split("|"),
    title: COMBOS[key]?.title ?? "",
  }));
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
    "Phần ẩn giữ cơ hội phụ và chỗ tích lũy. Đó là nền tảng, chưa phải cách bạn đang kiếm tiền.",
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
