/** Inline SVG icons for Desktop Canonical UI — no external icon package. */

import type { ReactNode } from "react";

type IconProps = { className?: string; size?: number; color?: string };

function Svg({
  className,
  size = 18,
  color = "currentColor",
  children,
  viewBox = "0 0 24 24",
}: IconProps & { children: ReactNode; viewBox?: string }): ReactNode {
  return (
    <svg
      className={className}
      width={size}
      height={size}
      viewBox={viewBox}
      fill="none"
      stroke={color}
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {children}
    </svg>
  );
}

export function IconMenu(props: IconProps): ReactNode {
  return (
    <Svg {...props}>
      <path d="M4 7h16M4 12h16M4 17h16" />
    </Svg>
  );
}

export function IconSun(props: IconProps): ReactNode {
  return (
    <Svg {...props}>
      <circle cx="12" cy="12" r="4" />
      <path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
    </Svg>
  );
}

export function IconBell(props: IconProps): ReactNode {
  return (
    <Svg {...props}>
      <path d="M6 9a6 6 0 0 1 12 0c0 7 3 7 3 7H3s3 0 3-7" />
      <path d="M10 19a2 2 0 0 0 4 0" />
    </Svg>
  );
}

export function IconHome(props: IconProps): ReactNode {
  return (
    <Svg {...props}>
      <path d="M3 11.5 12 4l9 7.5" />
      <path d="M6 10.5V20h12v-9.5" />
    </Svg>
  );
}

export function IconScroll(props: IconProps): ReactNode {
  return (
    <Svg {...props}>
      <path d="M7 4h9a3 3 0 0 1 3 3v11a2 2 0 0 1-2 2H8a3 3 0 0 1-3-3V7a3 3 0 0 1 2-2.8" />
      <path d="M8 8h8M8 12h8M8 16h5" />
    </Svg>
  );
}

export function IconChart(props: IconProps): ReactNode {
  return (
    <Svg {...props}>
      <path d="M4 19V5M4 19h16" />
      <path d="M8 15v-4M12 15V8M16 15v-6" />
    </Svg>
  );
}

export function IconSearchDoc(props: IconProps): ReactNode {
  return (
    <Svg {...props}>
      <path d="M8 4h7l3 3v11a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z" />
      <circle cx="12" cy="13" r="2.5" />
      <path d="m14 15 2 2" />
    </Svg>
  );
}

export function IconChat(props: IconProps): ReactNode {
  return (
    <Svg {...props}>
      <path d="M5 6h14v9H9l-4 3V6z" />
      <path d="M8 10h8M8 13h5" />
    </Svg>
  );
}

export function IconBook(props: IconProps): ReactNode {
  return (
    <Svg {...props}>
      <path d="M5 5.5A2.5 2.5 0 0 1 7.5 3H19v16H7.5A2.5 2.5 0 0 0 5 21.5V5.5z" />
      <path d="M5 18.5A2.5 2.5 0 0 1 7.5 16H19" />
    </Svg>
  );
}

export function IconCompare(props: IconProps): ReactNode {
  return (
    <Svg {...props}>
      <circle cx="9" cy="12" r="5" />
      <circle cx="15" cy="12" r="5" />
    </Svg>
  );
}

export function IconFolder(props: IconProps): ReactNode {
  return (
    <Svg {...props}>
      <path d="M3 8h6l2 2h10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8z" />
    </Svg>
  );
}

export function IconExport(props: IconProps): ReactNode {
  return (
    <Svg {...props}>
      <path d="M12 15V5M8 9l4-4 4 4" />
      <path d="M5 19h14" />
    </Svg>
  );
}

export function IconCalendar(props: IconProps): ReactNode {
  return (
    <Svg {...props} size={props.size ?? 14}>
      <rect x="4" y="6" width="16" height="14" rx="2" />
      <path d="M8 4v4M16 4v4M4 10h16" />
    </Svg>
  );
}

export function IconClock(props: IconProps): ReactNode {
  return (
    <Svg {...props} size={props.size ?? 14}>
      <circle cx="12" cy="12" r="8" />
      <path d="M12 8v5l3 2" />
    </Svg>
  );
}

export function IconCopy(props: IconProps): ReactNode {
  return (
    <Svg {...props} size={props.size ?? 14}>
      <rect x="8" y="8" width="11" height="11" rx="2" />
      <path d="M5 15V6a2 2 0 0 1 2-2h9" />
    </Svg>
  );
}

export function IconUser(props: IconProps): ReactNode {
  return (
    <Svg {...props} size={props.size ?? 28} color="#fff">
      <circle cx="12" cy="9" r="3.5" fill="currentColor" stroke="none" />
      <path d="M5 19c1.5-3.5 4-5 7-5s5.5 1.5 7 5" fill="currentColor" stroke="none" />
    </Svg>
  );
}

export function IconFire(props: IconProps): ReactNode {
  return (
    <Svg {...props} size={props.size ?? 22}>
      <path d="M12 3c2 3 1 5 1 5s3-1 4 3a5 5 0 1 1-10 0c1-3 3-5 5-8z" />
    </Svg>
  );
}

export function IconTarget(props: IconProps): ReactNode {
  return (
    <Svg {...props} size={props.size ?? 16}>
      <circle cx="12" cy="12" r="8" />
      <circle cx="12" cy="12" r="4" />
      <circle cx="12" cy="12" r="1.5" fill="currentColor" stroke="none" />
    </Svg>
  );
}

export function IconBulb(props: IconProps): ReactNode {
  return (
    <Svg {...props} size={props.size ?? 16}>
      <path d="M9 18h6M10 21h4" />
      <path d="M8 14a5 5 0 1 1 8 0c-.8.9-1.5 1.6-1.5 3h-5c0-1.4-.7-2.1-1.5-3z" />
    </Svg>
  );
}

export function IconCompass(props: IconProps): ReactNode {
  return (
    <Svg {...props} size={props.size ?? 16}>
      <circle cx="12" cy="12" r="8" />
      <path d="m14.5 9.5-2 5-5-2 5-2 2-1z" />
    </Svg>
  );
}

export function IconYinYang(props: IconProps): ReactNode {
  return (
    <Svg {...props} size={props.size ?? 22}>
      <circle cx="12" cy="12" r="8" />
      <path d="M12 4a4 4 0 0 1 0 8 4 4 0 0 0 0 8" />
      <circle cx="12" cy="8" r="1" fill="currentColor" stroke="none" />
      <circle cx="12" cy="16" r="1" fill="currentColor" stroke="none" />
    </Svg>
  );
}

export function IconScale(props: IconProps): ReactNode {
  return (
    <Svg {...props} size={props.size ?? 22}>
      <path d="M12 4v16M6 8h12" />
      <path d="M6 8 3.5 14h5L6 8zM18 8l-2.5 6h5L18 8z" />
    </Svg>
  );
}

export function IconDrop(props: IconProps): ReactNode {
  return (
    <Svg {...props} size={props.size ?? 22}>
      <path d="M12 4c3 4 6 7 6 10a6 6 0 1 1-12 0c0-3 3-6 6-10z" />
    </Svg>
  );
}

export function IconSpark(props: IconProps): ReactNode {
  return (
    <Svg {...props} size={props.size ?? 22}>
      <path d="M12 3l1.5 5.5L19 10l-5.5 1.5L12 17l-1.5-5.5L5 10l5.5-1.5L12 3z" />
    </Svg>
  );
}

export function IconLeaf(props: IconProps): ReactNode {
  return (
    <Svg {...props} size={props.size ?? 22}>
      <path d="M5 19c8-1 13-6 14-14-8 1-13 6-14 14z" />
      <path d="M8 16c2-2 5-5 8-7" />
    </Svg>
  );
}

export function IconBriefcase(props: IconProps): ReactNode {
  return (
    <Svg {...props} size={props.size ?? 18} color="#fff">
      <rect x="4" y="8" width="16" height="11" rx="2" />
      <path d="M9 8V6a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2" />
    </Svg>
  );
}

export function IconPalette(props: IconProps): ReactNode {
  return (
    <Svg {...props} size={props.size ?? 18} color="#fff">
      <path d="M12 4a8 8 0 1 0 0 16h1.5a2.5 2.5 0 0 0 0-5H12" />
      <circle cx="8" cy="10" r="1" fill="currentColor" stroke="none" />
      <circle cx="11" cy="7.5" r="1" fill="currentColor" stroke="none" />
      <circle cx="15" cy="8.5" r="1" fill="currentColor" stroke="none" />
    </Svg>
  );
}

export function IconGrid(props: IconProps): ReactNode {
  return (
    <Svg {...props} size={props.size ?? 18} color="#fff">
      <rect x="4" y="4" width="6" height="6" rx="1" />
      <rect x="14" y="4" width="6" height="6" rx="1" />
      <rect x="4" y="14" width="6" height="6" rx="1" />
      <rect x="14" y="14" width="6" height="6" rx="1" />
    </Svg>
  );
}

export function IconDoc(props: IconProps): ReactNode {
  return (
    <Svg {...props} size={props.size ?? 16}>
      <path d="M8 4h6l4 4v10a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z" />
      <path d="M14 4v4h4M9 13h6M9 16h4" />
    </Svg>
  );
}

export function IconStarLogo(props: IconProps): ReactNode {
  return (
    <svg
      className={props.className}
      width={props.size ?? 28}
      height={props.size ?? 28}
      viewBox="0 0 32 32"
      aria-hidden="true"
    >
      <polygon
        points="16,2 18.5,11 28,11 20.5,16.5 23,26 16,20.5 9,26 11.5,16.5 4,11 13.5,11"
        fill="#e8c56a"
        stroke="#f5dfa0"
        strokeWidth="0.5"
      />
    </svg>
  );
}

export function IconPersonMark(props: IconProps): ReactNode {
  return (
    <Svg {...props} size={props.size ?? 18} color="#fff">
      <circle cx="12" cy="9" r="3.2" fill="currentColor" stroke="none" />
      <path d="M6 19c1.2-3 3.5-4.5 6-4.5s4.8 1.5 6 4.5" fill="currentColor" stroke="none" />
    </Svg>
  );
}

const SIDEBAR_ICONS: Record<string, (p: IconProps) => ReactNode> = {
  home: IconHome,
  scroll: IconScroll,
  chart: IconChart,
  search: IconSearchDoc,
  chat: IconChat,
  book: IconBook,
  compare: IconCompare,
  folder: IconFolder,
  export: IconExport,
};

export function SidebarIcon({ name, ...props }: IconProps & { name: string }): ReactNode {
  const Comp = SIDEBAR_ICONS[name] ?? IconHome;
  return <Comp {...props} />;
}
