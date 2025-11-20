# ADQIA - Auto Data QA & Insight Agent

**ADQIA** (Automated Data Quality & Insight Agent) is a powerful data quality assurance tool that automatically analyzes CSV and Excel datasets, detects anomalies, and generates actionable insights using AI-powered analysis with Google Gemini integration.

## ✨ Features

### Core Capabilities
- 📊 **Multi-Format Support**: Analyze CSV and Excel files (.csv, .xlsx, .xls)
- 🔍 **Automated Data Ingestion**: Load files with automatic schema inference
- ✅ **Data Quality Checks**: Detect missing values, duplicate rows, and data type issues
- 🎯 **Anomaly Detection**: Identify outliers using z-score statistical methods
- 🤖 **AI-Powered Insights**: Generate intelligent insights with Google Gemini AI
- 💬 **Interactive Chat**: Ask questions about your data using Gemini
- 📱 **Modern Web UI**: Beautiful dark-themed Streamlit interface
- 📄 **Professional Reports**: Export as HTML or Markdown with dark theme

### Advanced Features
- **Dual-Mode Analysis**: Choose between AI-powered (Gemini) or rule-based insights
- **Real-time Metrics**: Track generation time and data source for each insight
- **Schema Evolution Tracking**: Monitor schema changes across multiple runs
- **Visual Analytics**: Distribution plots for anomaly detection
- **Containerized Deployment**: Docker support for easy deployment

## 🏗️ Architecture

```
ADQIA/
├── app/                      # Streamlit web application
│   ├── app.py               # Main application entry
│   └── components.py        # UI components with dark theme
├── src/
│   ├── agents/              # Modular analysis agents
│   │   ├── ingest_agent.py      # CSV/Excel loading & schema inference
│   │   ├── qa_agent.py          # Quality checks (missing, duplicates)
│   │   ├── anomaly_agent.py     # Outlier detection
│   │   └── insight_agent.py     # AI insights + chat with Gemini
│   ├── tools/               # Utility tools
│   │   ├── schema_tool.py       # Schema inference & comparison
│   │   ├── stats_tool.py        # Statistical calculations
│   │   └── report_tool.py       # HTML/Markdown report generation
│   ├── utils/               # Core utilities
│   │   ├── logger.py            # Logging configuration
│   │   └── memory.py            # In-memory data store
│   ├── orchestrator.py      # Main workflow coordinator
│   └── main.py              # CLI entry point
├── data/                    # Sample datasets
├── tests/                   # pytest test suite
├── .streamlit/              # Streamlit configuration
└── Dockerfile              # Container configuration
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Google Gemini API key (optional, for AI features)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/DeveloperDeva/ADQIA.git
cd ADQIA
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables** (optional, for AI features)
```bash
# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

### Running the Application

#### Web Interface (Recommended)
```bash
streamlit run app/app.py
```
Then open http://localhost:8501 in your browser.

#### Command Line Interface
```bash
python src/main.py --file data/sample_sales.csv --llm
```

### Using Docker
```bash
# Build image
docker build -t adqia .

# Run container
docker run -p 8501:8501 -e GEMINI_API_KEY=your_key adqia
```

## 📖 Usage Guide

### Web Interface

1. **Upload Data**
   - Click "Browse files" or use sample data
   - Supports CSV and Excel files

2. **Configure Analysis**
   - Enable/disable AI insights (requires API key)
   - Adjust outlier detection threshold
   - View Gemini status in sidebar

3. **Run Analysis**
   - Click "🚀 Run Analysis"
   - View results in organized tabs:
     - 📋 Schema
     - ✅ Quality Assessment
     - 🔎 Anomaly Detection
     - 💡 Insights (AI or rule-based)
     - 💬 Chat with Gemini

4. **Export Results**
   - Download HTML report (dark theme)
   - Download Markdown report
   - Save JSON results

### Chat with Gemini

Ask questions about your data:
- "What are the main quality issues?"
- "How should I handle missing values?"
- "What patterns do you see in the outliers?"
- "Suggest data cleaning steps"

## 🎨 Features Showcase

### Dark Theme UI
- Professional gradient backgrounds
- Color-coded insights (purple for AI, blue for rules)
- Formatted warnings, success, and info boxes
- Smooth animations and shadows

### AI vs Rule-Based
- **Gemini AI**: Deep analysis with code snippets and business impact
- **Rule-Based**: Fast, reliable pattern detection
- Visual badges show which mode was used
- Generation time displayed for transparency

### Professional Reports
- Dark-themed HTML with modern design
- Responsive tables and cards
- Color-coded metrics (critical/warning/info)
- Source attribution and timing metadata

## 🔧 Configuration

### Streamlit Settings (`.streamlit/config.toml`)
```toml
[server]
headless = true
enableCORS = false
maxUploadSize = 200

[browser]
gatherUsageStats = false
```

### Environment Variables
```bash
GEMINI_API_KEY=your_google_gemini_api_key
```

## 📊 Example Output

### Quality Assessment
- Missing value detection with percentages
- Duplicate row identification
- Data type validation

### Anomaly Detection
- Z-score based outlier detection
- Statistical summaries (mean, std, min, max)
- Distribution visualizations

### AI Insights
```
DATA QUALITY SUMMARY
- Dataset has 18 rows and 7 columns
- 2 quality issues detected requiring attention

REMEDIATION RECOMMENDATIONS
1. Handle missing values in 'region' column (11.11%)
   Code: df['region'].fillna(df['region'].mode()[0], inplace=True)

2. Remove duplicate rows
   Code: df.drop_duplicates(inplace=True)
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_qa.py

# With coverage
pytest --cov=src
```

## 📦 Dependencies

Core:
- `streamlit>=1.28.0` - Web interface
- `pandas>=2.0.0` - Data manipulation
- `numpy>=1.24.0` - Numerical operations
- `openpyxl>=3.1.0` - Excel support

AI:
- `google-generativeai>=0.8.0` - Gemini integration
- `python-dotenv>=1.0.0` - Environment management

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - see LICENSE file for details

## 👨‍💻 Author

**DeveloperDeva**
- GitHub: [@DeveloperDeva](https://github.com/DeveloperDeva)

## 🙏 Acknowledgments

- Google Gemini AI for intelligent insights
- Streamlit for the amazing web framework
- The open-source community

---

**Note**: Ensure you have a valid Gemini API key for AI-powered features. Get yours at [Google AI Studio](https://makersuite.google.com/app/apikey).
