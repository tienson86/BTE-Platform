# Component Lifecycle

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-2

---

## 1. Canonical lifecycle

```
Receive Contract
        ↓
Validate
        ↓
Bind
        ↓
Format
        ↓
Render
        ↓
Expand
        ↓
Dispose
```

No business logic at any step.

---

## 2. Stages

### Receive Contract

ResultPage receives `PortalResultModel` from the adapter.  
Children receive owned slices only.

### Validate

Check required fields per `UI_CONTRACT.md`.  
Invalid Hero/Summary → page `error`.  
Invalid optional section → that unit `empty` / `hidden` / `error`.

### Bind

Map props 1:1 from model fields.  
No derived consulting fields.

### Format

Apply `format` tokens only (clamp 5, trim, enum → i18n already resolved by adapter).

### Render

Follow `RENDERING_PRIORITY.md` and PX-1 reading order.

### Expand

User events toggle disclosure.  
No re-validate of Report truth required unless page retry.

### Dispose

Clear expand state. Drop model reference. No cache of engine objects (none should exist).

---

## 3. Page vs component

| Level | Owns |
|-------|------|
| Page | Receive adapter output · page state · retry |
| Component | Bind slice · local expand · local empty/error card |

---

## 4. Retry

Retry returns to **Receive Contract** for the declared scope (`page` or section).  
It does not authorize engine access from the component.

---

## 5. Stop line

Lifecycle is mechanical presentation. Meaning is already in the contract.

END
