# Giải thích code

## data_service.py
- `load_data()`: đọc CSV đã upload.
- `clean_data()`: chuẩn hóa tên cột và khoảng trắng, loại dòng trùng, loại dòng thiếu nhãn, điền thiếu số bằng median và phân loại bằng mode.
- `validate_dataset()`: kiểm tra cột Attrition và giá trị Yes/No.

## ml_service.py
- `prepare()`: tách X (đặc trưng) và y (nhãn), loại ID/cột hằng số.
- `train_test_split`: chia 80% train, 20% test; `stratify=y` giữ tỷ lệ hai lớp.
- `ColumnTransformer`: xử lý riêng dữ liệu số và phân loại.
- `Pipeline`: gói tiền xử lý cùng mô hình để tránh học thông tin từ tập test.
- Ba thuật toán: Logistic Regression, Decision Tree, Random Forest.
- Chọn mô hình theo F1-score; lưu pipeline bằng joblib.
- `predict_one()`: nạp pipeline và trả xác suất Attrition=Yes.

## Các chỉ số
- Accuracy: tỷ lệ dự đoán đúng trên tổng số.
- Precision: trong số dự đoán nghỉ việc, bao nhiêu trường hợp đúng.
- Recall: trong số người thực sự nghỉ việc, mô hình tìm được bao nhiêu.
- F1: trung bình điều hòa Precision và Recall.
- ROC-AUC: khả năng xếp hạng mẫu dương cao hơn mẫu âm.
- Confusion matrix theo nhãn 0=No, 1=Yes: [[TN, FP], [FN, TP]].

## main.py và giao diện
FastAPI cung cấp API upload, overview, EDA, train, predict, strategies. `static/app.js` gọi API bằng fetch và vẽ biểu đồ Chart.js. `strategy_service.py` dùng luật rõ ràng dựa trên tỷ lệ nhóm; đây là hệ thống hỗ trợ quyết định dạng rule-based, không phải LLM tạo sinh.
