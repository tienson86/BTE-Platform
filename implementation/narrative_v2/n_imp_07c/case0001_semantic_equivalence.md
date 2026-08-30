# CASE-0001 Semantic Equivalence Review

Sprint: N-IMP-07C
Rule: FAIL sentences must not enter approved runtime assets.

Meaning is immutable. Language may improve.

| sentence_id | source_meaning | customer_sentence | semantic_change | review_note |
| --- | --- | --- | --- | --- |
| sentence.pattern.chinh_an.meaning.001 | Có chỗ dưỡng, chịu được việc cần nền. Hữu ích khi cần ủ và học có khung. | Bạn thường làm việc tốt hơn khi có chỗ dựa ổn định và khi công việc cần xây từ nền tảng. Bạn cũng phù hợp với việc học có hệ thống và cần thời gian để ngấm dần. | NONE | Chỗ dưỡng → chỗ dựa ổn định. Việc cần nền → việc cần xây từ nền tảng. Ủ và học có khung → học có hệ thống, cần thời gian ngấm dần. No success claim. |
| sentence.strength.strong.meaning.001 | Có nền lực để chịu tải, hoàn thành việc dài, giữ nhịp khi môi trường đòi hỏi sức bền. Hữu ích khi kênh thoát và chế được giữ phép. | Bạn thường duy trì được sự ổn định tốt khi theo đuổi những việc cần thời gian và sự bền bỉ. Điều này hữu ích khi bạn có lối để thể hiện năng lực và khi giới hạn được giữ rõ. | NONE | Nền lực / chịu tải / việc dài / giữ nhịp → ổn định và bền bỉ. Kênh thoát → lối thể hiện năng lực. Chế được giữ phép → giới hạn được giữ rõ. |
| sentence.shensha.hong_loan.meaning.001 | Kênh gặp gỡ, hỷ sự cấu trúc. Hữu ích khi cần mở quan hệ. | Bạn có khuynh hướng gặp gỡ và kết nối trong những hoàn cảnh vui, có khuôn khổ. Điều này hữu ích khi bạn cần mở mối quan hệ. | NONE | Hỷ sự cấu trúc → hoàn cảnh vui có khuôn khổ. No hôn nhân / may mắn prediction. |
| sentence.shensha.thien_at_quy_nhan.meaning.001 | Có chỗ đỡ, giảm ma sát khi thân cần nhờ. Hữu ích khi việc đòi người nâng đúng phép. | Bạn thường có chỗ dựa giúp giảm ma sát khi cần sự hỗ trợ. Điều này hữu ích khi công việc đòi hỏi được nâng đỡ đúng cách. | NONE | Thân cần nhờ → khi cần sự hỗ trợ. Nâng đúng phép → nâng đỡ đúng cách. No quý nhân bảo vệ. |
| sentence.ten_gods.kiep_tai.meaning.001 | Phản xạ nhanh khi nguồn đang bị kẹt. Hữu ích khi cần bứt, không hữu ích khi cần giữ sổ. | Bạn phản xạ nhanh khi nguồn lực đang bị kẹt. Điều này hữu ích khi cần bứt phá, và kém phù hợp khi cần giữ sổ sách chặt. | REVIEW | Nguồn → nguồn lực. Bứt → bứt phá as customer restatement of the same burst, not a success claim. Keep-sổ boundary preserved. Product Owner may tighten wording. |
| sentence.ten_gods.that_sat.meaning.001 | Chịu được cửa hiểm có hạn. Hữu ích khi cần bứt việc khó, có mốc cắt. | Bạn chịu được những cửa việc khó trong phạm vi có hạn. Điều này hữu ích khi cần hoàn thành việc khó với một mốc dừng rõ. | NONE | Cửa hiểm → cửa việc khó, still bounded. Mốc cắt → mốc dừng rõ. |
| sentence.ten_gods.thien_an.meaning.001 | Tự dưỡng được khi khung chính thiếu. Hữu ích khi cần lối học không theo lề. | Bạn tự nuôi dưỡng được khi khung chính chưa đủ. Điều này hữu ích khi cần cách học không theo lối mòn. | NONE | Tự dưỡng → tự nuôi dưỡng. Không theo lề → không theo lối mòn. |

## Rejected (must not resolve)

| sentence_id | status | reason |
| --- | --- | --- |
| sentence.pattern.chinh_an.meaning.draft | draft | Contains chắc chắn thành công. Loaded for negative coverage. Selector ignores draft. |

## FAIL assets entered runtime?

NO.
