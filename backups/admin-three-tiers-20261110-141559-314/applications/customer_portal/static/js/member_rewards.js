(function () {
  function node(tag, text, className) {
    const el = document.createElement(tag);
    if (text !== undefined) el.textContent = text;
    if (className) el.className = className;
    return el;
  }
  async function render(id) {
    const host = document.getElementById(id);
    if (!host) return;
    const isSharePage = id === "referralRewards";
    host.hidden = false;
    host.textContent = "Đang tải Linh Thạch…";
    try {
      const data = await BtePortal.get("/api/v1/membership/rewards");
      host.replaceChildren();
      const heading = node("div", undefined, "member-reward-heading");
      const icon = node("img"); icon.src = "/static/images/membership/linh-thach.png";
      icon.alt = "Linh Thạch"; icon.width = 90; icon.height = 90;
      heading.append(icon, node("h2", data.balance + " Linh Thạch"));
      host.append(heading);
      if (data.balance < 0) host.append(node("p", "Phần thưởng đã được thu hồi do hoàn tiền. Linh Thạch tích tiếp theo sẽ bù số dư này."));
      if (isSharePage && data.referral_code) {
        host.append(
          node("h3", "Giới thiệu bạn đồng hành — Cùng nhận ưu đãi"),
          node("p", "Người mua gói lần đầu qua link hoặc mã giới thiệu được giảm 20%."),
          node("p", "Khi admin xác nhận đã thanh toán, bạn nhận 10 / 50 / 100 Linh Thạch tương ứng với gói cấp 1 / 2 / 3."),
          node("p", "Giá sau giảm lần lượt là 551.110 VNĐ, 2.222.222 VNĐ và 10.666.666 VNĐ. Khi giao dịch được ghi nhận hoàn tiền, khoản thưởng tương ứng sẽ được thu hồi.")
        );
        const url = new URL("/membership", data.referral_base_url || window.location.origin);
        url.searchParams.set("ref", data.referral_code);
        const label = node("label", "Link giới thiệu của bạn");
        const input = node("input"); input.readOnly = true; input.value = url.href;
        label.append(input);
        if (["localhost", "127.0.0.1", "[::1]"].includes(url.hostname)) {
          host.append(node("p", "BTE đang dùng địa chỉ nội bộ. Để gửi link cho người khác, quản trị viên cần cấu hình địa chỉ BTE công khai khi hệ thống đã được đưa lên online."));
        }
        const copy = node("button", "Sao chép link"); copy.type = "button";
        const state = node("p"); state.setAttribute("role", "status");
        copy.onclick = async () => {
          try { await navigator.clipboard.writeText(url.href); state.textContent = "Đã sao chép link giới thiệu."; }
          catch (_) { input.focus(); input.select(); state.textContent = "Nhấn Ctrl+C để sao chép link đã chọn."; }
        };
        host.append(label, copy, node("p", "Mã giới thiệu: " + data.referral_code), state);
      } else if (isSharePage) {
        host.append(node("p", "Link giới thiệu được mở khi tài khoản có quyền thành viên còn hiệu lực."));
      }
      host.append(node("h3", "Đổi thêm lượt xem"));
      host.append(node("p", "Mỗi lượt đổi cần 5 Linh Thạch. Dùng hết lượt của mục muốn xem trước khi đổi. Lượt đổi bằng Linh Thạch giữ nguyên số điểm sau khi xem."));
      const items = node("div", undefined, "member-redeem-list");
      data.usage.forEach(item => {
        const row = node("div", undefined, "member-redeem-row");
        row.append(node("span", item.label + " — " + (item.remaining === null ? "không giới hạn" : "còn " + item.remaining + " lượt")));
        const button = node("button", "Đổi 5 Linh Thạch"); button.type = "button";
        button.disabled = !data.referral_code || item.remaining === null || item.remaining > 0 || data.balance < 5;
        const operationKey = window.crypto.randomUUID();
        button.onclick = async () => {
          button.disabled = true;
          try {
            await BtePortal.post("/api/v1/membership/rewards/redeem", {feature: item.feature, operation_key: operationKey});
            await render(id);
          } catch (error) { stateMessage.textContent = error.message; button.disabled = false; }
        };
        row.append(button); items.append(row);
      });
      const stateMessage = node("p"); stateMessage.setAttribute("role", "status");
      host.append(items, stateMessage);
      const history = node("details"), summary = node("summary", "Lịch sử Linh Thạch — tối đa 100 giao dịch gần nhất");
      history.append(summary);
      const list = node("ul");
      data.entries.forEach(entry => list.append(node("li",
        new Date(entry.created_at).toLocaleString("vi-VN") + " · " +
        (entry.delta > 0 ? "+" : "") + entry.delta + " · " + entry.description)));
      if (!data.entries.length) list.append(node("li", "Chưa có giao dịch Linh Thạch."));
      history.append(list); host.append(history);
      host.append(node("p", "Các nội dung học thêm về phong thủy sẽ có mức đổi bằng Linh Thạch riêng khi được công bố."));
    } catch (error) { host.textContent = error.message || "Chưa tải được thông tin Linh Thạch."; }
  }
  window.BteMemberRewards = {render};
  if (document.getElementById("referralRewards")) render("referralRewards");
})();
