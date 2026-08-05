import type { ReactNode } from "react";
import { IconButton } from "../../components/base/IconButton";
import { SearchBox } from "../../components/forms/SearchBox";
import { Topbar } from "../../components/navigation/Topbar";
import { useTheme } from "../../theme";
import { cx } from "../../utils";

export type HeaderProps = {
  brand?: ReactNode;
  userLabel?: string;
  onMenuClick?: () => void;
  showMenuButton?: boolean;
  className?: string;
};

/** Application header — logo, search placeholder, theme, user (WP03). */
export function Header({
  brand = "BTE",
  userLabel = "Người dùng",
  onMenuClick,
  showMenuButton = false,
  className,
}: HeaderProps): ReactNode {
  const { mode, toggleMode } = useTheme();

  return (
    <Topbar
      className={cx("cui-app-header", className)}
      role="banner"
      brand={
        <a className="cui-app-header__brand" href="/dashboard">
          {brand}
        </a>
      }
      start={
        showMenuButton ? (
          <IconButton
            label="Mở menu điều hướng"
            icon={<span aria-hidden="true">☰</span>}
            onClick={onMenuClick}
          />
        ) : null
      }
      end={
        <div className="cui-app-header__actions">
          <div className="cui-app-header__search">
            <SearchBox
              id="app-header-search"
              placeholder="Tìm kiếm…"
              submitLabel="Tìm"
              aria-label="Tìm kiếm (placeholder)"
            />
          </div>
          <IconButton
            label="Thông báo"
            icon={<span aria-hidden="true">🔔</span>}
          />
          <IconButton
            label={mode === "dark" ? "Chuyển sang giao diện sáng" : "Chuyển sang giao diện tối"}
            icon={<span aria-hidden="true">{mode === "dark" ? "☀" : "☾"}</span>}
            onClick={toggleMode}
          />
          <button type="button" className="cui-app-header__user" aria-haspopup="menu">
            {userLabel}
          </button>
        </div>
      }
    />
  );
}
