import type { ReactNode } from "react";
import { StatCard } from "../../components/display/StatCard";
import type { DashboardStat } from "./mockData";

export type StatisticsSectionProps = {
  stats: readonly DashboardStat[];
};

/** Dashboard statistics cards (WP04). */
export function StatisticsSection({ stats }: StatisticsSectionProps): ReactNode {
  return (
    <section className="cui-dashboard__grid" aria-label="Thống kê tổng quan">
      {stats.map((stat) => (
        <StatCard
          key={stat.id}
          label={stat.label}
          value={stat.value}
          hint={stat.hint}
        />
      ))}
    </section>
  );
}
