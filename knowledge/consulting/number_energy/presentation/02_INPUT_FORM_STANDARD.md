# 02_INPUT_FORM_STANDARD.md

# BTE NUMBER ENERGY
## INPUT FORM STANDARD
### Chuẩn biểu mẫu đầu vào — Tư vấn Năng lượng số

**Status:** CANONICAL PRESENTATION STANDARD  
**Version:** 1.0  
**Module:** Number Energy Consulting  
**Method:** Bát Cực Linh Số / Năng lượng số  
**Scope:** Customer Input Form  
**Applies to:** Phone Number · Car Plate · Motorcycle Plate

**Parent:**
- `00_NUMBER_ENERGY_PRESENTATION_MASTER.md`
- `01_INFORMATION_ARCHITECTURE.md`

**Knowledge dependencies:**
- `number_energy/knowledge/01_BAGUA_DIGIT_MAPPING.md`
- `number_energy/knowledge/05_ZERO_FIVE_MODIFIERS.md`
- `number_energy/knowledge/13_PHONE_WEALTH_FLOW_RULES.md`
- `number_energy/knowledge/15_RUNTIME_BINDING_CONTRACT.md`

---

# 1. PURPOSE

Tài liệu này định nghĩa chuẩn giao diện nhập dữ liệu
cho module:

    TƯ VẤN NĂNG LƯỢNG SỐ

Mục tiêu:

    ÍT TRƯỜNG
    DỄ NHẬP
    DỄ HIỂU
    KHÔNG NHẬP DỮ LIỆU THỪA
    KHÔNG TRỘN CÁC PHƯƠNG PHÁP

Customer journey:

    CHỌN LOẠI SỐ
          ↓
    NHẬP DÃY SỐ
          ↓
    KIỂM TRA
          ↓
    PHÂN TÍCH
          ↓
    KẾT QUẢ

---

# 2. V1 PRODUCT BOUNDARY

V1 phân tích:

    BẢN THÂN CẤU TRÚC DÃY SỐ

V1 KHÔNG yêu cầu:

    ngày sinh
    giờ sinh
    nơi sinh
    Bát Tự
    Dụng Thần
    Cung Phi
    Mệnh Quái

Canonical:

    NUMBER_STRUCTURE
    !=
    OWNER_COMPATIBILITY

Lớp tương hợp với chủ nhân
có thể phát triển sau.

Không đưa các trường đó
vào form V1.

---

# 3. INPUT FORM STRUCTURE

Canonical form gồm hai bước logic:

    1. CHỌN LOẠI PHÂN TÍCH
    2. NHẬP SỐ

Không cần wizard nhiều bước.

Preferred desktop:

    single card

Preferred mobile:

    same form
    stacked vertically

---

# 4. FORM HEADER

Title:

    TƯ VẤN NĂNG LƯỢNG SỐ

Supporting text:

    Phân tích cấu trúc trường khí của số điện thoại
    hoặc biển số xe theo Bát Cực Linh Số.

Optional introduction:

    Hệ thống phân tích từng cặp số,
    sự kết hợp của các bộ ba,
    trường khí chủ đạo
    và năng lượng phần cuối dãy.

Do not place long methodology text
above the input.

---

# 5. ANALYSIS TYPE

Field label:

    Loại số cần phân tích

Required:

    YES

Canonical options:

    Số điện thoại
    Biển số ô tô
    Biển số xe máy

Internal values:

    phone_number
    car_plate
    motorcycle_plate

Preferred control:

    segmented cards
    or radio cards

Do not use a hidden default
unless explicitly frozen later.

---

# 6. ANALYSIS TYPE CARD

Each option may show:

## Số điện thoại

Supporting copy:

    Xem cấu trúc năng lượng,
    tài vận, nguồn tài, dòng tài
    và năng lượng phần cuối dãy.

## Biển số ô tô

Supporting copy:

    Xem cấu trúc Cát – Hung,
    tính ổn định, công việc,
    tài vận và năng lượng kết.

## Biển số xe máy

Supporting copy:

    Phân tích cấu trúc trường khí,
    mức cân bằng và năng lượng phần cuối biển số.

Keep copy short.

---

# 7. NO DEFAULT TYPE

Preferred canonical behavior:

    no analysis type selected initially

Reason:

Phone and Vehicle use
different product presentation profiles.

The customer should intentionally choose:

    PHONE
    CAR
    MOTORBIKE

If Product later decides
to default to Phone:

requires explicit Presentation update.

---

# 8. PHONE NUMBER FIELD

When:

    analysis_type = phone_number

Show:

    Số điện thoại

Required:

    YES

Example placeholder:

    Ví dụ: 0328278786

Input should accept:

    0328278786
    0328 278 786
    0328.278.786

Presentation may normalize visually.

Runtime truth must follow:

    15_RUNTIME_BINDING_CONTRACT.md

---

# 9. PHONE INPUT HELP

Supporting copy:

    Nhập đầy đủ số điện thoại đang sử dụng.

Optional second line:

    Số 0 đầu dãy được nhận diện là tiền tố
    và không tham gia ghép cặp Du Niên.

This technical line may be omitted
from the main form
and shown only as helper/tooltip.

Customer does not need to understand
the normalization algorithm before analysis.

---

# 10. PHONE DISPLAY NORMALIZATION

Customer may input:

    0328278786

Result display may format:

    0328 278 786

But raw order must remain unchanged.

Canonical analysis body:

    328278786

for Vietnamese leading phone zero.

Do not visually remove the initial 0
from the customer's phone number.

Distinguish:

    DISPLAY NUMBER
    vs
    ANALYSIS BODY

---

# 11. PHONE ZERO RULE

Leading phone zero:

    PREFIX

Internal/middle/trailing zero:

    SEMANTIC MODIFIER

Example:

    0912034567

Only the valid phone prefix zero
may be excluded under Phone Input Policy.

Other zero digits must remain
available to Modifier Engine.

Frontend MUST NOT simply:

    remove all zeros

before sending input.

---

# 12. PHONE FIVE RULE

Digit:

    5

must remain in the input.

Frontend MUST NOT:

    remove 5
    replace 5
    treat 5 as invalid

It is routed by runtime
to canonical Modifier logic.

---

# 13. PHONE VALIDATION

Customer validation should check:

    field is not empty
    contains an acceptable phone-number structure
    contains numeric content
    normalization succeeds

Frontend SHOULD NOT implement
Du Niên validation itself.

Engine remains responsible
for analytical truth.

---

# 14. PHONE LENGTH

Presentation layer should avoid
hard-coding analytical truth based solely
on one specific phone length.

However for Vietnamese customer UX,
the form may recognize normal
domestic phone formats.

If a sequence cannot be accepted:

Customer message:

    Số điện thoại chưa đúng định dạng.
    Vui lòng kiểm tra và nhập lại đầy đủ dãy số.

Do not expose parser exceptions.

---

# 15. PHONE COUNTRY PREFIX

If future Product supports:

    +84

the normalization policy must be explicit.

Example:

    +84 328 278 786

may correspond to display identity:

    0328278786

But Presentation MUST NOT implement
this conversion independently
unless Runtime Input Contract supports it.

V1 may restrict accepted formats
to the formats already supported by runtime.

---

# 16. CAR PLATE FIELD

When:

    analysis_type = car_plate

Show:

    Biển số ô tô

Required:

    YES

Placeholder:

    Ví dụ: 30A-123.45

Supporting copy:

    Nhập đầy đủ biển số như trên đăng ký hoặc biển xe.

---

# 17. MOTORCYCLE PLATE FIELD

When:

    analysis_type = motorcycle_plate

Show:

    Biển số xe máy

Required:

    YES

Placeholder:

    Ví dụ: 29X1-123.45

Supporting copy:

    Nhập đầy đủ biển số xe cần phân tích.

---

# 18. VEHICLE NORMALIZATION WARNING

Vehicle plates contain:

    province digits
    letters
    series digits
    punctuation

Presentation MUST NOT decide
which numeric components participate
in Number Energy truth.

That belongs to:

    VEHICLE INPUT POLICY

and:

    Runtime Binding Contract.

Until policy is frozen:

    DO NOT GUESS.

---

# 19. VEHICLE LETTERS

Letters such as:

    A
    B
    X
    H

are NOT automatically
Bagua digits.

Frontend must preserve
the original plate string.

Runtime determines
the canonical numeric analysis sequence.

---

# 20. VEHICLE DISPLAY IDENTITY

Result Hero should retain:

    original formatted plate

Example:

    30A-123.45

Even if runtime later analyzes
a normalized numeric body.

Again distinguish:

    DISPLAY IDENTITY
    ANALYSIS BODY

---

# 21. OPTIONAL NAME FIELD

V1 recommendation:

    DO NOT REQUIRE NAME

Reason:

Intrinsic Number Energy analysis
does not need customer identity.

If Product wants report personalization,
an optional field may exist:

    Họ tên
    Không bắt buộc

But it MUST NOT affect analytical truth.

Recommended V1:

    omit from minimal form

unless PDF/report personalization
is already required.

---

# 22. GENDER FIELD

V1:

    DO NOT SHOW

Gender is not required
for intrinsic Number Energy truth.

Even though historical knowledge
may contain gender-specific wording,
Customer V1 must not request gender
unless a later canonical method
actually uses it.

---

# 23. BIRTH DATE FIELD

V1:

    DO NOT SHOW

Birth date belongs to future:

    OWNER COMPATIBILITY

Possible future flow:

    Number Energy
        +
    Cung Phi
        +
    BaZi / Useful God
        ↓
    Personal Suitability

Not part of this form.

---

# 24. PURPOSE FIELD

V1 recommendation:

Do not ask:

    Bạn muốn cầu gì?
    Tài lộc?
    Tình duyên?
    Công việc?

before intrinsic analysis.

Reason:

The same number should first produce
the same intrinsic truth.

Purpose can later be used
to filter recommendations,
not rewrite the number.

Canonical:

    NUMBER TRUTH FIRST
    PURPOSE FILTER SECOND

---

# 25. PRIMARY CTA

Phone:

    PHÂN TÍCH SỐ ĐIỆN THOẠI

Car:

    PHÂN TÍCH BIỂN SỐ Ô TÔ

Motorcycle:

    PHÂN TÍCH BIỂN SỐ XE MÁY

Alternative universal CTA:

    PHÂN TÍCH NĂNG LƯỢNG SỐ

Preferred:

Contextual CTA changes
with analysis type.

---

# 26. CTA STATE

Before valid input:

    disabled

During request:

    loading

Loading copy:

    Đang phân tích năng lượng số...

Do not:

    allow repeated submit
    create duplicate analysis
    change input silently

---

# 27. VALIDATION MESSAGE

Required missing type:

    Vui lòng chọn loại số cần phân tích.

Required missing number:

Phone:

    Vui lòng nhập số điện thoại.

Car:

    Vui lòng nhập biển số ô tô.

Motorcycle:

    Vui lòng nhập biển số xe máy.

---

# 28. INVALID INPUT MESSAGE

Phone:

    Số điện thoại chưa đúng định dạng.
    Vui lòng kiểm tra và nhập lại.

Vehicle:

    Biển số chưa đúng định dạng.
    Vui lòng kiểm tra và nhập lại đầy đủ.

Avoid:

    INVALID_INPUT
    parse_error
    normalization_failed
    HTTP 422

in Customer Mode.

---

# 29. ANALYSIS FAILURE

Transport/runtime error:

    Không thể hoàn tất phân tích lúc này.
    Vui lòng thử lại.

If technical detail exists:

Expert Mode may expose it.

Customer Mode does not.

---

# 30. UNDEFINED KNOWLEDGE

If input is structurally valid
but runtime contains an unsupported
knowledge combination:

Do NOT present:

    "Số không hợp lệ."

Instead:

    Phân tích đã hoàn tất,
    nhưng một phần tổ hợp hiện chưa có
    dữ liệu luận giải chi tiết.

Supported findings should still display
if runtime contract permits partial results.

---

# 31. FORM STATE MODEL

Canonical states:

    IDLE
    TYPE_SELECTED
    INPUT_INCOMPLETE
    READY
    SUBMITTING
    SUCCESS
    VALIDATION_ERROR
    TRANSPORT_ERROR

Optional:

    PARTIAL_RESULT

Frontend labels should not expose
these raw state names.

---

# 32. TYPE SWITCHING

If customer changes:

    Phone
        →
    Car Plate

the input field must update
to the correct product type.

Recommended behavior:

Clear incompatible input
or explicitly preserve only
if format is still meaningful.

Never silently analyze
a phone number as a vehicle plate.

---

# 33. TYPE SWITCH DURING RESULT

If a result already exists
and customer changes analysis type:

Do not mutate the existing result
into the new profile.

The next successful Analyze
creates a new current analysis.

Previous result remains history
if persistence exists.

---

# 34. FORM AND RESULT RELATIONSHIP

Preferred experience:

    FORM
      ↓
    RESULT

Result may appear:

    on same route below form

or:

    dedicated result state

depending portal architecture.

But Product must preserve:

    selected analysis type
    original input
    current analysis identity

---

# 35. FORM RESET

Optional action:

    Phân tích số khác

Behavior:

    return to clean input state

Do not use:

    Reset

as primary customer wording.

---

# 36. PHONE QUICK EXAMPLE

Optional helper:

    Thử với số mẫu: 0328278786

This is useful in development/demo,
but production customer UI
should not make the Golden Case
look like a recommendation.

If included:

label clearly:

    Ví dụ minh họa

---

# 37. CUSTOMER INTRO COPY

Recommended compact copy:

    Phân tích dãy số theo Bát Cực Linh Số
    để nhận diện cấu trúc Cát – Hung,
    các bộ ba năng lượng,
    trường khí chủ đạo
    và năng lượng phần cuối dãy.

For Phone, after selection:

    Với số điện thoại,
    hệ thống còn phân tích Tài vận,
    nguồn Tài, dòng Tài và hậu vận của dãy số.

---

# 38. DO NOT OVEREXPLAIN BEFORE ANALYSIS

Do not put above the form:

- full 8-energy definitions;
- 64 interaction matrix;
- long methodology;
- score formula;
- remedy rules;
- strength table.

Those belong after result
or in educational content.

Input page should prioritize action.

---

# 39. DESKTOP LAYOUT

Recommended:

    ┌──────────────────────────────────────────────────┐
    │ TƯ VẤN NĂNG LƯỢNG SỐ                           │
    │ Mô tả ngắn                                      │
    │                                                  │
    │ Loại số cần phân tích                           │
    │ [Số điện thoại] [Ô tô] [Xe máy]                │
    │                                                  │
    │ Số điện thoại                                   │
    │ [ 0328278786                               ]     │
    │                                                  │
    │          [ PHÂN TÍCH SỐ ĐIỆN THOẠI ]           │
    └──────────────────────────────────────────────────┘

Keep form width controlled.

Do not stretch a single input
across the entire desktop viewport.

---

# 40. MOBILE LAYOUT

Recommended:

    TƯ VẤN NĂNG LƯỢNG SỐ

    [ Số điện thoại ]
    [ Ô tô           ]
    [ Xe máy         ]

    Số điện thoại
    [ 0328278786 ]

    [ PHÂN TÍCH ]

All controls:

    full-width where useful
    large tap targets
    readable labels

No horizontal overflow.

---

# 41. ACCESSIBILITY

Required:

- visible field labels;
- keyboard navigation;
- semantic radio/group behavior;
- focus states;
- error association;
- loading state announced;
- CTA accessible name;
- sufficient contrast.

Placeholder MUST NOT replace
the visible field label.

---

# 42. INPUT MASKING

Phone input may visually format digits.

But masking MUST NOT:

- reorder digits;
- drop semantic zeros;
- drop 5;
- alter runtime payload incorrectly.

Original semantic sequence
must remain recoverable.

---

# 43. COPY / PASTE

Input must support paste.

Examples:

    0328278786
    0328 278 786
    30A-123.45

Do not require customer
to manually remove punctuation
if normalizer supports it.

---

# 44. CUSTOMER PRIVACY PRESENTATION

Do not imply:

    the number is publicly stored
    shared
    published

unless product actually does so.

No unnecessary privacy claims.

If history exists,
it should be presented
through the portal's normal history behavior.

---

# 45. RESULT TRANSITION

After successful analysis:

Preferred:

    smooth move to Result Hero

Do not leave customer wondering
whether anything happened.

The analyzed identity
must be immediately visible.

Example:

    KẾT QUẢ PHÂN TÍCH

    0328 278 786

---

# 46. INPUT → RESULT IDENTITY

Result MUST preserve:

    analysis_type
    original_display_value
    normalized_analysis_identity

Customer sees:

    original/display value

Expert trace may see:

    normalized body

Example:

Customer:

    0328 278 786

Expert:

    analysis body = 328278786

---

# 47. CUSTOMER MODE

Default:

    CUSTOMER MODE

Form does not show:

    Expert toggle

unless Presentation Master
explicitly requires it.

Expert Mode may be activated
through a separate seam such as:

    ?expert=true

if existing product architecture uses it.

---

# 48. NO ENGINE OPTIONS

Customer must NOT choose:

    strength algorithm
    modifier algorithm
    Du Niên version
    tail weight
    score mode
    control policy

Those are canonical engine decisions.

---

# 49. NO MANUAL CÁT/HUNG OVERRIDE

Frontend must not allow:

    "Tôi muốn coi 28 là..."
    "Bỏ cặp 32..."
    "Chỉ xem 4 số cuối..."

unless a future Expert research tool
explicitly supports it.

Customer product uses canonical analysis.

---

# 50. STATIC GOLDEN UI PHASE

Before runtime binding,
Cursor