# Binding Philosophy

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Sprint: Phase X · PX-2

---

## 1. Report is the only truth Portal may read

The Result Page is a consultation surface. Its facts come from Report.

Not from engines.  
Not from pipelines imported into React.  
Not from Knowledge loaders.  
Not from adapter creativity.

---

## 2. Envelope vs aggregate

`CanonicalReportResult` is a pipeline aggregate. Walking it in UI would leak Analysis/Decision/Luck/Interpretation snapshots and layout `module_id`s.

PX-2 therefore binds UI to a sealed **`report.*` presentation envelope**, plus a short list of structural/metadata paths for page state and collapsed technical.

If the envelope is unpublished, the page is empty/partial/error — not a reconstructed calculator.

---

## 3. One path, one owner

Duplicated ownership creates divergent copy.  
Implicit fields create unofficial products.

Every visible content field has exactly one contract path and one component owner.

---

## 4. Formatting is not meaning

Clamp, trim, enum→label, visibility, collapse defaults — allowed.

Scoring, inventing Why, merging domains, translating consulting prose — forbidden.

---

## 5. Chrome is not content

Vietnamese titles and CTA labels are i18n.  
They must not be fetched from Report, and Report prose must not be replaced by i18n.

---

## 6. Artifact is evidence of export, not the page

CanonicalReportArtifact `content` is not the Result Experience.  
Metadata may sit in Chi tiết kỹ thuật.

---

## 7. Stop line

Binding protects the consultant voice by starving the UI of engine insides.

END
