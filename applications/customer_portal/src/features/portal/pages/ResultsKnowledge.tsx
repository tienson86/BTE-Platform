import { useMemo, useState } from "react";
import type { PortalRoute } from "../chrome/routes";
import { PvBadge, PvButton, PvCard, PvPagination, PvSearch, PvTabs, PvTag } from "../components/primitives";
import { PvEmpty } from "../components/states";

const RESULTS = [
  { id: "1", name: "Nguyễn Văn An", date: "10/08/2026", focus: "Sự nghiệp", status: "Sẵn sàng" },
  { id: "2", name: "Trần Thị Bình", date: "03/08/2026", focus: "Tài chính", status: "Đang hoàn thiện" },
  { id: "3", name: "Lê Minh Châu", date: "01/08/2026", focus: "Quan hệ", status: "Sẵn sàng" },
];

const ARTICLES = [
  { id: "a1", title: "Nhật chủ", category: "Nền tảng", teaser: "Trục nhận diện trong buổi tư vấn.", recommended: true },
  { id: "a2", title: "Ngũ hành cân bằng", category: "Phân tích", teaser: "Đọc lệch–cân mà không biến thành bảng điểm.", recommended: false },
  { id: "a3", title: "Vận trình gần", category: "Định hướng", teaser: "Cách đọc giai đoạn thay vì dự báo tuyệt đối.", recommended: true },
];

export function ResultListPage({ onNavigate }: { onNavigate: (route: PortalRoute) => void }) {
  const [query, setQuery] = useState("");
  const [filter, setFilter] = useState("all");
  const [sort, setSort] = useState("recent");
  const [page, setPage] = useState(1);
  const filtered = useMemo(() => {
    return RESULTS.filter((item) => {
      const matchQuery = item.name.toLowerCase().includes(query.toLowerCase());
      const matchFilter = filter === "all" || item.focus === filter;
      return matchQuery && matchFilter;
    }).sort((a, b) => (sort === "name" ? a.name.localeCompare(b.name, "vi") : 0));
  }, [filter, query, sort]);

  return (
    <section className="pv-page">
      <div className="pv-toolbar">
        <PvSearch label="Tìm kết quả" value={query} placeholder="Tìm theo tên" onChange={setQuery} />
        <PvTabs
          value={filter}
          onChange={setFilter}
          options={[
            { id: "all", label: "Tất cả" },
            { id: "Sự nghiệp", label: "Sự nghiệp" },
            { id: "Tài chính", label: "Tài chính" },
            { id: "Quan hệ", label: "Quan hệ" },
          ]}
        />
        <PvTabs
          value={sort}
          onChange={setSort}
          options={[
            { id: "recent", label: "Mới nhất" },
            { id: "name", label: "Theo tên" },
          ]}
        />
      </div>
      {filtered.length === 0 ? (
        <PvEmpty
          title="Tạo báo cáo đầu tiên"
          body="Chưa có tư vấn nào khớp bộ lọc. Hãy lập phân tích mới hoặc xem lại toàn bộ danh sách."
          actionLabel="Tạo báo cáo đầu tiên"
          onAction={() => onNavigate("analyze")}
        />
      ) : (
        <div className="pv-result-grid">
          {filtered.map((item) => (
            <PvCard
              key={item.id}
              title={
                <>
                  <PvTag>{item.focus}</PvTag>
                  <h3 className="pv-card-title">{item.name}</h3>
                </>
              }
              footer={
                <PvButton variant="secondary" onClick={() => onNavigate("result")}>
                  Mở tư vấn
                </PvButton>
              }
            >
              <p className="pv-note">{item.date}</p>
              <PvBadge tone={item.status === "Sẵn sàng" ? "success" : "warning"}>{item.status}</PvBadge>
            </PvCard>
          ))}
        </div>
      )}
      <PvPagination page={page} total={1} onPage={setPage} />
    </section>
  );
}

export function KnowledgeCenterPage({ onNavigate }: { onNavigate: (route: PortalRoute) => void }) {
  const [query, setQuery] = useState("");
  const [tab, setTab] = useState("recommended");
  const items = ARTICLES.filter((item) => item.title.toLowerCase().includes(query.toLowerCase())).filter((item) =>
    tab === "recommended" ? item.recommended : true,
  );
  return (
    <section className="pv-page">
      <div className="pv-toolbar">
        <PvSearch label="Tìm bài viết" value={query} placeholder="Tìm kiến thức" onChange={setQuery} />
        <PvTabs
          value={tab}
          onChange={setTab}
          options={[
            { id: "recommended", label: "Gợi ý" },
            { id: "all", label: "Tất cả" },
            { id: "recent", label: "Gần đây" },
          ]}
        />
      </div>
      <div className="pv-article-list">
        {items.map((item) => (
          <article key={item.id} className="pv-card pv-article">
            <PvTag>{item.category}</PvTag>
            <h3 className="pv-card-title">{item.title}</h3>
            <p className="pv-prose">{item.teaser}</p>
            <PvButton variant="text" onClick={() => onNavigate("knowledge-article")}>
              Đọc tiếp
            </PvButton>
          </article>
        ))}
      </div>
      <p className="pv-note">Đánh dấu bài viết sẽ có ở phiên sau.</p>
    </section>
  );
}
