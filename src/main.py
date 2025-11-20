"""
Main entry point for adqia CLI.
Demonstrates usage of the Orchestrator.
"""

import os
import sys
from dotenv import load_dotenv
from src.orchestrator import Orchestrator
from src.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """
    Main function to run data analysis.
    Analyzes sample_sales.csv by default.
    """
    # Default file path
    default_file = os.path.join("data", "sample_sales.csv")
    
    # Allow file path as command-line argument
    filepath = sys.argv[1] if len(sys.argv) > 1 else default_file
    
    # Check if file exists
    if not os.path.exists(filepath):
        logger.error(f"File not found: {filepath}")
        print(f"Error: File '{filepath}' does not exist.")
        print(f"Usage: python src/main.py [path_to_csv]")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print(" adqia - Auto Data QA & Insight Agent")
    print("=" * 70 + "\n")
    
    # Initialize orchestrator
    # Load environment variables (e.g., GEMINI_API_KEY from .env)
    load_dotenv()

    # Initialize orchestrator
    orchestrator = Orchestrator(use_llm=True)
    
    try:
        # Run analysis
        results = orchestrator.analyze(
            filepath=filepath,
            generate_report=True,
            report_dir="reports"
        )
        
        # Display summary
        print("\n" + "=" * 70)
        print(" ANALYSIS SUMMARY")
        print("=" * 70)
        
        info = results['dataset_info']
        print(f"\nDataset: {info['filepath']}")
        print(f"Rows: {info['rows']}")
        print(f"Columns: {info['columns']}")
        
        # QA Summary
        print("\n--- Data Quality Issues ---")
        qa = results['qa_results']
        
        missing = qa.get('missing_values', {})
        if missing:
            print(f"Missing values in {len(missing)} column(s):")
            for col, count in missing.items():
                frac = qa.get('null_fraction', {}).get(col, 0)
                print(f"  - {col}: {count} ({frac*100:.1f}%)")
        else:
            print("✅ No missing values")
        
        dup = qa.get('duplicate_rows', 0)
        if dup > 0:
            print(f"Duplicate rows: {dup}")
        else:
            print("✅ No duplicate rows")
        
        # Anomaly Summary
        print("\n--- Anomaly Detection ---")
        anomaly = results['anomaly_results']
        outliers = anomaly.get('outliers', {})
        
        if outliers:
            print(f"Outliers detected in {len(outliers)} column(s):")
            for col, count in outliers.items():
                print(f"  - {col}: {count} outlier(s)")
        else:
            print("✅ No outliers detected")
        
        # Insights
        print("\n--- Insights ---")
        print(results['insights'])
        
        # Recommendations
        if results.get('recommendations'):
            print("\n--- Recommendations ---")
            for i, rec in enumerate(results['recommendations'], 1):
                print(f"{i}. {rec}")
        
        # Report paths
        if 'report_paths' in results:
            print("\n--- Generated Reports ---")
            for report_type, path in results['report_paths'].items():
                print(f"  - {report_type.upper()}: {path}")
        
        print("\n" + "=" * 70)
        print(" Analysis Complete!")
        print("=" * 70 + "\n")
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
