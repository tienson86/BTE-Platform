# 01_DATA_MODEL.md

Version: 1.0

Status: CANONICAL

Pack: 01

Engine: Calendar Engine

---

# 1. Purpose

This document defines the canonical data models used by the Calendar Engine.

The Calendar Engine exposes exactly one public input model and one public output model.

Input

BirthRequest

↓

Calendar Engine

↓

BirthContext

No other public models are permitted.

---

# 2. Design Principles

The Calendar Engine models follow these principles:

- Immutable
- Strongly Typed
- Versioned
- Serializable
- Engine Independent
- Forward Compatible

The models defined here become the official contracts of the BTE Platform.

---

# 3. Canonical Input Model

## BirthRequest

BirthRequest represents the original birth information provided by the user.

No calculations are performed inside this model.

---

### 3.1 Identity

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| request_id | UUID | Yes | Unique request identifier |
| version | string | Yes | Schema version |
| created_at | datetime | Yes | Request creation time |

---

### 3.2 Personal Information

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| full_name | string | Yes | Full name |
| gender | enum | Yes | Male / Female |
| language | string | No | Preferred language |

---

### 3.3 Birth Information

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| birth_date | date | Yes | Gregorian birth date |
| birth_time | time | Yes | Local birth time |
| timezone | string | Yes | IANA timezone |
| latitude | decimal | Yes | Latitude |
| longitude | decimal | Yes | Longitude |
| location_name | string | No | Human-readable location |

---

### 3.4 Optional Settings

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| daylight_saving | boolean | No | DST override |
| calendar_override | string | No | Historical calendar selection |
| notes | string | No | Internal notes |

---

# 4. Canonical Output Model

## BirthContext

BirthContext is the official output of the Calendar Engine.

Every downstream Engine consumes this model.

No downstream Engine recalculates calendar information.

---

## 4.1 Metadata

| Field | Type | Description |
|--------|------|-------------|
| request_id | UUID | Original request |
| version | string | Schema version |
| generated_at | datetime | Context creation time |
| engine_version | string | Calendar Engine version |

---

## 4.2 Original Birth Data

| Field | Type | Description |
|--------|------|-------------|
| solar_datetime | datetime | Normalized local datetime |
| timezone | string | Final timezone |
| utc_offset | integer | Minutes offset |

---

## 4.3 Lunar Calendar

| Field | Type | Description |
|--------|------|-------------|
| lunar_year | integer | Lunar year |
| lunar_month | integer | Lunar month |
| lunar_day | integer | Lunar day |
| leap_month | boolean | Leap month flag |
| lunar_datetime | datetime | Lunar datetime |

---

## 4.4 Astronomical Data

| Field | Type | Description |
|--------|------|-------------|
| julian_day | decimal | Julian Day Number |
| solar_term | string | Current solar term |
| season | enum | Spring / Summer / Autumn / Winter |
| longitude | decimal | Longitude |
| latitude | decimal | Latitude |

---

## 4.5 Heavenly Stems & Earthly Branches

| Field | Type | Description |
|--------|------|-------------|
| year_ganzhi | string | Year pillar |
| month_ganzhi | string | Month pillar |
| day_ganzhi | string | Day pillar |
| hour_ganzhi | string | Hour pillar |

---

## 4.6 Derived Calendar Data

| Field | Type | Description |
|--------|------|-------------|
| zodiac | string | Chinese zodiac |
| yin_yang | enum | Yin / Yang |
| seasonal_phase | string | Seasonal phase |
| calendar_source | string | Data source |

---

## 4.7 Quality Information

| Field | Type | Description |
|--------|------|-------------|
| confidence | decimal | Confidence score |
| warnings | list | Validation warnings |
| errors | list | Calculation errors |

---

# 5. Model Relationship

BirthRequest

↓

Calendar Engine

↓

BirthContext

BirthContext is immutable.

No downstream Engine may modify its values.

---

# 6. Serialization

Both models must support:

- JSON
- YAML
- MessagePack

Future binary serialization may be added without changing the schema.

---

# 7. Validation Rules

BirthRequest is validated before entering the Calendar Engine.

BirthContext is validated before leaving the Calendar Engine.

Invalid models are never passed downstream.

---

# 8. Versioning

Major

Breaking schema changes.

Minor

Additional fields.

Patch

Documentation or bug fixes.

BirthContext compatibility must be preserved whenever possible.

---

# 9. Extension Rules

Future fields may only be appended.

Existing fields must not change meaning.

Existing field names must remain stable.

Field removal requires a major version.

---

# 10. Canonical Contract

BirthRequest and BirthContext are the only public data contracts of the Calendar Engine.

Every Engine in the BTE Platform must consume BirthContext rather than recalculating calendar information independently.

These models are the single source of truth for all downstream processing.

---

END OF DOCUMENT