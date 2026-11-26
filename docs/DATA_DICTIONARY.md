# Từ điển dữ liệu 35 cột IBM HR Analytics

| # | Cột | Ý nghĩa | Vai trò/lưu ý |
|---:|---|---|---|
|1|Age|Tuổi nhân viên|Đầu vào số|
|2|Attrition|Đã nghỉ việc chưa (Yes/No)|Nhãn mục tiêu|
|3|BusinessTravel|Nhóm/tần suất công tác|Phân loại|
|4|DailyRate|Daily Rate trong bộ dữ liệu|Không tự hiểu là lương|
|5|Department|Phòng ban|Phân loại|
|6|DistanceFromHome|Khoảng cách nhà đến nơi làm|Số|
|7|Education|Mã mức học vấn|Thang mã hóa|
|8|EducationField|Lĩnh vực học vấn|Phân loại|
|9|EmployeeCount|Số lượng nhân viên|Thường hằng số, loại|
|10|EmployeeNumber|Mã định danh|Không dùng làm đặc trưng|
|11|EnvironmentSatisfaction|Hài lòng môi trường|Thang 1–4|
|12|Gender|Giới tính|Nhạy cảm, cân nhắc fairness|
|13|HourlyRate|Hourly Rate|Số|
|14|JobInvolvement|Mức độ tham gia công việc|Thang 1–4|
|15|JobLevel|Cấp bậc công việc|Thang cấp bậc|
|16|JobRole|Vai trò/chức danh|Phân loại|
|17|JobSatisfaction|Hài lòng công việc|Thang 1–4|
|18|MaritalStatus|Tình trạng hôn nhân|Nhạy cảm, cân nhắc fairness|
|19|MonthlyIncome|Thu nhập tháng|Số|
|20|MonthlyRate|Monthly Rate|Không mặc định là lương|
|21|NumCompaniesWorked|Số công ty từng làm|Số|
|22|Over18|Trên 18 tuổi?|Thường hằng số, loại|
|23|OverTime|Có làm thêm giờ?|Yes/No|
|24|PercentSalaryHike|Phần trăm tăng lương|Số|
|25|PerformanceRating|Mức đánh giá hiệu suất|Mã/thang|
|26|RelationshipSatisfaction|Hài lòng quan hệ|Thang 1–4|
|27|StandardHours|Giờ chuẩn|Thường hằng số, loại|
|28|StockOptionLevel|Mức quyền chọn cổ phiếu|Mã/thang|
|29|TotalWorkingYears|Tổng số năm làm việc|Số|
|30|TrainingTimesLastYear|Số lần đào tạo năm trước|Số|
|31|WorkLifeBalance|Cân bằng công việc-cuộc sống|Thang 1–4|
|32|YearsAtCompany|Số năm tại công ty|Số|
|33|YearsInCurrentRole|Số năm ở vai trò hiện tại|Số|
|34|YearsSinceLastPromotion|Số năm từ lần thăng chức|Số|
|35|YearsWithCurrManager|Số năm với quản lý hiện tại|Số|

`Attrition`: Yes→1, No→0. Cột phân loại được One-Hot Encoding; cột số được điền thiếu bằng median và chuẩn hóa. EmployeeNumber là ID; EmployeeCount, Over18, StandardHours thường không có khả năng phân biệt nên loại khỏi feature. Age, Gender, MaritalStatus cần đánh giá rủi ro công bằng và không được dùng để ra quyết định bất lợi tự động. Kiểm tra tên/cấu trúc CSV thực tế trước khi chạy vì các bản sao dataset có thể khác nhau.
