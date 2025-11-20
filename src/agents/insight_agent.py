"""
Insight Agent - Generates human-readable insights and recommendations.
Optional integration with Google Gemini (google-generativeai).
If a `GEMINI_API_KEY` environment variable is present and `use_llm=True`,
the agent will attempt to call Gemini. On any failure it will fall back
to the rule-based insight generator.
"""

from typing import Dict, List
import os
from src.utils.logger import get_logger

logger = get_logger(__name__)


def call_llm_stub(prompt: str) -> str:
    """
    Local stub for environments without Gemini configured.
    """
    logger.debug("LLM stub called (no Gemini key present)")
    return "LLM integration not configured. Using fallback insights."


class InsightAgent:
    """
    Agent responsible for generating insights and actionable recommendations
    based on QA and anomaly detection results. Optionally uses Gemini.
    """

    def __init__(self, use_llm: bool = False):
        """
        Initialize the InsightAgent.

        Args:
            use_llm: Whether to attempt to use an LLM for enhanced insights
        """
        self.use_llm = use_llm
        self.gemini_enabled = False
        self.model = None

        # Attempt to enable Gemini if requested
        if self.use_llm:
            try:
                import google.generativeai as genai  # optional dependency

                api_key = os.getenv("GEMINI_API_KEY")
                if api_key:
                    genai.configure(api_key=api_key)
                    # Use gemini-2.5-flash (latest fast model)
                    self.model = genai.GenerativeModel("gemini-2.5-flash")
                    self.gemini_enabled = True
                    logger.info("Gemini LLM enabled for insights (using gemini-2.5-flash).")
                else:
                    self.gemini_enabled = False
                    logger.info("GEMINI_API_KEY not set: using fallback insights.")
            except Exception as e:
                # Any import/config error — disable Gemini and fallback
                self.gemini_enabled = False
                logger.warning(f"Gemini initialization failed; using fallback insights. Error: {e}")
        else:
            logger.info("InsightAgent initialized with LLM disabled (fallback only)")

        logger.info(f"InsightAgent initialized (gemini_enabled={self.gemini_enabled})")

    def _generate_fallback_insights(self, qa_results: Dict, anomaly_results: Dict, schema: Dict[str, str]) -> str:
        """
        Original rule-based insight generator.
        Returns a multi-line string describing data quality issues and recommendations.
        Uses proper text formatting without emoji or special characters.
        """
        insights = []

        # Analyze missing values
        missing = qa_results.get('missing_values', {})
        if missing:
            insights.append("**Missing Values Analysis:**")
            for col, count in missing.items():
                fraction = qa_results.get('null_fraction', {}).get(col, 0)
                percentage = fraction * 100
                insights.append(f"  - Column '{col}' has {count} missing values ({percentage:.2f}%)")

                if percentage > 50:
                    insights.append(f"    WARNING: Over 50% missing. Consider dropping this column.")
                elif percentage > 20:
                    insights.append(f"    WARNING: Significant missing data. Imputation recommended.")
            insights.append("")

        # Analyze duplicates
        duplicates = qa_results.get('duplicate_rows', 0)
        if duplicates > 0:
            insights.append(f"**Duplicate Rows:** {duplicates} duplicate(s) detected.")
            insights.append("  NOTE: Remove duplicates using df.drop_duplicates()")
            insights.append("")

        # Analyze outliers
        outliers = anomaly_results.get('outliers', {})
        if outliers:
            insights.append("**Outlier Detection:**")
            for col, count in outliers.items():
                insights.append(f"  - Column '{col}' has {count} outlier(s)")
                stats = anomaly_results.get('summary_stats', {}).get(col, {})
                if stats:
                    insights.append(f"    Mean: {stats.get('mean', 0):.2f}, Std: {stats.get('std', 0):.2f}")
            insights.append("  NOTE: Review outliers for data entry errors or legitimate extreme values.")
            insights.append("")

        # Schema insights
        insights.append(f"**Schema Overview:** {len(schema)} columns detected")
        numeric_types = sum(1 for dtype in schema.values() if 'int' in dtype or 'float' in dtype)
        insights.append(f"  - Numeric columns: {numeric_types}")
        insights.append(f"  - Categorical columns: {len(schema) - numeric_types}")
        insights.append("")

        # Summary
        if not missing and duplicates == 0 and not outliers:
            insights.append("SUCCESS: Dataset appears clean with no major quality issues detected.")
        else:
            issue_count = len(missing) + (1 if duplicates > 0 else 0) + len(outliers)
            insights.append(f"WARNING: {issue_count} data quality issue(s) detected. See recommendations below.")

        return "\n".join(insights)

    def run(self, qa_results: Dict, anomaly_results: Dict, schema: Dict[str, str]) -> Dict[str, any]:
        """
        Generate human-readable insights from analysis results.

        If Gemini is enabled (and the InsightAgent was created with `use_llm=True`),
        attempt to call Gemini; otherwise return fallback insights.
        
        Returns:
            Dict with 'text', 'source', and 'generation_time' keys
        """
        import time
        logger.info("Generating insights from analysis results")
        
        start_time = time.time()

        # Always compute fallback first
        fallback = self._generate_fallback_insights(qa_results, anomaly_results, schema)

        # If Gemini is not enabled, return fallback immediately
        if not self.gemini_enabled:
            logger.debug("Gemini disabled; returning fallback insights")
            generation_time = time.time() - start_time
            return {
                'text': fallback,
                'source': 'rule-based',
                'generation_time': generation_time
            }

        # Build a prompt for Gemini
        prompt = self._create_llm_prompt(qa_results, anomaly_results, schema)

        try:
            # Call Gemini model
            response = self.model.generate_content(prompt)
            # Access response text safely
            text = getattr(response, 'text', None) or str(response)
            text = text.strip()

            if not text:
                logger.warning("Gemini returned empty text; falling back to rule-based insights")
                generation_time = time.time() - start_time
                return {
                    'text': fallback,
                    'source': 'rule-based',
                    'generation_time': generation_time
                }

            logger.info("Gemini response received successfully")
            generation_time = time.time() - start_time
            return {
                'text': text,
                'source': 'gemini',
                'generation_time': generation_time
            }

        except Exception as e:
            # On any error, log and return fallback
            logger.error(f"Gemini call failed; returning fallback insights. Error: {e}")
            generation_time = time.time() - start_time
            return {
                'text': fallback,
                'source': 'rule-based',
                'generation_time': generation_time
            }

    def generate_recommendations(self, qa_results: Dict, anomaly_results: Dict) -> List[str]:
        """
        Generate actionable recommendations based on results.

        Args:
            qa_results: Results from QAAgent
            anomaly_results: Results from AnomalyAgent

        Returns:
            List of recommendation strings
        """
        recommendations = []

        # Missing value recommendations
        missing = qa_results.get('missing_values', {})
        for col, count in missing.items():
            fraction = qa_results.get('null_fraction', {}).get(col, 0)
            if fraction > 0.5:
                recommendations.append(f"Consider dropping column '{col}' (>50% missing)")
            elif fraction > 0.1:
                recommendations.append(f"Impute missing values in '{col}' using mean/median/mode")

        # Duplicate recommendations
        if qa_results.get('duplicate_rows', 0) > 0:
            recommendations.append("Remove duplicate rows: `df.drop_duplicates(inplace=True)`")

        # Outlier recommendations
        outliers = anomaly_results.get('outliers', {})
        for col in outliers.keys():
            recommendations.append(f"Review outliers in '{col}' - verify data integrity")

        # SQL snippet for data cleaning (example)
        if missing or qa_results.get('duplicate_rows', 0) > 0:
            recommendations.append("SQL cleaning example: `DELETE FROM table WHERE col IS NULL`")

        logger.info(f"Generated {len(recommendations)} recommendations")
        return recommendations

    def chat_with_gemini(self, user_question: str, context: Dict) -> str:
        """
        Allow users to ask questions about their data using Gemini.
        
        Args:
            user_question: User's question
            context: Dictionary with 'schema', 'qa_results', 'anomaly_results', 'sample_data'
        
        Returns:
            Gemini's response as string
        """
        if not self.gemini_enabled:
            return "❌ Gemini chat is not available. Please enable LLM and ensure GEMINI_API_KEY is set."
        
        # Build context-aware prompt
        context_prompt = f"""You are a helpful data analyst assistant. The user has uploaded a dataset with the following characteristics:

Schema: {context.get('schema', {})}
Data Quality Issues: {context.get('qa_results', {})}
Anomalies: {context.get('anomaly_results', {})}

Sample data (first few rows):
{context.get('sample_data', 'Not available')}

User Question: {user_question}

Provide a clear, helpful answer based on the data context above."""
        
        try:
            response = self.model.generate_content(context_prompt)
            text = getattr(response, 'text', None) or str(response)
            return text.strip()
        except Exception as e:
            logger.error(f"Gemini chat failed: {e}")
            return f"❌ Sorry, I couldn't process your question. Error: {str(e)}"

    def _create_llm_prompt(self, qa_results: Dict, anomaly_results: Dict, schema: Dict) -> str:
        """
        Create a prompt for LLM-based insight generation.

        Args:
            qa_results: QA analysis results
            anomaly_results: Anomaly detection results
            schema: Dataset schema

        Returns:
            Formatted prompt string
        """
        prompt = f"""You are an experienced data analyst. Analyze the dataset quality report below and provide a concise, actionable summary.

IMPORTANT FORMATTING RULES:
- Use proper text formatting, NOT emoji or special characters
- Use "WARNING:" instead of ⚠️
- Use "SUCCESS:" instead of ✅
- Use "NOTE:" instead of 💡
- Use standard bullet points with "-" or numbered lists
- Use bold text with **text** for emphasis only
- Write in clear, professional English

Dataset Information:
- Total Columns: {len(schema)}
- Column Types: {dict(list(schema.items())[:10])}

Quality Assessment Results:
- Missing Values: {qa_results.get('missing_values', {})}
- Null Fractions: {qa_results.get('null_fraction', {})}
- Duplicate Rows: {qa_results.get('duplicate_rows', 0)}
- Outliers Detected: {anomaly_results.get('outliers', {})}

Please provide:

1. DATA QUALITY SUMMARY
   - Brief overview of the dataset condition
   - Highlight critical issues that need immediate attention

2. DETAILED FINDINGS
   - Missing data analysis with percentages
   - Duplicate records assessment
   - Outlier patterns and their potential impact

3. ROOT CAUSE ANALYSIS
   - Likely reasons for data quality issues
   - Patterns or systematic problems identified

4. REMEDIATION RECOMMENDATIONS
   - Specific steps to fix each issue
   - Include code snippets (Python/SQL) where applicable
   - Prioritize actions by severity

5. BUSINESS IMPACT
   - How these issues affect data reliability
   - Potential risks if not addressed

Format your response in clear sections with proper headings. Use professional language without emoji or special characters."""
        
        return prompt
