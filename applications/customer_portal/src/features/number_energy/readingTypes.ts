export type NumberEnergyPairChip = {
  pair_digits: string;
  display_name: string;
  energy_id?: string;
  kind?: string;
  expression?: string;
  force_label?: string;
  force_level?: number;
};

export type NumberEnergyGroup = {
  energy_id?: string;
  display_name: string;
  pairs: string[];
  meaning?: string;
  strength?: string;
  watchout?: string;
  kind?: string;
};

export type NumberEnergyTriplet = {
  digits: string;
  left_name: string;
  right_name: string;
  left_pair?: string;
  right_pair?: string;
};

export type NumberEnergyDominant = {
  display_name: string;
  pairs?: string[];
  count?: number;
};

export type NumberEnergyEnding = {
  pair_digits: string | null;
  display_name: string | null;
  kind?: string;
  note?: string;
};

export type NumberEnergyReading = {
  layout?: string;
  version?: string;
  display_number?: string;
  analyzed_number?: string;
  leading_zero?: boolean;
  leading_zero_note?: string | null;
  interior_zero_note?: string | null;
  pairs?: NumberEnergyPairChip[];
  groups?: NumberEnergyGroup[];
  triplets?: NumberEnergyTriplet[];
  dominant?: NumberEnergyDominant | null;
  ending?: NumberEnergyEnding | null;
  supportive_group_count?: number;
  challenging_group_count?: number;
  supportive_balance_note?: string;
  consecutive_challenging_note?: string | null;
  lifted?: boolean;
  lifted_note?: string | null;
  force_notes?: string[];
  summary?: string;
  notices?: string[];
  purpose_note?: string | null;
  cccd_note?: string | null;
  incomplete?: boolean;
};
