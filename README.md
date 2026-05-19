# 🧠 DataCleaner AI — Premium AI Data Preprocessing Platform

<div align="center">

![DataCleaner AI](https://img.shields.io/badge/DataCleaner-AI%20v2.0%20Pro-8b5cf6?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSI+PHBhdGggZD0iTTMgMTJMMTIgM0wyMSAxMkwxMiAyMUwzIDEyWiIgZmlsbD0iIzhiNWNmNiIvPjwvc3ZnPg==)
![Python](https://img.shields.io/badge/Python-3.9+-3b82f6?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-ec4899?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-10b981?style=for-the-badge)

**The most visually stunning, recruiter-attracting AI data preprocessing platform — built for portfolio, hackathons, and placements.**

[🚀 Live Demo](#) · [📖 Documentation](#features) · [🐛 Report Bug](#) · [⭐ Star this repo](#)

</div>

---

## ✨ What Makes This Special

> "This does NOT look like a student project."

DataCleaner AI is a **startup-grade AI SaaS platform** built with:
- 🎨 **Cinematic glassmorphism UI** — dark mode, neon gradients, floating panels
- 🤖 **8 AI-powered modules** — cleaning, outliers, features, insights, visualization
- ⚡ **One-click auto-clean** — intelligent pipeline with animated workflow
- 📊 **Interactive Plotly charts** — 3D scatter, heatmaps, violin plots, PCA
- 📤 **Professional exports** — CSV, JSON report, PDF report

---

## 🖥️ Screenshots

| Home | Upload | AI Cleaning |
|------|--------|-------------|
| Hero landing page with animated gradient | Drag & drop with instant profiling | Auto-clean pipeline with progress |

| Visualization Lab | Outlier Detection | AI Insights |
|-------------------|-------------------|-------------|
| 6 interactive chart types | Z-Score / IQR / Isolation Forest | Quality score + feature importance |

---

## 🔥 Features

### 📁 AI Dataset Upload Center
- Drag & drop CSV / Excel upload
- Instant dataset profiling (rows, cols, nulls, memory, dtypes)
- Animated quality score ring chart
- Issue detection with severity badges
- 4 built-in sample datasets

### ⚡ AI Cleaning Engine
- AI-generated cleaning suggestions with priority badges
- One-click **Auto Clean** pipeline
- Missing value strategies: auto, mean, median, mode, ffill, bfill, drop, zero
- Duplicate row removal
- Datatype auto-correction
- Constant column removal
- Step-by-step animated workflow

### 📊 Visualization Lab
- 🔥 Correlation heatmap
- 📊 Distribution histograms with violin marginals
- 📦 Box & violin plots
- 🔵 Scatter plots with trendlines
- 🌐 3D scatter plots
- 🎭 Missing value grid heatmap

### 🚨 Outlier Detection System
- **Z-Score** detection with adjustable threshold slider
- **IQR** method with adjustable multiplier
- **Isolation Forest** ML-based anomaly detection
- Live chart updates with red-glow outlier highlighting
- One-click outlier removal

### 🧬 Feature Engineering Studio
- Label Encoding
- One-Hot Encoding (with cardinality warnings)
- StandardScaler / MinMaxScaler / RobustScaler
- PCA dimensionality reduction with explained variance chart
- Live data preview after each transformation

### 🤖 AI Insights Engine
- Dataset quality score (0–100) with circular gauge
- ML problem type prediction (classification/regression/clustering)
- Feature importance proxy bar chart
- Correlation insights with severity levels
- AI-generated natural language dataset summary
- Recommended preprocessing pipeline

### 📈 Before vs After Comparison
- Animated metric delta cards
- Side-by-side quality gauges
- Grouped bar chart comparison
- Column-level null comparison
- Full cleaning operation log

### 📤 Export System
- Download cleaned CSV
- JSON preprocessing report
- PDF report (fpdf2)
- Original dataset download
- Cleaning log export

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/DataCleanerAI.git
cd DataCleanerAI
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```

The app will open at **http://localhost:8501** 🎉

---

## 📁 Project Structure

```
DataCleanerAI/
│
├── app.py                      # 🏠 Main entry point
│
├── components/
│   ├── header.py               # Animated logo navbar
│   └── metrics_cards.py        # Bento-grid metric cards
│
├── pages/
│   ├── home.py                 # Landing page
│   ├── upload_page.py          # Dataset upload center
│   ├── cleaning_engine.py      # AI auto-clean
│   ├── visualization_lab.py    # Interactive charts
│   ├── outlier_detection.py    # Anomaly detection
│   ├── feature_engineering.py  # Encoding / scaling / PCA
│   ├── ai_insights_page.py     # AI insights dashboard
│   ├── before_after.py         # Comparison view
│   └── export.py               # Download / export
│
├── utils/
│   ├── data_profiler.py        # Quality scoring & profiling
│   ├── missing_handler.py      # Imputation strategies
│   ├── outlier_detector.py     # Detection algorithms
│   ├── feature_engineer.py     # Encoding, scaling, PCA
│   └── report_generator.py     # PDF & JSON reports
│
├── styles/
│   └── main.css                # Full glassmorphism theme
│
├── assets/
│   └── sample_datasets/        # Titanic, Housing, Mall, Churn
│
├── requirements.txt
└── README.md
```

---

## 🌐 Deployment

### Streamlit Cloud (Free)
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → select `app.py`
4. Click **Deploy** ✅

### Local Network (Share on LAN)
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

```bash
docker build -t datacleaner-ai .
docker run -p 8501:8501 datacleaner-ai
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| **Python 3.9+** | Core language |
| **Streamlit** | Web framework |
| **Pandas** | Data manipulation |
| **NumPy** | Numerical computing |
| **Plotly** | Interactive visualizations |
| **Scikit-learn** | Isolation Forest, PCA, Scalers |
| **fpdf2** | PDF report generation |
| **Custom CSS** | Glassmorphism UI theme |

---

## 🎨 Design System

| Token | Color | Usage |
|-------|-------|-------|
| Primary | `#8b5cf6` (Purple) | Accents, buttons |
| Secondary | `#06b6d4` (Cyan) | Charts, highlights |
| Warning | `#ec4899` (Pink) | Alerts, danger |
| Success | `#10b981` (Emerald) | Clean state, good |
| Background | `#020818` (Deep Space) | Main background |

---

## 📊 Sample Datasets

| Dataset | Rows | Columns | Type |
|---------|------|---------|------|
| 🚢 Titanic | 891 | 12 | Binary Classification |
| 🏠 Housing Prices | 1460 | 81 | Regression |
| 🛍️ Mall Customers | 200 | 5 | Clustering |
| 📡 Customer Churn | 7043 | 21 | Binary Classification |

---

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first.

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add AmazingFeature'`
4. Push: `git push origin feature/AmazingFeature`
5. Open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built with ❤️ for data scientists, ML engineers, and anyone who wants clean data.**

⭐ **Star this repo if it helped your portfolio!** ⭐

</div>
