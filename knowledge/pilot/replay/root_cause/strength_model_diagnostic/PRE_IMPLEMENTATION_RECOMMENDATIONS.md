# PRE_IMPLEMENTATION_RECOMMENDATIONS

**Sprint:** PILOT-1H

## MUST_HAVE_BEFORE_IMPLEMENTATION

- Additional real dual-reviewed cases across missing levels (esp. VERY_WEAK, WEAK, BALANCED, STRONG/VERY_STRONG)
- Evidence/profile audit published as design contract (this sprint starts it)
- Score collision analysis maintained as living set
- Boundary evidence with expert agreement (not synthetic alone)
- Confidence model design (conflict, completeness, calendar, boundary proximity)
- Taxonomy coverage gates (≥ dual-reviewed per level before freezing T1–T6)

## SHOULD_HAVE

- Expose raw_total / unclamped diagnostics in pilot tooling (not production retune)
- Sitting-branch / hidden pressure evidence design
- Separate support_state vs pressure_state vectors
- Synthetic expectation review pass (mark only; do not silently edit)

## OPTIONAL

- Richer combination/clash design notes
- Temperature source unification design
- Follow-pattern handoff contract with Pattern Engine

## DO_NOT_DO_YET

- Threshold tuning
- Score weight tuning
- Engine rewrite
- Production taxonomy v2
- Golden Dataset promotion of synthetic or provisional labels
- Freezing T1–T6
- Treating synthetic expectations as expert truth
