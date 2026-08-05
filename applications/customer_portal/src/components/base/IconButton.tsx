import type { ReactNode } from "react";
import { cx } from "../../utils";
import { BaseButton, type BaseButtonProps } from "./BaseButton";
import { BaseIcon } from "./BaseIcon";

export type IconButtonProps = Omit<BaseButtonProps, "children"> & {
  label: string;
  icon: ReactNode;
};

/** WP02 IconButton — icon-only action control. */
export function IconButton({
  label,
  icon,
  className,
  variant = "ghost",
  size = "md",
  ...rest
}: IconButtonProps) {
  return (
    <BaseButton
      variant={variant}
      size={size}
      className={cx("cui-icon-button", className)}
      aria-label={label}
      title={label}
      {...rest}
    >
      <BaseIcon size={size} label={label}>
        {icon}
      </BaseIcon>
    </BaseButton>
  );
}
