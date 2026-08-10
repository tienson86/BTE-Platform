# Issue Triage

Version: 1.0.0  
Sprint: Beta-4

## Classes

| Class | Examples |
|-------|----------|
| Incident | API/portal down, cannot complete any analysis |
| Defect | Wrong validation message, broken link in help |
| Data | Suspected wrong chart after verified birth data |
| How-to | “How do I read section X?” |
| Feature | New export format, new language |
| Abuse / security | Unauthorized access, vulnerability report |

## Severity

- **S1** All users blocked  
- **S2** Core path blocked for a segment  
- **S3** Non-blocking defect  
- **S4** Question or cosmetic  

## Data vs product

If birth time/timezone is wrong, it is not an engine bug. Ask the customer to re-verify records first (`customer/TROUBLESHOOTING.md`).

## Security

Use `legal/SECURITY_DISCLOSURE.md` template path after counsel review. Do not discuss vulns in public tickets.

## Engine / Knowledge changes

Out of support authority. Escalate as a product defect; do not hot-edit Knowledge packages.

---

END
