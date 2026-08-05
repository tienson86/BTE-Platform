from pathlib import Path

ROOT = Path("applications/customer_portal/src/components")

def w(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print(path)

# ---- BASE WP02 aliases ----
w("base/Button.tsx", '''
import { BaseButton, type BaseButtonProps } from "./BaseButton";

export type ButtonProps = BaseButtonProps;

/** WP02 Button — wraps BaseButton. Uses Design Tokens via CSS. */
export function Button(props: ButtonProps) {
  return <BaseButton {...props} />;
}
''')

w("base/IconButton.tsx", '''
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
''')

w("base/Card.tsx", '''
import type { ReactNode } from "react";
import { cx } from "../../utils";
import { BaseSurface, type BaseSurfaceProps } from "./BaseSurface";

export type CardProps = BaseSurfaceProps & {
  title?: ReactNode;
  footer?: ReactNode;
};

/** WP02 Card — elevated surface container. */
export function Card({
  title,
  footer,
  children,
  className,
  variant = "section",
  ...rest
}: CardProps) {
  return (
    <BaseSurface
      variant={variant}
      className={cx("cui-card", className)}
      data-elevation="soft"
      {...rest}
    >
      {title ? <div className="cui-card__title">{title}</div> : null}
      <div className="cui-card__body">{children}</div>
      {footer ? <div className="cui-card__footer">{footer}</div> : null}
    </BaseSurface>
  );
}
''')

w("base/Divider.tsx", '''
export { BaseDivider as Divider } from "./BaseDivider";
export type { BaseDividerProps as DividerProps } from "./BaseDivider";
''')

w("base/Badge.tsx", '''
export { BaseBadge as Badge } from "./BaseBadge";
export type { BaseBadgeProps as BadgeProps } from "./BaseBadge";
''')

w("base/Tag.tsx", '''
export { BaseTag as Tag } from "./BaseTag";
export type { BaseTagProps as TagProps } from "./BaseTag";
''')

w("base/Avatar.tsx", '''
export { BaseAvatar as Avatar } from "./BaseAvatar";
export type { BaseAvatarProps as AvatarProps } from "./BaseAvatar";
''')

w("base/Chip.tsx", '''
export { BaseChip as Chip } from "./BaseChip";
export type { BaseChipProps as ChipProps } from "./BaseChip";
''')

# Append exports to base/index.ts — handled separately

# ---- FORMS ----
w("forms/Input.tsx", '''
export { BaseInput as Input } from "../base/BaseInput";
export type { BaseInputProps as InputProps } from "../base/BaseInput";
''')

w("forms/PasswordInput.tsx", '''
import type { InputHTMLAttributes } from "react";
import { cx } from "../../utils";
import { BaseInput } from "../base/BaseInput";

export type PasswordInputProps = Omit<InputHTMLAttributes<HTMLInputElement>, "type"> & {
  invalid?: boolean;
};

/** WP02 PasswordInput. */
export function PasswordInput({ className, invalid = false, ...rest }: PasswordInputProps) {
  return (
    <BaseInput
      type="password"
      autoComplete="current-password"
      invalid={invalid}
      className={cx("cui-password-input", className)}
      {...rest}
    />
  );
}
''')

w("forms/TextArea.tsx", '''
export { BaseTextarea as TextArea } from "../base/BaseTextarea";
export type { BaseTextareaProps as TextAreaProps } from "../base/BaseTextarea";
''')

w("forms/NumberInput.tsx", '''
import type { InputHTMLAttributes } from "react";
import { cx } from "../../utils";
import { BaseInput } from "../base/BaseInput";

export type NumberInputProps = Omit<InputHTMLAttributes<HTMLInputElement>, "type"> & {
  invalid?: boolean;
};

/** WP02 NumberInput. */
export function NumberInput({ className, invalid = false, ...rest }: NumberInputProps) {
  return (
    <BaseInput
      type="number"
      inputMode="decimal"
      invalid={invalid}
      className={cx("cui-number-input", className)}
      {...rest}
    />
  );
}
''')

w("forms/Select.tsx", '''
export { BaseSelect as Select } from "../base/BaseSelect";
export type { BaseSelectProps as SelectProps } from "../base/BaseSelect";
''')

w("forms/MultiSelect.tsx", '''
import type { SelectHTMLAttributes } from "react";
import { cx } from "../../utils";

export type MultiSelectOption = {
  value: string;
  label: string;
  disabled?: boolean;
};

export type MultiSelectProps = Omit<SelectHTMLAttributes<HTMLSelectElement>, "multiple"> & {
  options: MultiSelectOption[];
  invalid?: boolean;
};

/** WP02 MultiSelect — native multiple select (token-styled). */
export function MultiSelect({
  options,
  invalid = false,
  className,
  ...rest
}: MultiSelectProps) {
  return (
    <select
      multiple
      className={cx("cui-base-select", "cui-base-control", "cui-multi-select", className)}
      aria-invalid={invalid || undefined}
      {...rest}
    >
      {options.map((option) => (
        <option key={option.value} value={option.value} disabled={option.disabled}>
          {option.label}
        </option>
      ))}
    </select>
  );
}
''')

w("forms/Checkbox.tsx", '''
export { BaseCheckbox as Checkbox } from "../base/BaseCheckbox";
export type { BaseCheckboxProps as CheckboxProps } from "../base/BaseCheckbox";
''')

w("forms/Radio.tsx", '''
export { BaseRadio as Radio } from "../base/BaseRadio";
export type { BaseRadioProps as RadioProps } from "../base/BaseRadio";
''')

w("forms/Switch.tsx", '''
export { BaseSwitch as Switch } from "../base/BaseSwitch";
export type { BaseSwitchProps as SwitchProps } from "../base/BaseSwitch";
''')

w("forms/DatePicker.tsx", '''
import type { InputHTMLAttributes } from "react";
import { cx } from "../../utils";
import { BaseInput } from "../base/BaseInput";

export type DatePickerProps = Omit<InputHTMLAttributes<HTMLInputElement>, "type"> & {
  invalid?: boolean;
};

/** WP02 DatePicker — native date input, token-styled. */
export function DatePicker({ className, invalid = false, ...rest }: DatePickerProps) {
  return (
    <BaseInput
      type="date"
      invalid={invalid}
      className={cx("cui-date-picker", className)}
      {...rest}
    />
  );
}
''')

w("forms/SearchBox.tsx", '''
export { SearchBar as SearchBox } from "../shared/SearchBar";
export type { SearchBarProps as SearchBoxProps } from "../shared/SearchBar";
''')

w("forms/index.ts", '''
/**
 * WP02 Form Components.
 */

export { Input } from "./Input";
export type { InputProps } from "./Input";

export { PasswordInput } from "./PasswordInput";
export type { PasswordInputProps } from "./PasswordInput";

export { TextArea } from "./TextArea";
export type { TextAreaProps } from "./TextArea";

export { NumberInput } from "./NumberInput";
export type { NumberInputProps } from "./NumberInput";

export { Select } from "./Select";
export type { SelectProps } from "./Select";

export { MultiSelect } from "./MultiSelect";
export type { MultiSelectOption, MultiSelectProps } from "./MultiSelect";

export { Checkbox } from "./Checkbox";
export type { CheckboxProps } from "./Checkbox";

export { Radio } from "./Radio";
export type { RadioProps } from "./Radio";

export { Switch } from "./Switch";
export type { SwitchProps } from "./Switch";

export { DatePicker } from "./DatePicker";
export type { DatePickerProps } from "./DatePicker";

export { SearchBox } from "./SearchBox";
export type { SearchBoxProps } from "./SearchBox";
''')

w("forms/README.md", '''
# Forms Components (WP02)

| Component | Props | Notes |
|-----------|-------|-------|
| Input | BaseInputProps | Text field |
| PasswordInput | PasswordInputProps | type=password |
| TextArea | BaseTextareaProps | Multiline |
| NumberInput | NumberInputProps | type=number |
| Select | BaseSelectProps | Single select |
| MultiSelect | MultiSelectProps | Native multiple |
| Checkbox | BaseCheckboxProps | |
| Radio | BaseRadioProps | |
| Switch | BaseSwitchProps | |
| DatePicker | DatePickerProps | Native date |
| SearchBox | SearchBarProps | Alias of SearchBar |

Example:

```tsx
import { Input, SearchBox } from "@/components/forms";
<Input name="email" />
<SearchBox onSearch={(q) => console.log(q)} />
```
''')

print("forms+base aliases done")
