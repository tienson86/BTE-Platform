/**
 * Static fixture for Desktop Canonical UI (preview / tests / S10 fallback).
 * Runtime SSOT is AnalyzeService → canonicalDesktopAdapter (POST /analyze).
 */

export const CANONICAL_DESKTOP_MOCK = {
  header: {
    brand: "BTE Portal",
    nav: [
      { id: "home", label: "Trang chủ", active: false },
      { id: "analysis", label: "Luận giải", active: false },
      { id: "result", label: "Kết quả", active: true },
      { id: "report", label: "Báo cáo", active: false },
      { id: "history", label: "Lịch sử", active: false },
      { id: "account", label: "Tài khoản", active: false },
      { id: "guide", label: "Hướng dẫn", active: false },
    ],
    user: { initials: "NV", name: "Nguyễn Văn A", role: "Thành viên" },
    notifications: 3,
  },
  sidebar: {
    brand: "BTE Portal",
    groups: [
      {
        title: "PHÂN TÍCH LÁ SỐ",
        items: [
          { id: "tom-tat", label: "Tóm tắt", icon: "home", active: true },
          { id: "bat-tu", label: "Bát Tự", icon: "scroll", active: false },
          { id: "bieu-do", label: "Biểu đồ", icon: "chart", active: false },
          { id: "phan-tich", label: "Phân tích", icon: "search", active: false },
          { id: "luan-giai", label: "Luận giải", icon: "chat", active: false },
          { id: "kien-thuc", label: "Kiến thức", icon: "book", active: false },
        ],
      },
      {
        title: "TIỆN ÍCH",
        items: [
          { id: "so-sanh", label: "So sánh lá số", icon: "compare", active: false },
          { id: "luu-tru", label: "Lưu trữ", icon: "folder", active: false },
          { id: "xuat", label: "Xuất báo cáo", icon: "export", active: false },
        ],
      },
    ],
    themeLabel: "CHẾ ĐỘ GIAO DIỆN",
    themeValue: "Sáng",
    version: "BTE Platform v1.0.0",
    copyright: "© 2024 BTE Platform",
  },
  s00: {
    title: "THÔNG TIN BỐI CẢNH",
    profile: {
      label: "HỒ SƠ",
      name: "Nguyễn Văn A",
      genderSymbol: "♂",
      meta: "Nam • Dương Nam",
      profileLink: "Xem hồ sơ đầy đủ →",
    },
    birth: {
      label: "NGÀY GIỜ SINH",
      date: "15/08/1990",
      lunar: "(25/06 Canh Ngọ)",
      time: "10:30 (GMT+7)",
    },
    chartId: {
      label: "MÃ LÁ SỐ",
      value: "BTE-2024-000123",
    },
    version: {
      label: "PHIÊN BẢN",
      value: "v1.0.0",
      system: "BTE System",
    },
    analyzedAt: {
      label: "THỜI GIAN PHÂN TÍCH",
      value: "20/05/2024 14:30:25",
      relative: "2 phút trước",
    },
    status: {
      label: "TRẠNG THÁI",
      value: "Hoàn tất",
      shareLink: "Chia sẻ lá số →",
    },
  },
  s01: {
    title: "THÔNG TIN ĐỊNH HƯỚNG",
    identityTitle: "THÔNG TIN BẢN MỆNH",
    dayMaster: {
      label: "Nhật chủ",
      value: "Bính Hỏa",
      subtype: "Dương Hỏa",
      tags: [
        { text: "Hỏa vượng", tone: "danger" as const },
        { text: "Tính cách: Nhiệt huyết", tone: "neutral" as const },
      ],
    },
    conditions: {
      title: "ĐIỀU KIỆN MỆNH CỤC",
      rows: [
        { label: "Mùa sinh", value: "Hạ (Tháng Ngọ)", tag: "Hỏa vượng", tone: "danger" as const },
        { label: "Cục mệnh", value: "Hỏa Lục Cục", tag: "Trung bình", tone: "warning" as const },
        { label: "Thân cư", value: "Tài Bạch", tag: "Tốt", tone: "success" as const },
      ],
    },
    decisionTitle: "ĐỊNH HƯỚNG CUỘC ĐỜI",
    decisions: [
      {
        icon: "target" as const,
        question: "BẠN LÀ AI?",
        answer:
          "Người nhiệt huyết, chủ động, có khả năng lãnh đạo và tinh thần cống hiến.",
      },
      {
        icon: "bulb" as const,
        question: "THẾ MẠNH CỦA BẠN?",
        answer:
          "Hỏa vượng giúp bạn quyết đoán, sáng tạo, truyền cảm hứng và có khả năng bứt phá.",
      },
      {
        icon: "compass" as const,
        question: "BẠN NÊN LÀM GÌ?",
        answer:
          "Phát huy khả năng lãnh đạo, ưu tiên lĩnh vực liên quan đến sáng tạo, truyền thông, giáo dục...",
      },
    ],
    cta: "Xem luận giải chi tiết →",
  },
  s02: {
    title: "TỔNG QUAN LÁ SỐ",
    items: [
      { icon: "fire" as const, label: "Phân bố Ngũ hành", value: "Mộc 4 · Hỏa 5 · Thổ 6 · Kim 3 · Thủy 1", color: "earth" },
      { icon: "yinyang" as const, label: "Âm dương", value: "Cân bằng", color: "water" },
      { icon: "scale" as const, label: "Thế cục", value: "Trung bình", color: "earth" },
      { icon: "drop" as const, label: "Dụng thần", value: "Thủy", color: "water" },
      { icon: "spark" as const, label: "Hỷ thần", value: "Kim, Thủy", color: "metal" },
      { icon: "leaf" as const, label: "Kỵ thần", value: "Mộc, Hỏa", color: "wood" },
    ],
  },
  s09: {
    title: "CUNG PHI - MỆNH QUÁI - NHÓM TRẠCH",
    quai: {
      center: "Ly Hỏa",
      number: "9",
      bullets: [
        "Cung mệnh: Ly Hỏa",
        "Đông tứ mệnh",
        "Hợp hướng: Đông, Đông Nam, Nam, Bắc",
        "Kỵ hướng: Tây, Tây Bắc, Tây Nam, Đông Bắc",
      ],
    },
    nhomTrachTitle: "NHÓM TRẠCH HỢP",
    nhomTrach: [
      { icon: "home" as const, label: "Nhà ở", color: "purple" },
      { icon: "briefcase" as const, label: "Văn phòng", color: "green" },
      { icon: "compass" as const, label: "Hướng tốt", color: "teal" },
      { icon: "palette" as const, label: "Màu sắc", color: "orange" },
      { icon: "grid" as const, label: "Số hợp", color: "blue" },
    ],
  },
  s03: {
    title: "TỨ TRỤ - BÁT TỰ",
    pillars: [
      {
        title: "NĂM TRỤ",
        stem: { han: "庚", viet: "Canh", element: "Kim Dương", tone: "metal" },
        branch: { han: "午", viet: "Ngọ", element: "Hỏa Dương", tone: "fire" },
        stamp: "1990",
        highlight: false,
        tenGod: "",
        hiddenLines: [] as string[],
      },
      {
        title: "THÁNG TRỤ",
        stem: { han: "甲", viet: "Giáp", element: "Mộc Dương", tone: "wood" },
        branch: { han: "午", viet: "Ngọ", element: "Hỏa Dương", tone: "fire" },
        stamp: "06",
        highlight: false,
        tenGod: "",
        hiddenLines: [] as string[],
      },
      {
        title: "NGÀY TRỤ (NHẬT CHỦ)",
        stem: { han: "丙", viet: "Bính", element: "Hỏa Dương", tone: "fire" },
        branch: { han: "寅", viet: "Dần", element: "Mộc Dương", tone: "wood" },
        stamp: "25",
        highlight: true,
        tenGod: "",
        hiddenLines: [] as string[],
      },
      {
        title: "GIỜ TRỤ",
        stem: { han: "辛", viet: "Tân", element: "Kim Âm", tone: "metal" },
        branch: { han: "巳", viet: "Tỵ", element: "Hỏa Âm", tone: "fire" },
        stamp: "10:30",
        highlight: false,
        tenGod: "",
        hiddenLines: [] as string[],
      },
    ],
  },
  s04: {
    title: "PHÂN BỐ NGŨ HÀNH",
    rows: [
      { name: "Mộc", element: "wood" as const, pct: 21, count: 4, status: "" },
      { name: "Hỏa", element: "fire" as const, pct: 26, count: 5, status: "" },
      { name: "Thổ", element: "earth" as const, pct: 32, count: 6, status: "" },
      { name: "Kim", element: "metal" as const, pct: 16, count: 3, status: "" },
      { name: "Thủy", element: "water" as const, pct: 5, count: 1, status: "" },
    ],
    summary: "Tính theo Thiên can · bản hành Địa chi · Tàng can. Tổng đơn vị cấu trúc: 19",
  },
  s05: {
    title: "MỆNH CỤC",
    level: "MẠNH",
    score: "82 / 100",
    percent: 82,
    insight: "Mệnh cục cân bằng tốt.\nNhật chủ được sinh trợ.",
    factors: [
      { text: "Nhật chủ đắc lệnh", tone: "positive" as const },
      { text: "Được Mộc sinh trợ", tone: "positive" as const },
      { text: "Hỏa vượng", tone: "neutral" as const },
      { text: "Kim suy", tone: "negative" as const },
    ],
    cta: "Xem phân tích chi tiết →",
  },
  s10: {
    title: "CÂN XƯƠNG ĐOÁN MỆNH",
    stars: 5,
    weight: "4 LƯỢNG 3 CHỈ",
    grade: "MỆNH TỐT",
    insight: "Thuộc nhóm có hậu vận ổn định.",
    verse: {
      title: "📜 BÀI CA CÂN XƯƠNG",
      lines: [
        "Thân mang phúc khí trời ban,",
        "Công danh thuận lợi, gia an cửa nhà.",
        "Trung vận vững vàng tích lũy,",
        "Hậu vận an hòa, phúc lộc thêm hoa.",
      ],
    },
    interpretation: {
      title: "📖 LUẬN GIẢI",
      body:
        "Bạn là người có số mệnh khá tốt. Tiền vận có thể gặp thử thách, nhưng trung vận và hậu vận ổn định, dễ tích lũy thành quả nếu kiên trì.",
    },
    link: "Đọc luận giải đầy đủ →",
  },
  s06: {
    title: "CÁC THẬP THẦN",
    gods: [
      { name: "Chính Quan", short: "Ch.Quan", score: "0.8", color: "#1565c0" },
      { name: "Thất Sát", short: "Th.Sát", score: "0.6", color: "#6a1b9a" },
      { name: "Chính Ấn", short: "Ch.Ấn", score: "1.2", color: "#ef6c00" },
      { name: "Thiên Ấn", short: "Th.Ấn", score: "1.3", color: "#f9a825" },
      { name: "Chính Tài", short: "Ch.Tài", score: "0.6", color: "#2e7d32" },
      { name: "Thiên Tài", short: "Th.Tài", score: "0.6", color: "#c62828" },
      { name: "Thực Thần", short: "Th.Thần", score: "0.5", color: "#5d4037" },
      { name: "Thương Quan", short: "Th.Quan", score: "0.8", color: "#455a64" },
      { name: "Tỷ Kiên", short: "Tỷ.Kiên", score: "0.9", color: "#7b1fa2" },
      { name: "Kiếp Tài", short: "Ki.Tài", score: "0.7", color: "#00838f" },
    ],
    link: "Xem chi tiết →",
    visibleLabel: "Lộ can",
    hiddenLabel: "Tàng can",
    note: "Xác định theo quan hệ Ngũ hành và âm dương với Nhật chủ.",
    hiddenGods: [] as Array<{
      name: string;
      short: string;
      score: string;
      color: string;
    }>,
  },
  s07: {
    title: "THẦN SÁT",
    executive: {
      line1: "Có 10 Thần Sát được kích hoạt",
      line2: "5 Cát tinh • 5 Hung tinh",
    },
    good: {
      title: "● CÁT TINH (5)",
      items: [
        "Thiên Ất Quý Nhân",
        "Thiên Đức Quý Nhân",
        "Nguyệt Đức Quý Nhân",
        "Văn Xương",
        "Hoa Cái",
      ],
    },
    bad: {
      title: "● HUNG TINH (5)",
      items: ["Kiếp Sát", "Không Vong", "Cô Thần", "Quả Tú", "Đại Hao"],
    },
    footerSummary: {
      line1: "Có 5 Cát tinh và 5 Hung tinh.",
      line2: "Nên xem chi tiết để đánh giá mức độ ảnh hưởng.",
    },
    link: "Xem toàn bộ →",
  },
  s08: {
    title: "LUẬN GIẢI TỔNG THỂ",
    executive: {
      title: "TỔNG QUAN LUẬN GIẢI",
      body:
        "Bạn là người có tố chất lãnh đạo, quyết đoán và khả năng truyền cảm hứng. Mệnh cục thiên về Hỏa nên hành động mạnh mẽ, nhưng cần cân bằng cảm xúc và sự kiên nhẫn để phát huy ổn định.",
    },
    strengths: {
      title: "🟢 ĐIỂM MẠNH",
      items: [
        "Khả năng lãnh đạo",
        "Quyết đoán",
        "Ý chí mạnh",
        "Có trách nhiệm",
      ],
    },
    warnings: {
      title: "🟠 CẦN LƯU Ý",
      items: ["Hỏa quá vượng", "Thiếu Thủy", "Dễ nóng vội", "Thiếu kiên nhẫn"],
    },
    actions: {
      title: "🔵 GỢI Ý HÀNH ĐỘNG",
      items: [
        "Phát triển vai trò quản lý",
        "Bổ sung yếu tố Thủy",
        "Làm việc theo nhóm",
        "Kiểm soát cảm xúc",
      ],
    },
    link: "Đọc luận giải đầy đủ →",
  },
  s11: {
    title: "BÁO CÁO TỔNG KẾT",
    executive: {
      title: "KẾT LUẬN TỔNG QUAN",
      body:
        "Bạn có nền tảng mệnh cục khá tốt. Khả năng phát triển ổn định nếu phát huy năng lực lãnh đạo và duy trì sự cân bằng cảm xúc.",
    },
    strengths: {
      title: "✓ ĐIỂM MẠNH",
      items: ["Lãnh đạo", "Quyết đoán", "Trách nhiệm", "Học hỏi nhanh"],
    },
    attention: {
      title: "⚠ ĐIỂM CẦN LƯU Ý",
      items: ["Dễ nóng vội", "Thiếu kiên nhẫn", "Cần cân bằng Ngũ hành"],
    },
    recommendations: {
      title: "➜ KHUYẾN NGHỊ HÀNH ĐỘNG",
      items: [
        "Phát triển vai trò quản lý",
        "Bổ sung yếu tố Thủy",
        "Lựa chọn hướng làm việc phù hợp",
        "Kiểm soát cảm xúc khi ra quyết định",
      ],
    },
    link: "Xem báo cáo phân tích đầy đủ →",
  },
  footer:
    "Lưu ý: Thông tin chỉ mang tính tham khảo. Việc luận giải cần dựa trên nhiều yếu tố khác nhau.",
} as const;

export type CanonicalDesktopMock = typeof CANONICAL_DESKTOP_MOCK;
