import io
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils import resample
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

st.set_page_config(
    page_title="IBM HR Analytics",
    page_icon="",
    layout="wide"
)

plt.style.use('ggplot')

VALUE_LABELS_VI = {
    "Male": "Nam",
    "Female": "Nữ",
    "Single": "Độc thân",
    "Married": "Đã kết hôn",
    "Divorced": "Đã ly hôn",
    "Sales": "Kinh doanh",
    "Research & Development": "Nghiên cứu & Phát triển",
    "Human Resources": "Nhân sự",
    "Sales Representative": "Nhân viên kinh doanh",
    "Sales Executive": "Chuyên viên kinh doanh",
    "Laboratory Technician": "Kỹ thuật viên phòng thí nghiệm",
    "Research Scientist": "Nhà khoa học nghiên cứu",
    "Manufacturing Director": "Giám đốc sản xuất",
    "Healthcare Representative": "Đại diện chăm sóc sức khỏe",
    "Manager": "Quản lý",
    "Research Director": "Giám đốc nghiên cứu",
    "Non-Travel": "Không đi công tác",
    "Travel_Rarely": "Ít đi công tác",
    "Travel_Frequently": "Đi công tác thường xuyên",
    "Yes": "Có",
    "No": "Không",
    "Life Sciences": "Khoa học sự sống",
    "Medical": "Y tế",
    "Marketing": "Tiếp thị",
    "Technical Degree": "Bằng kỹ thuật",
    "Other": "Khác"
}

VALUE_LABELS_EN = {
    "Male": "Male",
    "Female": "Female",
    "Single": "Single",
    "Married": "Married",
    "Divorced": "Divorced",
    "Sales": "Sales",
    "Research & Development": "Research & Development",
    "Human Resources": "Human Resources",
    "Sales Representative": "Sales Representative",
    "Sales Executive": "Sales Executive",
    "Laboratory Technician": "Laboratory Technician",
    "Research Scientist": "Research Scientist",
    "Manufacturing Director": "Manufacturing Director",
    "Healthcare Representative": "Healthcare Representative",
    "Manager": "Manager",
    "Research Director": "Research Director",
    "Non-Travel": "Non-Travel",
    "Travel_Rarely": "Travel Rarely",
    "Travel_Frequently": "Travel Frequently",
    "Yes": "Yes",
    "No": "No",
    "Life Sciences": "Life Sciences",
    "Medical": "Medical",
    "Marketing": "Marketing",
    "Technical Degree": "Technical Degree",
    "Other": "Other"
}

I18N = {
    "vi": {
        "sidebar_title": "Cấu Hình Hệ Thống",
        "threshold_label": "Ngưỡng quyết định",
        "threshold_help": "Hạ xuống 0.35 để cảnh báo sớm tối đa; tăng lên 0.60 để cân bằng độ chính xác.",
        "preset_label": "Nạp nhanh hồ sơ mẫu:",
        "presets": [
            "Tùy chỉnh thủ công",
            "Hồ sơ Nguy cơ cao (Nhân viên kinh doanh trẻ, tăng ca)",
            "Hồ sơ Ổn định (Giám đốc nghiên cứu)"
        ],
        "upload_header": "Tải file CSV khác để phân tích",
        "upload_label": "Chọn file CSV nhân sự",
        "upload_help": "Tải file CSV khác có cột Attrition để phân tích và huấn luyện lại mô hình.",
        "uploading_msg": "Đang phân tích: {name} ({rows} dòng)",
        "default_data_msg": "Đang dùng dữ liệu mặc định: IBM HR Analytics",
        "missing_attr_err": "File CSV cần có cột 'Attrition' (giá trị Yes/No hoặc 1/0) để huấn luyện mô hình.",
        "err_prefix": "Lỗi khi xử lý file CSV: {err}",
        "page_title": "Hệ Thống Giữ Chân Nhân Viên - IBM HR Analytics",
        "page_subtitle": "Ứng dụng Học máy phân tích dữ liệu nhân sự và cảnh báo sớm rủi ro nghỉ việc theo thời gian thực.",
        "tabs": [
            "Dự Đoán Nhân Viên",
            "Phân Tích Khám Phá Dữ Liệu",
            "Đánh Giá Mô Hình"
        ],
        "input_subheader": "Nhập thông tin hồ sơ nhân viên",
        "sec1": "**1. Thông tin cá nhân & Vị trí**",
        "age": "Độ tuổi",
        "gender": "Giới tính",
        "marital": "Tình trạng hôn nhân",
        "dept": "Phòng ban",
        "job_role": "Chức danh",
        "travel": "Tần suất công tác",
        "distance": "Khoảng cách từ nhà đến công ty (km)",
        "sec2": "**2. Đãi ngộ, Tăng ca & Thâm niên**",
        "income": "Thu nhập hàng tháng (USD)",
        "overtime": "Làm thêm giờ",
        "stock": "Mức quyền chọn cổ phiếu (0 - 3)",
        "job_level": "Cấp bậc công việc (1 - 5)",
        "tot_years": "Tổng số năm kinh nghiệm",
        "comp_years": "Số năm tại công ty",
        "mgr_years": "Số năm làm với quản lý hiện tại",
        "sec3": "**3. Khảo sát mức độ hài lòng (1 - 4)**",
        "job_sat": "Hài lòng công việc",
        "env_sat": "Hài lòng môi trường làm việc",
        "rel_sat": "Hài lòng đồng nghiệp",
        "wlb": "Cân bằng công việc - cuộc sống",
        "job_inv": "Mức độ gắn kết công việc",
        "edu": "Trình độ học vấn",
        "edu_labels": {
            1: "1 - Dưới Đại học",
            2: "2 - Cao đẳng",
            3: "3 - Cử nhân",
            4: "4 - Thạc sĩ",
            5: "5 - Tiến sĩ"
        },
        "edu_field": "Chuyên ngành đào tạo",
        "res_subheader": "Kết Quả Phân Tích & Dự Báo",
        "m_prob": "Xác suất nghỉ việc",
        "m_pred": "Kết luận (Ngưỡng {th:.2f})",
        "yes_lbl": "NGHỈ VIỆC",
        "no_lbl": "Ở LẠI",
        "m_sat": "Điểm hài lòng tổng hợp",
        "m_inc_yr": "Lương / Năm kinh nghiệm",
        "alert_high": "Báo động đỏ! CV của nhân viên này đang được đánh bóng và sẵn sàng gửi đi khắp nơi rồi kìa. HR mang ngay trà sữa, ngày nghỉ bù hoặc mức lương mới ra giữ người gấp trước khi phải mở lại tin tuyển dụng!",
        "alert_mid": "Hơi rung lắc nhẹ rồi đây! Chưa thấy đơn xin nghỉ đâu nhưng bắt đầu thấy dấu hiệu 'ngó nghiêng' rồi. Quản lý trực tiếp nên rủ trao đổi 1-1 xem nhân viên có đang bị quá tải hoặc thiếu động lực không nhé.",
        "alert_low": "Tín hiệu xanh mướt! Nhân viên này đang khá ổn định và gắn bó với công ty. Duy trì đãi ngộ đều tay và ghi nhận đúng lúc là giữ chân ngon lành!",
        "sim_ot": "Giả lập nhanh: Nếu ngừng tăng ca, xác suất nghỉ việc ước tính đổi từ {p_old:.2f}% xuống còn {p_new:.2f}% (chênh lệch {diff:+.2f}%).",
        "eda_subheader": "Tổng quan dữ liệu nhân sự ({rows:,} nhân viên)",
        "k1": "Tổng số nhân viên",
        "k2": "Tỷ lệ nghỉ việc chung",
        "k3": "Thu nhập trung bình",
        "k4": "Tỷ lệ nghỉ nhóm Tăng ca",
        "c1_title": "Tỷ lệ nghỉ việc theo Làm thêm giờ",
        "c2_title": "Tỷ lệ nghỉ việc (%) theo Chức danh",
        "c2_xlabel": "Tỷ lệ (%)",
        "c1_xlabel": "Làm thêm giờ",
        "legend_title": "Trạng thái",
        "ml_subheader": "Bảng so sánh hiệu năng các mô hình Học máy trên tập kiểm thử ({n} mẫu)",
        "col_algo": "Thuật toán",
        "col_acc": "Độ chính xác tổng thể",
        "col_prec": "Độ chính xác dương tính",
        "col_rec": "Độ phủ (Bắt đúng nghỉ việc)",
        "col_f1": "Điểm F1",
        "col_auc": "Chỉ số ROC-AUC",
        "cm_title": "Ma trận nhầm lẫn - Hồi quy Logistic (Ngưỡng = {th:.2f})",
        "cm_xlabel": "Dự đoán",
        "cm_ylabel": "Thực tế",
        "cm_xticks": ["Ở lại (0)", "Nghỉ việc (1)"],
        "cm_yticks": ["Ở lại (0)", "Nghỉ việc (1)"]
    },
    "en": {
        "sidebar_title": "System Configuration",
        "threshold_label": "Decision Threshold",
        "threshold_help": "Lower to 0.35 for higher early-warning recall; raise to 0.60 for balanced precision.",
        "preset_label": "Quick Load Sample Profile:",
        "presets": [
            "Custom Input",
            "High Risk Profile (Young Sales Rep, Overtime)",
            "Low Risk Profile (Research Director)"
        ],
        "upload_header": "Upload Another CSV to Analyze",
        "upload_label": "Choose HR CSV file",
        "upload_help": "Upload another CSV containing an Attrition column to retrain and analyze.",
        "uploading_msg": "Analyzing: {name} ({rows} rows)",
        "default_data_msg": "Using default dataset: IBM HR Analytics",
        "missing_attr_err": "CSV file must contain an 'Attrition' column (Yes/No or 1/0) to train models.",
        "err_prefix": "Error processing CSV file: {err}",
        "page_title": "Employee Retention System - IBM HR Analytics",
        "page_subtitle": "Machine learning application for HR data analysis and real-time employee attrition early warning.",
        "tabs": [
            "AI Predictor",
            "EDA Dashboard",
            "Model Evaluation"
        ],
        "input_subheader": "Enter Employee Profile Details",
        "sec1": "**1. Personal & Role Information**",
        "age": "Age",
        "gender": "Gender",
        "marital": "Marital Status",
        "dept": "Department",
        "job_role": "Job Role",
        "travel": "Business Travel",
        "distance": "Distance From Home",
        "sec2": "**2. Compensation, Overtime & Tenure**",
        "income": "Monthly Income (USD)",
        "overtime": "OverTime",
        "stock": "Stock Option Level (0 - 3)",
        "job_level": "Job Level (1 - 5)",
        "tot_years": "Total Working Years",
        "comp_years": "Years At Company",
        "mgr_years": "Years With Current Manager",
        "sec3": "**3. Satisfaction Survey (1 - 4)**",
        "job_sat": "Job Satisfaction",
        "env_sat": "Environment Satisfaction",
        "rel_sat": "Relationship Satisfaction",
        "wlb": "Work-Life Balance",
        "job_inv": "Job Involvement",
        "edu": "Education",
        "edu_labels": {
            1: "1 - Below College",
            2: "2 - College",
            3: "3 - Bachelor",
            4: "4 - Master",
            5: "5 - Doctor"
        },
        "edu_field": "Education Field",
        "res_subheader": "Analysis & Prediction Results",
        "m_prob": "Attrition Probability",
        "m_pred": "Prediction (Threshold {th:.2f})",
        "yes_lbl": "LEAVE (Yes)",
        "no_lbl": "STAY (No)",
        "m_sat": "Overall Satisfaction",
        "m_inc_yr": "Income / Exp Year",
        "alert_high": "Red alert! This employee's resume is practically polished and ready to hit every job board. HR should bring coffee, comp time, or a retention offer right away before opening a new hiring requisition!",
        "alert_mid": "Mild tremor detected! No resignation letter yet, but signs of wandering eyes are showing. Direct managers should schedule a 1-on-1 check-in to spot workload burnout or motivation gaps early.",
        "alert_low": "Green light all the way! This employee looks steady and well-engaged with the company. Keep consistent rewards and timely recognition to maintain retention.",
        "sim_ot": "Quick What-If: If OverTime is switched to No, estimated attrition probability shifts from {p_old:.2f}% to {p_new:.2f}% ({diff:+.2f}%).",
        "eda_subheader": "HR Dataset Overview ({rows:,} employees)",
        "k1": "Total Employees",
        "k2": "Overall Attrition Rate",
        "k3": "Average Monthly Income",
        "k4": "OverTime Attrition Rate",
        "c1_title": "Attrition Count by OverTime",
        "c2_title": "Attrition Rate (%) by Job Role",
        "c2_xlabel": "Attrition Rate (%)",
        "c1_xlabel": "OverTime",
        "legend_title": "Attrition",
        "ml_subheader": "Model Performance Comparison on Test Set ({n} samples)",
        "col_algo": "Algorithm",
        "col_acc": "Accuracy",
        "col_prec": "Precision",
        "col_rec": "Recall",
        "col_f1": "F1-Score",
        "col_auc": "ROC-AUC",
        "cm_title": "Confusion Matrix - Logistic Regression (Threshold = {th:.2f})",
        "cm_xlabel": "Predicted",
        "cm_ylabel": "Actual",
        "cm_xticks": ["Stay (0)", "Leave (1)"],
        "cm_yticks": ["Stay (0)", "Leave (1)"]
    }
}

def fmt_val(val, lang):
    mapping = VALUE_LABELS_VI if lang == "vi" else VALUE_LABELS_EN
    return mapping.get(str(val), str(val))

DEFAULT_FILLS = {
    'Age': 35, 'MonthlyIncome': 5000, 'DistanceFromHome': 8,
    'TotalWorkingYears': 10, 'YearsAtCompany': 5, 'YearsInCurrentRole': 3,
    'YearsSinceLastPromotion': 1, 'YearsWithCurrManager': 3,
    'EnvironmentSatisfaction': 3, 'JobSatisfaction': 3,
    'RelationshipSatisfaction': 3, 'WorkLifeBalance': 3, 'JobInvolvement': 3,
    'JobLevel': 2, 'StockOptionLevel': 1, 'Education': 3,
    'DailyRate': 802, 'HourlyRate': 66, 'MonthlyRate': 14235,
    'NumCompaniesWorked': 2, 'PercentSalaryHike': 14, 'PerformanceRating': 3,
    'TrainingTimesLastYear': 3, 'BusinessTravel': 'Travel_Rarely',
    'Department': 'Research & Development', 'EducationField': 'Life Sciences',
    'Gender': 'Male', 'JobRole': 'Research Scientist',
    'MaritalStatus': 'Married', 'OverTime': 'No'
}

def prepare_hr_dataframe(raw_df: pd.DataFrame) -> pd.DataFrame:
    df = raw_df.copy()
    # Normalize header whitespace so common CSV export quirks do not create
    # duplicate-looking columns such as "Age ".
    df.columns = [str(col).strip() for col in df.columns]
    if df.columns.duplicated().any():
        duplicates = df.columns[df.columns.duplicated()].tolist()
        raise ValueError(f"Duplicate column names after trimming whitespace: {duplicates}")

    drop_cols = [c for c in ['EmployeeCount', 'Over18', 'StandardHours', 'EmployeeNumber'] if c in df.columns]
    if drop_cols:
        df.drop(columns=drop_cols, inplace=True)

    for col, default_val in DEFAULT_FILLS.items():
        if col not in df.columns:
            df[col] = default_val
        elif pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median() if not df[col].dropna().empty else default_val)
        else:
            df[col] = df[col].fillna(default_val).astype(str)

    df['OverallSatisfaction'] = (
        df['EnvironmentSatisfaction'] + df['JobSatisfaction'] +
        df['RelationshipSatisfaction'] + df['WorkLifeBalance']
    ) / 4.0
    df['LoyaltyRatio'] = df['YearsAtCompany'] / (df['TotalWorkingYears'] + 1)
    df['IncomePerYearExp'] = df['MonthlyIncome'] / (df['TotalWorkingYears'] + 1)
    df['PromotionGapRatio'] = df['YearsSinceLastPromotion'] / (df['YearsAtCompany'] + 1)
    return df

@st.cache_data
def load_default_data():
    raw_df = pd.read_csv('WA_Fn-UseC_-HR-Employee-Attrition.csv')
    return prepare_hr_dataframe(raw_df)

@st.cache_data
def load_uploaded_data(file_bytes: bytes):
    raw_df = pd.read_csv(io.BytesIO(file_bytes))
    return prepare_hr_dataframe(raw_df)

@st.cache_resource
def train_models(df: pd.DataFrame):
    df_ml = df.copy()
    if 'Attrition' not in df_ml.columns:
        raise ValueError("CSV must contain 'Attrition' column.")

    labels = df_ml['Attrition'].astype('string').str.strip().str.casefold()
    label_map = {'no': 0, 'yes': 1, '0': 0, '1': 1, 'false': 0, 'true': 1}
    mapped_labels = labels.map(label_map)
    invalid_labels = sorted(labels[mapped_labels.isna() & labels.notna()].unique())
    if invalid_labels:
        raise ValueError(
            "Attrition values must be Yes/No or 1/0. Invalid values: "
            f"{invalid_labels[:10]}"
        )
    df_ml['Attrition'] = mapped_labels
    df_ml = df_ml.dropna(subset=['Attrition'])
    if df_ml.empty or df_ml['Attrition'].nunique() != 2:
        raise ValueError("Attrition must contain both classes (Yes and No) after removing empty values.")
    df_ml['Attrition'] = df_ml['Attrition'].astype(int)
    class_counts = df_ml['Attrition'].value_counts()
    if class_counts.min() < 2:
        raise ValueError("At least two rows from each Attrition class are required for a stratified train/test split.")

    df_ml = pd.get_dummies(df_ml, drop_first=True)

    X = df_ml.drop('Attrition', axis=1)
    y = df_ml['Attrition']

    if X.empty:
        raise ValueError("CSV must contain at least one usable feature besides Attrition.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    train_df = pd.DataFrame(X_train_scaled, columns=X.columns)
    train_df['Attrition'] = y_train.values
    df_maj = train_df[train_df['Attrition'] == 0]
    df_min = train_df[train_df['Attrition'] == 1]

    if len(df_min) > 0 and len(df_maj) > 0:
        df_min_up = resample(df_min, replace=True, n_samples=len(df_maj), random_state=42)
        train_bal = pd.concat([df_maj, df_min_up])
        X_train_res = train_bal.drop('Attrition', axis=1).values
        y_train_res = train_bal['Attrition'].values
    else:
        X_train_res, y_train_res = X_train_scaled, y_train.values

    models = {
        "Logistic Regression (Tuned C=0.1)": LogisticRegression(C=0.1, penalty='l2', solver='liblinear', max_iter=1000, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=150, learning_rate=0.05, max_depth=3, random_state=42),
        "SVM (RBF Kernel)": SVC(kernel='rbf', C=1.0, probability=True, random_state=42)
    }

    eval_rows = []
    for name, m in models.items():
        m.fit(X_train_res, y_train_res)
        yp = m.predict(X_test_scaled)
        yprob = m.predict_proba(X_test_scaled)[:, 1]
        eval_rows.append({
            "algo": name,
            "acc": round(accuracy_score(y_test, yp), 4),
            "prec": round(precision_score(y_test, yp, zero_division=0), 4),
            "rec": round(recall_score(y_test, yp, zero_division=0), 4),
            "f1": round(f1_score(y_test, yp, zero_division=0), 4),
            "auc": round(roc_auc_score(y_test, yprob), 4)
        })

    return models["Logistic Regression (Tuned C=0.1)"], scaler, list(X.columns), pd.DataFrame(eval_rows), (X_test_scaled, y_test)

# Sidebar
if "lang_choice" not in st.session_state:
    st.session_state.lang_choice = "vi"

st.sidebar.title(I18N[st.session_state.lang_choice]["sidebar_title"])

lang_choice = st.sidebar.radio(
    "Ngôn ngữ" if st.session_state.lang_choice == "vi" else "Language",
    options=["vi", "en"],
    format_func=lambda code: "Tiếng Việt" if code == "vi" else "English",
    horizontal=True,
    key="lang_choice"
)
t = I18N[lang_choice]

threshold = st.sidebar.slider(
    t["threshold_label"],
    min_value=0.25, max_value=0.75, value=0.50, step=0.05,
    help=t["threshold_help"]
)

preset_idx = st.sidebar.selectbox(
    t["preset_label"],
    options=[0, 1, 2],
    format_func=lambda idx: t["presets"][idx]
)

st.sidebar.divider()
st.sidebar.markdown(f"**{t['upload_header']}**")
uploaded_csv = st.sidebar.file_uploader(
    t["upload_label"],
    type=["csv"],
    help=t["upload_help"]
)

try:
    if uploaded_csv is not None:
        df = load_uploaded_data(uploaded_csv.getvalue())
        st.sidebar.success(t["uploading_msg"].format(name=uploaded_csv.name, rows=len(df)))
    else:
        df = load_default_data()
        st.sidebar.caption(t["default_data_msg"])

    best_model, scaler, feature_cols, raw_eval_df, (X_test_scaled, y_test) = train_models(df)
except Exception as e:
    st.error(t["err_prefix"].format(err=e))
    st.stop()

st.title(t["page_title"])
st.markdown(t["page_subtitle"])

tab1, tab2, tab3 = st.tabs(t["tabs"])

with tab1:
    st.subheader(t["input_subheader"])

    if preset_idx == 1:
        d_age, d_income, d_ot, d_dept, d_role, d_marital = 24, 2200, "Yes", "Sales", "Sales Representative", "Single"
        d_travel, d_dist, d_tot_yr, d_comp_yr, d_curr_yr, d_mgr_yr, d_promo_yr = "Travel_Frequently", 22, 2, 1, 1, 0, 0
        d_stock, d_lvl, d_js, d_es, d_rs, d_wlb, d_ji = 0, 1, 1, 1, 2, 1, 2
    elif preset_idx == 2:
        d_age, d_income, d_ot, d_dept, d_role, d_marital = 42, 13500, "No", "Research & Development", "Research Director", "Married"
        d_travel, d_dist, d_tot_yr, d_comp_yr, d_curr_yr, d_mgr_yr, d_promo_yr = "Travel_Rarely", 4, 18, 12, 7, 6, 2
        d_stock, d_lvl, d_js, d_es, d_rs, d_wlb, d_ji = 2, 3, 4, 4, 4, 3, 3
    else:
        d_age, d_income, d_ot, d_dept, d_role, d_marital = 32, 4800, "No", "Research & Development", "Research Scientist", "Married"
        d_travel, d_dist, d_tot_yr, d_comp_yr, d_curr_yr, d_mgr_yr, d_promo_yr = "Travel_Rarely", 8, 8, 5, 3, 3, 1
        d_stock, d_lvl, d_js, d_es, d_rs, d_wlb, d_ji = 1, 2, 3, 3, 3, 3, 3

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(t["sec1"])
        age = st.slider(t["age"], 18, 60, d_age)
        gender = st.selectbox(
            t["gender"],
            options=["Male", "Female"],
            format_func=lambda x: fmt_val(x, lang_choice)
        )
        marital = st.selectbox(
            t["marital"],
            options=["Single", "Married", "Divorced"],
            index=["Single", "Married", "Divorced"].index(d_marital),
            format_func=lambda x: fmt_val(x, lang_choice)
        )
        dept_options = sorted(df['Department'].unique()) if 'Department' in df.columns else ["Sales", "Research & Development", "Human Resources"]
        dept_idx = dept_options.index(d_dept) if d_dept in dept_options else 0
        dept = st.selectbox(
            t["dept"],
            options=dept_options,
            index=dept_idx,
            format_func=lambda x: fmt_val(x, lang_choice)
        )
        roles = sorted(df['JobRole'].unique()) if 'JobRole' in df.columns else ["Sales Representative", "Research Director"]
        role_idx = roles.index(d_role) if d_role in roles else 0
        job_role = st.selectbox(
            t["job_role"],
            options=roles,
            index=role_idx,
            format_func=lambda x: fmt_val(x, lang_choice)
        )
        travel = st.selectbox(
            t["travel"],
            options=["Non-Travel", "Travel_Rarely", "Travel_Frequently"],
            index=["Non-Travel", "Travel_Rarely", "Travel_Frequently"].index(d_travel),
            format_func=lambda x: fmt_val(x, lang_choice)
        )
        distance = st.slider(t["distance"], 1, 30, d_dist)

    with col2:
        st.markdown(t["sec2"])
        income = st.number_input(t["income"], 1000, 20000, d_income, step=100)
        overtime = st.radio(
            t["overtime"],
            options=["No", "Yes"],
            index=["No", "Yes"].index(d_ot),
            horizontal=True,
            format_func=lambda x: fmt_val(x, lang_choice)
        )
        stock = st.selectbox(t["stock"], [0, 1, 2, 3], index=d_stock)
        job_level = st.selectbox(t["job_level"], [1, 2, 3, 4, 5], index=d_lvl-1)
        tot_years = st.slider(t["tot_years"], 0, 40, d_tot_yr)
        comp_years = st.slider(t["comp_years"], 0, 40, min(d_comp_yr, tot_years))
        mgr_years = st.slider(t["mgr_years"], 0, 20, min(d_mgr_yr, comp_years))

    with col3:
        st.markdown(t["sec3"])
        job_sat = st.slider(t["job_sat"], 1, 4, min(d_js, 4))
        env_sat = st.slider(t["env_sat"], 1, 4, min(d_es, 4))
        rel_sat = st.slider(t["rel_sat"], 1, 4, min(d_rs, 4))
        wlb = st.slider(t["wlb"], 1, 4, min(d_wlb, 4))
        job_inv = st.slider(t["job_inv"], 1, 4, min(d_ji, 4))
        edu = st.selectbox(
            t["edu"],
            options=[1, 2, 3, 4, 5],
            index=2,
            format_func=lambda x: t["edu_labels"][x]
        )
        edu_fields = sorted(df['EducationField'].unique()) if 'EducationField' in df.columns else ["Life Sciences"]
        edu_field = st.selectbox(
            t["edu_field"],
            options=edu_fields,
            format_func=lambda x: fmt_val(x, lang_choice)
        )

    emp_dict = {
        'Age': age, 'BusinessTravel': travel, 'DailyRate': 802,
        'Department': dept, 'DistanceFromHome': distance, 'Education': edu,
        'EducationField': edu_field, 'EnvironmentSatisfaction': env_sat, 'Gender': gender,
        'HourlyRate': 66, 'JobInvolvement': job_inv, 'JobLevel': job_level,
        'JobRole': job_role, 'JobSatisfaction': job_sat, 'MaritalStatus': marital,
        'MonthlyIncome': income, 'MonthlyRate': 14235, 'NumCompaniesWorked': 2,
        'OverTime': overtime, 'PercentSalaryHike': 14, 'PerformanceRating': 3,
        'RelationshipSatisfaction': rel_sat, 'StockOptionLevel': stock, 'TotalWorkingYears': tot_years,
        'TrainingTimesLastYear': 3, 'WorkLifeBalance': wlb, 'YearsAtCompany': comp_years,
        'YearsInCurrentRole': min(d_curr_yr, comp_years), 'YearsSinceLastPromotion': min(d_promo_yr, comp_years),
        'YearsWithCurrManager': mgr_years
    }

    # Start from representative values for every uploaded feature, then
    # override fields entered in the form. This keeps inference aligned with
    # the columns used to train the model when a CSV has extra fields.
    emp_dict_full = {}
    for col in df.columns:
        if col == 'Attrition':
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            emp_dict_full[col] = df[col].median() if df[col].notna().any() else 0
        else:
            modes = df[col].dropna().mode()
            emp_dict_full[col] = modes.iloc[0] if not modes.empty else ''
    emp_dict_full.update(emp_dict)
    emp_df = pd.DataFrame([emp_dict_full])
    emp_df['OverallSatisfaction'] = (env_sat + job_sat + rel_sat + wlb) / 4.0
    emp_df['LoyaltyRatio'] = comp_years / (tot_years + 1)
    emp_df['IncomePerYearExp'] = income / (tot_years + 1)
    emp_df['PromotionGapRatio'] = emp_df['YearsSinceLastPromotion'] / (comp_years + 1)

    emp_encoded = pd.get_dummies(emp_df)
    emp_aligned = emp_encoded.reindex(columns=feature_cols, fill_value=0)
    emp_scaled = scaler.transform(emp_aligned)

    prob = best_model.predict_proba(emp_scaled)[0, 1]
    pred = int(prob >= threshold)

    st.divider()
    st.subheader(t["res_subheader"])
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(t["m_prob"], f"{prob*100:.2f}%")
    m2.metric(t["m_pred"].format(th=threshold), t["yes_lbl"] if pred == 1 else t["no_lbl"])
    m3.metric(t["m_sat"], f"{emp_df['OverallSatisfaction'].iloc[0]:.2f} / 4.0")
    m4.metric(t["m_inc_yr"], f"${emp_df['IncomePerYearExp'].iloc[0]:,.0f}")

    if prob >= 0.60:
        st.error(t["alert_high"])
    elif prob >= 0.35:
        st.warning(t["alert_mid"])
    else:
        st.success(t["alert_low"])

    if overtime == "Yes":
        emp_no_ot = emp_df.iloc[0].to_dict()
        emp_no_ot["OverTime"] = "No"
        df_no_ot = pd.DataFrame([emp_no_ot])
        df_no_ot["OverallSatisfaction"] = emp_df["OverallSatisfaction"].iloc[0]
        df_no_ot["LoyaltyRatio"] = emp_df["LoyaltyRatio"].iloc[0]
        df_no_ot["IncomePerYearExp"] = emp_df["IncomePerYearExp"].iloc[0]
        df_no_ot["PromotionGapRatio"] = emp_df["PromotionGapRatio"].iloc[0]
        enc_no_ot = pd.get_dummies(df_no_ot).reindex(columns=feature_cols, fill_value=0)
        prob_no_ot = best_model.predict_proba(scaler.transform(enc_no_ot))[0, 1]
        giam_pct = (prob - prob_no_ot) * 100
        st.info(t["sim_ot"].format(p_old=prob*100, p_new=prob_no_ot*100, diff=giam_pct))

with tab2:
    st.subheader(t["eda_subheader"].format(rows=len(df)))
    attr_series = df['Attrition'].astype(str).str.strip()
    is_yes = attr_series.isin(['Yes', '1'])

    k1, k2, k3, k4 = st.columns(4)
    k1.metric(t["k1"], f"{len(df):,}")
    k2.metric(t["k2"], f"{is_yes.mean()*100:.2f}%")
    k3.metric(t["k3"], f"${df['MonthlyIncome'].mean():,.0f}")
    ot_yes_mask = df['OverTime'].astype(str).str.strip() == 'Yes'
    ot_rate = (is_yes[ot_yes_mask].mean() * 100) if ot_yes_mask.any() else 0.0
    k4.metric(t["k4"], f"{ot_rate:.2f}%")

    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots(figsize=(7, 4))
        plot_df = df.copy()
        plot_df['OverTime_disp'] = plot_df['OverTime'].apply(lambda x: fmt_val(x, lang_choice))
        plot_df['Attrition_disp'] = plot_df['Attrition'].apply(lambda x: fmt_val(x, lang_choice))
        sns.countplot(x='OverTime_disp', hue='Attrition_disp', data=plot_df, ax=ax, palette='Set1')
        ax.set_title(t["c1_title"])
        ax.set_xlabel(t["c1_xlabel"])
        ax.set_ylabel(t["k1"])
        ax.legend(title=t["legend_title"])
        st.pyplot(fig)
    with c2:
        fig, ax = plt.subplots(figsize=(7, 4))
        ct = pd.crosstab(df['JobRole'], is_yes, normalize='index')
        yes_col = True if True in ct.columns else ct.columns[-1]
        role_attr = (ct[yes_col] * 100).sort_values(ascending=False)
        y_labels = [fmt_val(r, lang_choice) for r in role_attr.index]
        sns.barplot(x=role_attr.values, y=y_labels, hue=y_labels, ax=ax, palette='flare', legend=False)
        ax.set_title(t["c2_title"])
        ax.set_xlabel(t["c2_xlabel"])
        ax.set_ylabel(t["job_role"])
        st.pyplot(fig)

with tab3:
    st.subheader(t["ml_subheader"].format(n=len(y_test)))
    disp_eval_df = raw_eval_df.rename(columns={
        "algo": t["col_algo"],
        "acc": t["col_acc"],
        "prec": t["col_prec"],
        "rec": t["col_rec"],
        "f1": t["col_f1"],
        "auc": t["col_auc"]
    })
    st.dataframe(disp_eval_df, width='stretch')

    y_pred_test = (best_model.predict_proba(X_test_scaled)[:, 1] >= threshold).astype(int)
    cm = confusion_matrix(y_test, y_pred_test)
    fig, ax = plt.subplots(figsize=(5, 3.5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                xticklabels=t["cm_xticks"], yticklabels=t["cm_yticks"])
    ax.set_title(t["cm_title"].format(th=threshold))
    ax.set_xlabel(t["cm_xlabel"])
    ax.set_ylabel(t["cm_ylabel"])
    st.pyplot(fig)
