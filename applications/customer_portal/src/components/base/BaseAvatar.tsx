import type { HTMLAttributes, ReactNode } from "react";
import { cx } from "../../utils";
import type { BaseSize } from "./types";

export type BaseAvatarProps = HTMLAttributes<HTMLSpanElement> & {
  size?: BaseSize;
  src?: string;
  alt?: string;
  initials?: string;
  children?: ReactNode;
};

/** Primitive avatar. Image or initials fallback. */
export function BaseAvatar({
  size = "md",
  src,
  alt = "",
  initials,
  className,
  children,
  ...rest
}: BaseAvatarProps) {
  return (
    <span className={cx("cui-base-avatar", className)} data-size={size} {...rest}>
      {src ? <img src={src} alt={alt} /> : children ?? initials ?? null}
    </span>
  );
}
