import type { ReactNode } from "react";
import { IconButton } from "../../components/base/IconButton";
import { Topbar } from "../../components/navigation/Topbar";
import { useTheme } from "../../theme";
import { cx } from "../../utils";
import { PrimaryNav } from "../Navigation/PrimaryNav";

export type HeaderProps = {
  brand?: ReactNode;
  userLabel?: string;
  activeNavId?: string;
  onMenuClick?: () => void;
  showMenuButton?: boolean;
  className?: string;
};

/**
 * Canonical application header — brand, primary nav, theme, user.
 * Design System / Topbar API unchanged.
 */
export function Header({
  brand = "BTE Portal",
  userLabel = "Người dùng",
  activeNavId,
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
            label="Mở mục lục"
            icon={<span aria-hidden="true">☰</span>}
            onClick={onMenuClick}
          />
        ) : null
      }
      end={
        <div className="cui-app-header__actions">
          <IconButton
            label={
              mode === "dark"
                ? "Chuyển sang giao diện sáng"
                : "Chuyển sang giao diện tối"
            }
            icon={<span aria-hidden="true">{mode === "dark" ? "☀" : "☾"}</span>}
            onClick={toggleMode}
          />
          <button
            type="button"
            className="cui-app-header__user"
            aria-haspopup="menu"
            aria-label={userLabel}
            title={userLabel}
          >
            <span className="cui-app-header__avatar" aria-hidden="true">
              {(userLabel.trim().split(/\s+/).pop() ?? "U").charAt(0).toUpperCase()}
            </span>
            <span className="cui-app-header__user-label">{userLabel}</span>
          </button>
        </div>
      }
    >
      <PrimaryNav activeId={activeNavId} />
    </Topbar>
  );
}
