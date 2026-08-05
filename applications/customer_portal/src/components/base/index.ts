/**
 * Base Component Library — WP-0002.
 * Atomic, token-driven, presentation-only primitives.
 * No business meaning.
 */

export type {
  BaseHeadingLevel,
  BaseSize,
  BaseSpacing,
  BaseSurfaceVariant,
  BaseTextVariant,
  BaseTone,
} from "./types";

export { BaseButton } from "./BaseButton";
export type { BaseButtonProps, BaseButtonVariant } from "./BaseButton";

export { BaseIcon } from "./BaseIcon";
export type { BaseIconProps } from "./BaseIcon";

export { BaseText } from "./BaseText";
export type { BaseTextProps, BaseTextTone } from "./BaseText";

export { BaseHeading } from "./BaseHeading";
export type { BaseHeadingProps } from "./BaseHeading";

export { BaseSurface } from "./BaseSurface";
export type { BaseSurfaceProps } from "./BaseSurface";

export { BaseDivider } from "./BaseDivider";
export type { BaseDividerProps } from "./BaseDivider";

export { BaseBadge } from "./BaseBadge";
export type { BaseBadgeProps } from "./BaseBadge";

export { BaseChip } from "./BaseChip";
export type { BaseChipProps } from "./BaseChip";

export { BaseTag } from "./BaseTag";
export type { BaseTagProps } from "./BaseTag";

export { BaseAvatar } from "./BaseAvatar";
export type { BaseAvatarProps } from "./BaseAvatar";

export { BaseSpinner } from "./BaseSpinner";
export type { BaseSpinnerProps } from "./BaseSpinner";

export { BaseSkeleton } from "./BaseSkeleton";
export type { BaseSkeletonProps } from "./BaseSkeleton";

export { BaseProgress } from "./BaseProgress";
export type { BaseProgressProps } from "./BaseProgress";

export { BaseTooltip } from "./BaseTooltip";
export type { BaseTooltipProps } from "./BaseTooltip";

export { BaseLink } from "./BaseLink";
export type { BaseLinkProps } from "./BaseLink";

export { BaseInput } from "./BaseInput";
export type { BaseInputProps } from "./BaseInput";

export { BaseTextarea } from "./BaseTextarea";
export type { BaseTextareaProps } from "./BaseTextarea";

export { BaseSelect } from "./BaseSelect";
export type { BaseSelectProps } from "./BaseSelect";

export { BaseCheckbox } from "./BaseCheckbox";
export type { BaseCheckboxProps } from "./BaseCheckbox";

export { BaseRadio } from "./BaseRadio";
export type { BaseRadioProps } from "./BaseRadio";

export { BaseSwitch } from "./BaseSwitch";
export type { BaseSwitchProps } from "./BaseSwitch";

export { BaseAlert } from "./BaseAlert";
export type { BaseAlertProps } from "./BaseAlert";

export { BaseCallout } from "./BaseCallout";
export type { BaseCalloutProps } from "./BaseCallout";

export { BaseEmptyState } from "./BaseEmptyState";
export type { BaseEmptyStateProps } from "./BaseEmptyState";

export { BaseErrorState } from "./BaseErrorState";
export type { BaseErrorStateProps } from "./BaseErrorState";

export { BaseUnavailableState } from "./BaseUnavailableState";
export type { BaseUnavailableStateProps } from "./BaseUnavailableState";

export { BaseLoadingState } from "./BaseLoadingState";
export type { BaseLoadingStateProps } from "./BaseLoadingState";

export { BaseScrollArea } from "./BaseScrollArea";
export type { BaseScrollAreaProps } from "./BaseScrollArea";

export { BaseContainer } from "./BaseContainer";
export type { BaseContainerProps, BaseContainerWidth } from "./BaseContainer";

export { BaseStack } from "./BaseStack";
export type { BaseStackProps } from "./BaseStack";

export { BaseGrid } from "./BaseGrid";
export type { BaseGridColumns, BaseGridProps } from "./BaseGrid";

/* WP02 public aliases — prefer these names in new Portal UI. */
export { Button } from "./Button";
export type { ButtonProps } from "./Button";

export { IconButton } from "./IconButton";
export type { IconButtonProps } from "./IconButton";

export { Card } from "./Card";
export type { CardProps } from "./Card";

export { Divider } from "./Divider";
export type { DividerProps } from "./Divider";

export { Badge } from "./Badge";
export type { BadgeProps } from "./Badge";

export { Tag } from "./Tag";
export type { TagProps } from "./Tag";

export { Avatar } from "./Avatar";
export type { AvatarProps } from "./Avatar";

export { Chip } from "./Chip";
export type { ChipProps } from "./Chip";
