import type { MarriageReportDto, MarriageViewModel } from "../marriage_consulting/types";

export type BusinessScoreGroup = {
  key: string;
  title: string;
  configured_weight: number;
  effective_weight: number;
  score: number | null;
  contribution: number;
  confidence: number;
  scored_rows: number;
  total_rows: number;
  explanation: string;
};

export type BusinessScoreAudit = {
  model_version: string;
  score: number | null;
  coverage: number;
  confidence: number;
  provisional: boolean;
  recommendation_key: string;
  recommendation: string;
  advice: string;
  reasons: string[];
  groups: BusinessScoreGroup[];
  methodology: string;
  disclaimer: string;
};

export type BusinessReportDto = MarriageReportDto & { business_score?: BusinessScoreAudit | null };
export type BusinessViewModel = MarriageViewModel & { businessScore: BusinessScoreAudit | null };
