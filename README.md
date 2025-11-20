# adqia - Auto Data QA & Insight Agent

**adqia** is an automated data quality assurance and insight generation tool that analyzes CSV datasets, detects anomalies, and produces actionable insights with minimal configuration.

## Features

- **Automated Data Ingestion**: Load CSV files with automatic schema inference
- **Data Quality Checks**: Detect missing values, duplicate rows, and null fractions
- **Anomaly Detection**: Identify outliers using z-score-based statistical methods
- **Insight Generation**: Generate human-readable insights and actionable recommendations
- **Memory Store**: Track schema evolution across multiple runs
- **Interactive UI**: Streamlit-based web interface for easy dataset analysis
- **Report Generation**: Export findings as Markdown/HTML reports

## Architecture

```
adqia/
├── src/
│   ├── agents/          # Modular analysis agents
│   │   ├── ingest_agent.py    # CSV loading & schema inference
│   │   ├── qa_agent.py         # Quality checks (missing, duplicates)
│   │   ├── anomaly_agent.py    # Outlier detection
│   │   └── insight_agent.py    # Generate insights & recommendations
│   ├── tools/           # Utility tools
│   │   ├── schema_tool.py      # Schema inference & comparison
│   │   ├── stats_tool.py       # Statistical calculations
│   │   └── report_tool.py      # Report generation
│   ├── utils/           # Core utilities
│   │   ├── logger.py           # Logging configuration
│   │   └── memory.py           # In-memory data store
│   ├── orchestrator.py  # Main workflow coordinator
│   └── main.py          # CLI entry point
├── app/                 # Streamlit web application
├── tests/               # pytest test suite
├── data/                # Sample datasets
└── notebooks/           # Jupyter notebook demos
```

## Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/adqia.git
cd adqia
```

2. **Create a virtual environment**
```bash
python -m venv .venv
```

3. **Activate the virtual environment**

Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```

Linux/Mac:
```bash
source .venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

Run analysis on a CSV file:
```bash
python src/main.py
```

By default, this analyzes `data/sample_sales.csv`. To analyze a different file, modify the path in `src/main.py`.

### Streamlit Web Interface

Launch the interactive web application:
```bash
streamlit run app/app.py
```

Then open your browser to `http://localhost:8501` and:
1. Upload a CSV file
2. Click "Run Analysis"
3. View QA metrics, anomaly detection results, and generated insights
4. Download the generated report

### Jupyter Notebook

Explore the interactive demo:
```bash
jupyter notebook notebooks/demo.ipynb
```

## Testing

Run the test suite:
```bash
pytest
```

Run tests with verbose output:
```bash
pytest -v
```

Run tests with coverage:
```bash
pytest --cov=src tests/
```

## Docker (Optional)

Build the Docker image:
```bash
docker build -t adqia:latest .
```

Run the Streamlit app in a container:
```bash
docker run -p 8501:8501 adqia:latest
```

## Project Structure Details

### Agents
- **IngestAgent**: Loads CSV files and infers schema
- **QAAgent**: Performs data quality checks
- **AnomalyAgent**: Detects statistical outliers
- **InsightAgent**: Generates human-readable insights

### Tools
- **schema_tool**: Schema inference and change detection
- **stats_tool**: Statistical calculations for QA and anomaly detection
- **report_tool**: Markdown/HTML report generation

### Memory Store
The `MemoryStore` class maintains state across runs, storing the last known schema to detect schema drift.

## Sample Output

```
=== Data Quality Report ===
Missing Values: 
  - price: 2 (12.5%)
  - region: 1 (6.25%)
Duplicate Rows: 1
Outliers Detected: 
  - quantity: 2 outliers found

Insights:
- Dataset contains 2 duplicate rows. Consider removing duplicates.
- Column 'price' has 12.5% missing values. Consider imputation or removal.
- 2 outliers detected in 'quantity'. Review for data entry errors.
```

## Extending adqia

### Adding LLM Integration

The `InsightAgent` includes a stub for LLM integration. To add real LLM calls:

1. Install your LLM library (e.g., `openai`, `google-generativeai`)
2. Add API key to environment variables (never commit credentials!)
3. Replace the `call_llm_stub()` function in `src/agents/insight_agent.py`

Example:
```python
def call_llm_stub(prompt: str) -> str:
    # TODO: Replace with real LLM integration
    # import openai
    # response = openai.ChatCompletion.create(...)
    # return response.choices[0].message.content
    pass
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Roadmap

- [ ] Support for JSON, Parquet, Excel formats
- [ ] Advanced anomaly detection (isolation forest, DBSCAN)
- [ ] LLM-powered insight generation (Gemini, GPT-4)

### Gemini Integration (Optional)

adqia can optionally use Google Gemini (via `google-generativeai`) to produce enhanced insights. This is disabled by default and the project will always fall back to the rule-based insight generator when Gemini is not configured.

To enable Gemini support:

1. Add your API key to a `.env` file in the project root with:

```text
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

2. Install updated dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app (the presence of `GEMINI_API_KEY` and enabling LLM in the UI will attempt to use Gemini):

```bash
streamlit run app/app.py
```

If the key is missing or a Gemini call fails, adqia will safely return the original rule-based insights.
- [ ] Multi-dataset comparison
- [ ] SQL query generation for data cleaning
- [ ] REST API endpoint
- [ ] Scheduled analysis with email reports

## Contact

For questions or issues, please open a GitHub issue.
