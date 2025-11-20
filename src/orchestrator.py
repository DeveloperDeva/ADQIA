"""
Orchestrator - Coordinates all agents to perform complete data analysis.
"""

import os
from typing import Dict, Any
from src.agents import IngestAgent, QAAgent, AnomalyAgent, InsightAgent
from src.tools import schema_tool, report_tool
from src.utils import MemoryStore, get_logger

logger = get_logger(__name__)


class Orchestrator:
    """
    Main orchestrator that coordinates all analysis agents.
    Manages workflow: Ingest → Schema Check → QA → Anomaly → Insight → Report
    """
    
    def __init__(self, use_llm: bool = False):
        """
        Initialize the orchestrator with all agents.
        
        Args:
            use_llm: Whether to enable LLM-based insights
        """
        self.memory = MemoryStore()
        self.ingest_agent = IngestAgent()
        self.qa_agent = QAAgent()
        self.anomaly_agent = AnomalyAgent()
        self.insight_agent = InsightAgent(use_llm=use_llm)
        
        logger.info("Orchestrator initialized with all agents")
    
    def analyze(self, filepath: str, generate_report: bool = True, 
                report_dir: str = "reports") -> Dict[str, Any]:
        """
        Run complete analysis pipeline on a dataset.
        
        Args:
            filepath: Path to the CSV file to analyze
            generate_report: Whether to generate report files
            report_dir: Directory to save reports
        
        Returns:
            Dictionary containing all analysis results:
            - dataset_info: Basic dataset information
            - schema: Inferred schema
            - schema_changes: Schema change detection results
            - qa_results: Data quality assessment
            - anomaly_results: Anomaly detection results
            - insights: Human-readable insights
            - recommendations: Actionable recommendations
            - report_paths: Paths to generated reports (if generate_report=True)
        """
        logger.info(f"=" * 60)
        logger.info(f"Starting analysis pipeline for: {filepath}")
        logger.info(f"=" * 60)
        
        # Step 1: Ingest data
        logger.info("Step 1: Data Ingestion")
        df, schema = self.ingest_agent.run(filepath)
        
        dataset_info = {
            'filepath': filepath,
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': list(df.columns)
        }
        
        # Step 2: Schema comparison with memory
        logger.info("Step 2: Schema Comparison")
        old_schema = self.memory.get('schema')
        schema_changes = schema_tool.check_schema_changes(old_schema, schema)
        
        # Save new schema to memory
        self.memory.save('schema', schema)
        
        # Step 3: Quality Assessment
        logger.info("Step 3: Quality Assessment")
        qa_results = self.qa_agent.run(df)
        
        # Step 4: Anomaly Detection
        logger.info("Step 4: Anomaly Detection")
        anomaly_results = self.anomaly_agent.run(df)
        
        # Step 5: Insight Generation
        logger.info("Step 5: Insight Generation")
        insights = self.insight_agent.run(qa_results, anomaly_results, schema)
        recommendations = self.insight_agent.generate_recommendations(qa_results, anomaly_results)
        
        # Compile all results
        results = {
            'dataset_info': dataset_info,
            'schema': schema,
            'schema_changes': schema_changes,
            'qa_results': qa_results,
            'anomaly_results': anomaly_results,
            'insights': insights,
            'recommendations': recommendations
        }
        
        # Step 6: Generate Reports
        if generate_report:
            logger.info("Step 6: Report Generation")
            report_paths = report_tool.create_report_bundle(results, output_dir=report_dir)
            results['report_paths'] = report_paths
            logger.info(f"Reports generated: {', '.join(report_paths.keys())}")
        
        logger.info("=" * 60)
        logger.info("Analysis pipeline complete")
        logger.info("=" * 60)
        
        return results
    
    def quick_summary(self, filepath: str) -> str:
        """
        Run analysis and return a quick text summary.
        
        Args:
            filepath: Path to CSV file
        
        Returns:
            Formatted summary string
        """
        results = self.analyze(filepath, generate_report=False)
        
        summary_lines = [
            "=" * 60,
            "QUICK DATA QUALITY SUMMARY",
            "=" * 60,
            f"File: {filepath}",
            f"Rows: {results['dataset_info']['rows']}",
            f"Columns: {results['dataset_info']['columns']}",
            "",
            "Missing Values:",
        ]
        
        missing = results['qa_results'].get('missing_values', {})
        if missing:
            for col, count in missing.items():
                fraction = results['qa_results'].get('null_fraction', {}).get(col, 0)
                summary_lines.append(f"  - {col}: {count} ({fraction*100:.1f}%)")
        else:
            summary_lines.append("  None")
        
        summary_lines.append("")
        summary_lines.append(f"Duplicate Rows: {results['qa_results'].get('duplicate_rows', 0)}")
        
        outliers = results['anomaly_results'].get('outliers', {})
        summary_lines.append(f"Columns with Outliers: {len(outliers)}")
        
        summary_lines.append("")
        summary_lines.append("=" * 60)
        
        return "\n".join(summary_lines)
    
    def get_memory_state(self) -> Dict[str, Any]:
        """
        Get current state of memory store.
        
        Returns:
            Dictionary with memory contents
        """
        return {
            'keys': self.memory.keys(),
            'schema': self.memory.get('schema')
        }
    
    def clear_memory(self) -> None:
        """Clear the memory store."""
        self.memory.clear()
        logger.info("Memory store cleared")
