# Release Calendar

| Field | Value |
|-------|-------|
| Document | RELEASE_CALENDAR |
| Version | 1.0.0 |
| Status | **OFFICIAL** |
| Date | 2026-08-17 |
| Owner | Release Manager |

This document defines **cadence**, not a schedule.
It does not assign dates.

A cadence slot does not authorise an issue.
Signoff authorises an issue.

---

## 1. Cadence

| Train | Cadence | Meaning |
|-------|---------|---------|
| **Internal** | **Weekly** | Internal builds or reviews may occur weekly. They are not Beta, RC, or Production. They do not require this pack’s full issue record unless shown as a reading. |
| **Beta** | **Monthly** | A Beta quality train may be opened at most on a monthly rhythm, and only if quality work exists and Freeze still holds. If the consultation is not ready, the month is skipped. Skipping is correct. |
| **RC** | **As ready** | Not calendar-driven. RC opens when Product Owner judges Beta quality sufficient to candidate 1.0. Multiple RCs may follow if a candidate fails. |
| **Production** | **As signed** | Not calendar-driven. Production occurs when RC gates pass and Product Owner signs 1.0 (or a later Production version). |
| **Emergency** | **Unscheduled** | Emergency Patch and Hotfix occur when a Critical or High Production defect exists. They do not wait for weekly or monthly slots. |

---

## 2. What cadence is not

- A promise to ship every week or every month
- Permission to add features in a monthly Beta
- A substitute for Golden Dataset regeneration
- A reason to skip Editorial or Commercial review

---

## 3. Planning rule

Release Manager proposes a train.
Product Owner opens it.
If evidence will not exist by the intended cadence, the train is not opened.

Empty months are recorded as “no issue,” not as failed releases.
