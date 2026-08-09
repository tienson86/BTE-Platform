# Methodology

Validation methodology: compare `PIPELINE_INDEX.json` to the QC-3 matrix; check each edge’s required contracts ⊆ producer published outputs; confirm consumer version pins; confirm stage order; serialize reports.

Quality methodology: five coverage scores averaged to overall integration.

Integration philosophy: one-way handoff of published contracts; no engine-internal imports across pipelines.
