# User Journeys

Version: 1.0.0  
Sprint: Beta-5

Complete consultant-style path. Record expected outcome, possible failure, feedback point, completion criteria.

## J1 — Landing

| | |
|--|--|
| Steps | Open product URL → first screen loads |
| Expected | Calm, professional landing or signed-in home; no mystical splash |
| Failure | Blank page, mixed-up env, cert warning |
| Feedback | UX / performance |
| Complete | User knows where to start an analysis |

## J2 — Create analysis

| | |
|--|--|
| Steps | New analysis → enter birth data → submit once |
| Expected | Validation helps; submit accepted |
| Failure | Impossible dates accepted; timezone confusion; double create |
| Feedback | UX / bug |
| Complete | Analysis id or waiting state visible |

## J3 — Waiting

| | |
|--|--|
| Steps | Remain on progress / wait UI until done |
| Expected | Clear in-progress vs complete; no panic refresh loop required |
| Failure | Infinite wait, silent fail, unclear error |
| Feedback | Performance / bug / support |
| Complete | User reaches readable report or a clear error |

## J4 — Read report

| | |
|--|--|
| Steps | Open report → overview → main sections |
| Expected | Hierarchy readable; consultant tone |
| Failure | Empty sections, overwhelming dump, wrong person header |
| Feedback | Report / interpretation / UX |
| Complete | User can state the overview in their own words |

## J5 — Knowledge

| | |
|--|--|
| Steps | From report term → Knowledge Center (if enabled) → return |
| Expected | Term explained; not a second fortune engine |
| Failure | Broken link, missing article, dead end |
| Feedback | Knowledge / UX |
| Complete | User returns to report with clearer term |

## J6 — Save PDF

| | |
|--|--|
| Steps | Export or save PDF if the live UI offers it |
| Expected | File downloads; identity matches case |
| Failure | Empty PDF, timeout, wrong case |
| Feedback | Bug / commercial (license) |
| Complete | PDF opened and skimmable |

If PDF is not in the frozen UI, mark scenario **N/A** and file a feature request — do not build PDF in this sprint.

## J7 — Share

| | |
|--|--|
| Steps | Share action if present (link or file) |
| Expected | User understands who will see data |
| Failure | Accidental public link, missing control |
| Feedback | UX / commercial / security |
| Complete | Share succeeded **or** user knowingly cancelled |

If share is absent, **N/A** + feature request.

## J8 — History

| | |
|--|--|
| Steps | Open history / cases → reopen a finished analysis |
| Expected | Same report as before |
| Failure | Missing case, wrong report |
| Feedback | Bug / UX |
| Complete | Prior case reopened |

## J9 — Return

| | |
|--|--|
| Steps | Leave product → come back later → find work |
| Expected | Sign-in or invite still works; history reachable |
| Failure | Lost session with no recovery path |
| Feedback | UX / support / commercial |
| Complete | User resumes without recreating the chart from memory |

---

END
