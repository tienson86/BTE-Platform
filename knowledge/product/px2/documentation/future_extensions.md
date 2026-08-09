# Future Extensions

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Sprint: Phase X · PX-2

---

## 1. Not this sprint

- Portal / React / CSS implementation  
- Publishing `CanonicalReportResult.presentation` from Report Engine  
- PACK_06/07 layout reorder  
- Offline / print / export UX beyond reserved states  
- Additional locales  

---

## 2. Likely next product steps

| Candidate | Intent |
|-----------|--------|
| Report presentation publisher | Fill `report.*` envelope from Report (still no Portal engine imports) |
| PX-3 implementation map | Bind Portal to this contract without token invention |
| Streaming partial bind | Independent section `loading` (today forbidden) |

Report publisher is a **Report** sprint, not a silent adapter reconstruction.

---

## 3. Extension rules

1. New visible field → catalog row + owner + mapping file  
2. Still one contract path  
3. Still Vietnamese chrome via i18n  
4. Still no Analysis/Decision/Luck/Interpretation in React  
5. Still no Artifact content as the page  

---

## 4. Open questions (do not block PX-2)

- Exact Report publisher shape vs `presentation` name  
- Whether warnings get a quiet “none” line later (PX-2: hide)  
- Secondary CTA verb lock to a Capability id  

---

## 5. Stop line

PX-2 is complete as specification. Implementation waits for authorization.

END
