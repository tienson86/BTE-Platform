import type { FormEvent, InputHTMLAttributes, ReactNode } from "react";
import { BaseButton, BaseInput } from "../base";
import { cx } from "../../utils";

export type SearchBarProps = Omit<InputHTMLAttributes<HTMLInputElement>, "type"> & {
  onSearch?: (value: string) => void;
  submitLabel?: ReactNode;
};

/** Shared search bar. Emits presentation callbacks only. */
export function SearchBar({
  onSearch,
  submitLabel = "Search",
  className,
  id = "shared-search",
  ...rest
}: SearchBarProps) {
  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const value = String(data.get(id) ?? "");
    onSearch?.(value);
  };

  return (
    <form className={cx("cui-shared-search-bar", className)} onSubmit={handleSubmit} role="search">
      <BaseInput id={id} name={id} type="search" aria-label="Search" {...rest} />
      <BaseButton type="submit">{submitLabel}</BaseButton>
    </form>
  );
}
