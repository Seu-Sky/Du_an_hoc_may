# ABC HR Intelligence

Ứng dụng HR Analytics mô phỏng dùng bộ dữ liệu IBM HR Analytics, xây dựng bằng Streamlit.

## Cài đặt nhanh

Cần cài Git và Python 3.10 trở lên. Clone dự án:

```bash
git clone https://github.com/Seu-Sky/Du_an_hoc_may.git
cd Du_an_hoc_may
```

Tạo môi trường ảo và cài các thư viện.

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

Mở địa chỉ Streamlit hiển thị trong Terminal, thường là http://localhost:8501. Hướng dẫn chi tiết và cách xử lý lỗi kích hoạt môi trường ảo trên Windows có trong [huongdan.md](huongdan.md).

Ứng dụng có sẵn dữ liệu mẫu `WA_Fn-UseC_-HR-Employee-Attrition.csv`; file CSV tải lên cần có cột `Attrition` với giá trị `Yes/No` hoặc `1/0`.
