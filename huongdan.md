# Hướng dẫn cài đặt và chạy dự án

## Yêu cầu

- Git
- Python 3.10 trở lên

## Clone dự án

Mở Terminal hoặc PowerShell tại thư mục muốn lưu dự án, sau đó chạy:

```bash
git clone https://github.com/Seu-Sky/Du_an_hoc_may.git
cd Du_an_hoc_may
```

## Cài đặt và chạy trên Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

Nếu PowerShell báo không cho phép chạy script khi kích hoạt môi trường ảo, chạy lệnh sau trong cửa sổ PowerShell hiện tại rồi kích hoạt lại:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Cài đặt và chạy trên macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

Sau khi chạy, mở địa chỉ được Streamlit hiển thị trong Terminal (thường là http://localhost:8501). Dừng ứng dụng bằng `Ctrl+C`.

## Dữ liệu

Dự án đi kèm file dữ liệu mẫu `WA_Fn-UseC_-HR-Employee-Attrition.csv`. Có thể chạy ứng dụng với dữ liệu mẫu hoặc tải lên file CSV khác có cột `Attrition` với giá trị `Yes/No` hoặc `1/0`.
