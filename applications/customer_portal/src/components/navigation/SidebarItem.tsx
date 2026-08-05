import type { AnchorHTMLAttributes, ButtonHTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";

type Common = {
  label: ReactNode;
  active?: boolean;
  icon?: ReactNode;
  className?: string;
};

export type SidebarItemLinkProps = Common &
  AnchorHTMLAttributes<HTMLAnchorElement> & { href: string };

export type SidebarItemButtonProps = Common &
  ButtonHTMLAttributes<HTMLButtonElement> & { href?: undefined };

export type SidebarItemProps = SidebarItemLinkProps | SidebarItemButtonProps;

/** WP02 SidebarItem — nav row for sidebar/rail. */
export function SidebarItem(props: SidebarItemProps) {
  const { label, active = false, icon, className } = props;
  const classes = cx("cui-sidebar-item", className);
  if ("href" in props && props.href !== undefined) {
    const { href, label: _l, active: _a, icon: _i, className: _c, ...rest } = props;
    return (
      <a
        href={href}
        className={classes}
        data-active={active || undefined}
        aria-current={active ? "page" : undefined}
        {...rest}
      >
        {icon}
        <span>{label}</span>
      </a>
    );
  }
  const { label: _l2, active: _a2, icon: _i2, className: _c2, ...buttonRest } =
    props as SidebarItemButtonProps;
  return (
    <button
      type="button"
      className={classes}
      data-active={active || undefined}
      aria-current={active ? "page" : undefined}
      {...buttonRest}
    >
      {icon}
      <span>{label}</span>
    </button>
  );
}
