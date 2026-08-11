# BLINDING_RULES

Automated blinding check **fails** if an Expert-B packet contains any of:

- expert_a
- expert_a_label
- expert_a_rationale
- expert_a_evidence
- adjudication
- runtime_score
- runtime_band
- future_taxonomy
- T1, T2, T3, T4, T5, T6

Check must run **before** Expert-B packet release.
