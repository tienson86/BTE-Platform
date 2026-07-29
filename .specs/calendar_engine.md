# Calendar Engine Specification

Version: 1.0

Status: Official

---

# 1. Purpose

Calendar Engine chịu trách nhiệm chuyển đổi dữ liệu thời gian đầu vào thành dữ liệu lịch thiên văn chuẩn phục vụ toàn bộ hệ thống.

Đây là Engine đầu tiên trong Pipeline.

Không thực hiện bất kỳ phép luận giải Bát Tự nào.

---

# 2. Responsibilities

Calendar Engine phải hỗ trợ:

- Gregorian Calendar
- Lunar Calendar
- Julian Day Number
- Delta T
- Solar Longitude
- Solar Terms (24 Tiết Khí)
- Moon Phase
- New Moon
- Time Zone
- Leap Month
- Heavenly Stem & Earthly Branch của lịch

---

# 3. Non-Responsibilities

Calendar Engine KHÔNG được:

- Tính Tứ Trụ
- Tính Thập Thần
- Tính Dụng Thần
- Chấm điểm
- Luận giải
- Sinh báo cáo

---

# 4. Input

BirthInput

Bao gồm:

- birth_datetime
- timezone
- longitude
- latitude

---

# 5. Output

CalendarResult

Bao gồm:

- solar_datetime
- lunar_datetime
- julian_day
- delta_t
- solar_longitude
- solar_term
- moon_phase
- new_moon
- leap_month
- year_ganzhi
- month_ganzhi
- day_ganzhi
- hour_ganzhi

---

# 6. Public API

CalendarService

Các phương thức chính:

- calculate()
- convert_to_lunar()
- calculate_julian_day()
- calculate_solar_terms()

---

# 7. Internal Components

calendar.py

julian.py

solar_term.py

moon/

timezone.py

converter.py

validators.py

---

# 8. Processing Flow

BirthInput

↓

Validate

↓

Timezone Normalize

↓

Julian Day

↓

Solar Longitude

↓

Solar Terms

↓

Moon Phase

↓

Lunar Calendar

↓

Ganzhi

↓

CalendarResult

---

# 9. Dependencies

Internal

- Astronomy Tables
- Periodic Terms Database

Không phụ thuộc Engine khác.

---

# 10. Error Handling

Các Exception:

CalendarError

InvalidDateError

TimezoneError

AstronomyCalculationError

---

# 11. Performance

Một lần tính toán chuẩn:

< 50 ms

Không đọc dữ liệu nhiều lần.

Ưu tiên cache bảng thiên văn.

---

# 12. Testing Strategy

Unit Test

- Julian
- Lunar
- Solar Terms
- Moon Phase

Integration Test

Golden Dataset

Regression Test

---

# 13. Future Extensions

- Swiss Ephemeris
- NASA JPL
- High Precision Ephemeris
- Historical Calendar Support

---

END
