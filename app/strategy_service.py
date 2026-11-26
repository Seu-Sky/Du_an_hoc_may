def build_recommendations(eda):
    items = []
    if eda["attrition_rate"] >= .15:
        items.append({"priority":"Cao","topic":"Theo dõi biến động nhân sự",
          "evidence":f"Tỷ lệ nghỉ việc quan sát: {eda['attrition_rate']:.1%}.",
          "action":"Phân tích theo phòng ban, thâm niên và vai trò; phỏng vấn nghỉ việc để xác minh nguyên nhân."})
    if eda["overtime_attrition_rate"] > eda["no_overtime_attrition_rate"]:
        items.append({"priority":"Cao","topic":"Rà soát làm thêm giờ",
          "evidence":"Nhóm OverTime=Yes có tỷ lệ nghỉ việc quan sát cao hơn nhóm No.",
          "action":"Kiểm tra tải công việc, lịch làm, thời gian nghỉ và thử nghiệm biện pháp cân bằng tải."})
    if eda["low_satisfaction_attrition_rate"] > eda["high_satisfaction_attrition_rate"]:
        items.append({"priority":"Trung bình","topic":"Cải thiện trải nghiệm nhân viên",
          "evidence":"Nhóm hài lòng công việc thấp có tỷ lệ nghỉ việc quan sát cao hơn nhóm hài lòng cao.",
          "action":"Tổ chức trao đổi 1-1, xem xét môi trường làm việc và cơ hội phát triển."})
    if not items:
        items.append({"priority":"Trung bình","topic":"Theo dõi KPI nhân sự",
          "evidence":"Chưa phát hiện tín hiệu vượt ngưỡng trong các quy tắc hiện tại.",
          "action":"Theo dõi định kỳ và kiểm chứng bằng phản hồi nhân viên."})
    items.append({"priority":"Nguyên tắc","topic":"Sử dụng ML có trách nhiệm",
      "evidence":"Mô hình có sai số và có thể phản ánh thiên lệch trong dữ liệu.",
      "action":"Không dùng điểm rủi ro làm căn cứ duy nhất cho quyết định nhân sự cá nhân."})
    return items
