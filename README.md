# ABC HR Intelligence
Ứng dụng mô phỏng HR Analytics dùng IBM HR Analytics.

## Cài đặt trên Windows PowerShell
```powershell
cd ABC_HR_Intelligence
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Mở http://127.0.0.1:8000

Nếu PowerShell chặn activate:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Cách chạy
1. Tải CSV IBM HR Analytics từ Kaggle.
2. Mở giao diện và tải CSV lên (cần cột `Attrition` với Yes/No).
3. Xem Tổng quan, EDA, huấn luyện ML, thử dự đoán, xem khuyến nghị.
4. CSV được lưu tại `data/hr_data.csv`; đồng thời dữ liệu được nạp vào SQLite `data/abc_hr.db`, bảng `hr_employees`. File mô hình được lưu trong `artifacts/`.

Dữ liệu IBM HR Analytics là dữ liệu mô phỏng phục vụ nghiên cứu, không phải hồ sơ nhân viên thật của ABC. Điểm rủi ro chỉ hỗ trợ phân tích, không được dùng làm căn cứ duy nhất để ra quyết định bất lợi với nhân viên.
