/**
 * Static mock data for Desktop Canonical UI (TASK_UI_IMPLEMENTATION_001).
 * Matches CANONICAL_PORTAL_UI_DESKTOP_V1.png — Vietnamese labels only.
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
    title: "S00 - THÔNG TIN BỐI CẢNH",
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
    title: "S01 - THÔNG TIN & ĐỊNH HƯỚNG",
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
    title: "S02 - TỔNG QUAN & HÀNH ĐỘNG",
    subtitle: "TỔNG QUAN LÁ SỐ",
    items: [
      { icon: "fire" as const, label: "Ngũ hành", value: "Hỏa vượng", color: "fire" },
      { icon: "yinyang" as const, label: "Âm dương", value: "Cân bằng", color: "water" },
      { icon: "scale" as const, label: "Thế cục", value: "Trung bình", color: "earth" },
      { icon: "drop" as const, label: "Dụng thần", value: "Thủy", color: "water" },
      { icon: "spark" as const, label: "Hỷ thần", value: "Kim, Thủy", color: "metal" },
      { icon: "leaf" as const, label: "Kỵ thần", value: "Mộc, Hỏa", color: "wood" },
    ],
  },
  s09: {
    title: "S09 - CUNG PHÍ / QUÁI MỆNH & NHÓM TRẠCH",
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
    title: "S03 - TỨ TRỤ - BÁT TỰ",
    pillars: [
      {
        title: "NĂM TRỤ",
        stem: { han: "庚", viet: "Canh", element: "Kim Dương", tone: "metal" },
        branch: { han: "午", viet: "Ngọ", element: "Hỏa Dương", tone: "fire" },
        stamp: "1990",
        highlight: false,
      },
      {
        title: "THÁNG TRỤ",
        stem: { han: "甲", viet: "Giáp", element: "Mộc Dương", tone: "wood" },
        branch: { han: "午", viet: "Ngọ", element: "Hỏa Dương", tone: "fire" },
        stamp: "06",
        highlight: false,
      },
      {
        title: "NGÀY TRỤ (NHẬT CHỦ)",
        stem: { han: "丙", viet: "Bính", element: "Hỏa Dương", tone: "fire" },
        branch: { han: "寅", viet: "Dần", element: "Mộc Dương", tone: "wood" },
        stamp: "25",
        highlight: true,
      },
      {
        title: "GIỜ TRỤ",
        stem: { han: "辛", viet: "Tân", element: "Kim Âm", tone: "metal" },
        branch: { han: "巳", viet: "Tỵ", element: "Hỏa Âm", tone: "fire" },
        stamp: "10:30",
        highlight: false,
      },
    ],
  },
  s04: {
    title: "S04 - CÂN BẰNG NGŨ HÀNH",
    rows: [
      { name: "Mộc", element: "wood" as const, pct: 22, status: "Trung bình" },
      { name: "Hỏa", element: "fire" as const, pct: 42, status: "Rất mạnh" },
      { name: "Thổ", element: "earth" as const, pct: 15, status: "Trung bình" },
      { name: "Kim", element: "metal" as const, pct: 12, status: "Yếu" },
      { name: "Thủy", element: "water" as const, pct: 9, status: "Rất yếu" },
    ],
    summary: "Hỏa vượng • Thủy thiếu • Cân bằng trung bình",
  },
  s05: {
    title: "S05 - SỨC MẠNH MỆNH CỤC",
    scoreLabel: "ĐIỂM SỨC MẠNH",
    score: "72 / 100",
    status: "Mạnh",
    percent: 72,
    evidenceTitle: "BẢNG ĐỘNG CHÍNH",
    evidence: [
      "Nhật chủ Bính Hỏa vượng",
      "Được Mộc sinh trợ",
      "Ngọ Dần hợp Hỏa",
      "Ấn tinh và Tỷ Kiên hỗ trợ",
    ],
    link: "Xem chi tiết phân tích →",
  },
  s10: {
    title: "S10 - CÂN XƯƠNG ĐOÁN MỆNH",
    resultLabel: "KẾT QUẢ CÂN XƯƠNG",
    result: "4 lượng 8 chỉ",
    grade: "Thượng cách",
    stars: 5,
    bullets: [
      "Cân nặng: 4 lượng 8 chỉ",
      "Chủ về: Phú quý, thành đạt",
      "Tính cách: Thông minh, quyết đoán, có chí tiến thủ",
      "Xu hướng: Tự lập, có danh vị và tài lộc",
    ],
    link: "Xem luận giải chi tiết →",
  },
  s06: {
    title: "S06 - THẬP THẦN",
    gods: [
      { name: "Chính Quan", value: "0.8", highlight: false, color: "#1565c0" },
      { name: "Thất Sát", value: "0.6", highlight: false, color: "#6a1b9a" },
      { name: "Chính Ấn", value: "1.2", highlight: true, color: "#ef6c00" },
      { name: "Thiên Ấn", value: "1.3", highlight: true, color: "#f9a825" },
      { name: "Tỷ Kiên", value: "0.9", highlight: false, color: "#6a1b9a" },
      { name: "Kiếp Tài", value: "0.7", highlight: false, color: "#00838f" },
      { name: "Chính Tài", value: "0.6", highlight: false, color: "#2e7d32" },
      { name: "Thiên Tài", value: "0.6", highlight: false, color: "#c62828" },
      { name: "Thực Thần", value: "0.5", highlight: false, color: "#5d4037" },
      { name: "Thương Quan", value: "0.8", highlight: false, color: "#455a64" },
    ],
    link: "Xem chi tiết →",
  },
  s07: {
    title: "S07 - THẦN SÁT",
    categories: [
      { name: "Quý nhân", items: ["Thiên Ất", "Phúc Tinh"] },
      { name: "Cát tinh", items: ["Tương Tinh", "Văn Xương"] },
      { name: "Hung tinh", items: ["Không Vong", "Kiếp Sát"] },
      { name: "Đặc biệt", items: ["Lộc Thần", "Thiên Đức"] },
    ],
    link: "Xem toàn bộ →",
  },
  s08: {
    title: "S08 - LUẬN GIẢI TỔNG HỢP",
    heading: "TỔNG LUẬN",
    body:
      "Bạn là người nhiệt huyết, có khả năng lãnh đạo và truyền cảm hứng. Lá số cho thấy bạn có tiềm năng lớn trong các lĩnh vực sáng tạo, giáo dục, truyền thông và quản trị. Giai đoạn trung vận là thời điểm bứt phá mạnh mẽ nếu biết tận dụng thế mạnh và kiểm soát cảm xúc.",
    cta: "Đọc luận giải chi tiết →",
  },
  s11: {
    title: "S11 - PANEL HỌC TẬP",
    items: [
      { label: "Bài học phù hợp", value: "12 bài" },
      { label: "Thuật ngữ liên quan", value: "25 mục" },
      { label: "Hướng dẫn sử dụng", value: "Xem ngay" },
      { label: "Tài liệu chuyên sâu", value: "8 tài liệu" },
    ],
    link: "Mở học tập →",
  },
  footer:
    "Lưu ý: Thông tin chỉ mang tính tham khảo. Việc luận giải cần dựa trên nhiều yếu tố khác nhau.",
} as const;

export type CanonicalDesktopMock = typeof CANONICAL_DESKTOP_MOCK;
