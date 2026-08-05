import { BaseButton, type BaseButtonProps } from "./BaseButton";

export type ButtonProps = BaseButtonProps;

/** WP02 Button — wraps BaseButton. Uses Design Tokens via CSS. */
export function Button(props: ButtonProps) {
  return <BaseButton {...props} />;
}
