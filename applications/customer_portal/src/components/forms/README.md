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
