"""
Streamlit web application for adqia.
Upload CSV, run analysis, and view results interactively.
"""

import streamlit as st
import pandas as pd
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.orchestrator import Orchestrator
from src.tools import report_tool

# Import components from the same directory
from components import (
    display_dataset_info,
    display_schema,
    display_qa_results,
    display_anomaly_results,
    display_insights,
    display_chat_interface,
    create_download_button
)


# Page configuration
st.set_page_config(
    page_title="adqia - Auto Data QA",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main Streamlit app function."""
    
    # Header
    st.markdown('<div class="main-header">📊 adqia</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Auto Data QA & Insight Agent</div>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Settings")
    use_llm = st.sidebar.checkbox("Enable LLM Insights (requires API key)", value=False)
    z_threshold = st.sidebar.slider("Outlier Z-Score Threshold", 1.0, 5.0, 3.0, 0.1)

    # Show Gemini status based on environment and user choice
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        if use_llm:
            st.sidebar.success("✅ Gemini LLM: ENABLED")
        else:
            st.sidebar.info("ℹ️ Gemini LLM: Available (check box to enable)")
    else:
        st.sidebar.warning("⚠️ Gemini LLM: DISABLED (GEMINI_API_KEY not set)")
    
    st.sidebar.markdown("---")
    st.sidebar.info(
        "Upload a CSV or Excel file to automatically analyze data quality, "
        "detect anomalies, and generate actionable insights."
    )
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload Data File (CSV or Excel)",
        type=['csv', 'xlsx', 'xls'],
        help="Select a CSV or Excel file to analyze"
    )
    
    # Use sample file option
    use_sample = st.checkbox("Use sample data (sample_sales.csv)", value=False)
    
    # Determine which file to use
    filepath = None
    
    if use_sample:
        sample_path = os.path.join("data", "sample_sales.csv")
        if os.path.exists(sample_path):
            filepath = sample_path
            st.info(f"Using sample file: {sample_path}")
        else:
            st.error("Sample file not found. Please upload a CSV file.")
    elif uploaded_file is not None:
        # Save uploaded file temporarily
        try:
            # Get file extension from uploaded file name
            file_ext = os.path.splitext(uploaded_file.name)[1]
            temp_path = f"temp_upload{file_ext}"
            with open(temp_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            filepath = temp_path
            st.success(f"File loaded: {uploaded_file.name}")
        except Exception as e:
            st.error(f"Error uploading file: {e}")
    
    # Analysis section - only show if we have a file
    if filepath is not None:
        
        # Preview data
        with st.expander("📄 Preview Data (first 10 rows)"):
            try:
                # Read preview based on file type
                if filepath.lower().endswith('.csv'):
                    preview_df = pd.read_csv(filepath, nrows=10)
                elif filepath.lower().endswith(('.xlsx', '.xls')):
                    preview_df = pd.read_excel(filepath, nrows=10)
                else:
                    st.error("Unsupported file format")
                    return
                st.dataframe(preview_df, use_container_width=True)
            except Exception as e:
                st.error(f"Error reading file: {e}")
                return
        
        # Run analysis button
        if st.button("🚀 Run Analysis", type="primary"):
            
            with st.spinner("Analyzing dataset... This may take a moment."):
                try:
                    # Initialize orchestrator
                    orchestrator = Orchestrator(use_llm=use_llm)
                    
                    # Run analysis
                    results = orchestrator.analyze(
                        filepath=filepath,
                        generate_report=False
                    )
                    
                    # Store results in session state
                    st.session_state['results'] = results
                    st.session_state['filepath'] = filepath
                    
                    st.success("✅ Analysis complete!")
                    
                except Exception as e:
                    st.error(f"❌ Analysis failed: {e}")
                    return
        
        # Display results if available
        if 'results' in st.session_state:
            results = st.session_state['results']
            
            st.markdown("---")
            
            # Display dataset info
            display_dataset_info(results['dataset_info'])
            
            st.markdown("---")
            
            # Create tabs for different sections
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📋 Schema",
                "✅ Quality Assessment",
                "🔎 Anomaly Detection",
                "💡 Insights",
                "💬 Chat with Gemini"
            ])
            
            with tab1:
                display_schema(results['schema'])
                
                # Schema changes
                if results.get('schema_changes', {}).get('is_changed'):
                    st.warning("⚠️ Schema changes detected from previous run")
                    changes = results['schema_changes']
                    if changes.get('added_columns'):
                        st.write(f"**Added:** {', '.join(changes['added_columns'])}")
                    if changes.get('removed_columns'):
                        st.write(f"**Removed:** {', '.join(changes['removed_columns'])}")
            
            with tab2:
                display_qa_results(results['qa_results'])
            
            with tab3:
                # Load DataFrame for plotting
                filepath = st.session_state['filepath']
                if filepath.lower().endswith('.csv'):
                    df = pd.read_csv(filepath)
                elif filepath.lower().endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(filepath)
                display_anomaly_results(results['anomaly_results'], df)
            
            with tab4:
                display_insights(
                    results['insights'],
                    results.get('recommendations', [])
                )
            
            with tab5:
                # Chat interface
                filepath = st.session_state['filepath']
                if filepath.lower().endswith('.csv'):
                    df = pd.read_csv(filepath)
                elif filepath.lower().endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(filepath)
                sample_data = df.head(5).to_string()
                
                chat_context = {
                    'schema': results['schema'],
                    'qa_results': results['qa_results'],
                    'anomaly_results': results['anomaly_results'],
                    'sample_data': sample_data
                }
                
                # Create a new orchestrator with current use_llm state for chat
                chat_orchestrator = Orchestrator(use_llm=use_llm)
                
                display_chat_interface(
                    chat_orchestrator.insight_agent,
                    chat_context
                )
            
            # Download report section
            st.markdown("---")
            st.subheader("📥 Reports & Export")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Generate Markdown report
                md_report = report_tool.generate_markdown_report(results)
                create_download_button(
                    md_report,
                    "adqia_report.md",
                    "📄 Download Markdown"
                )
            
            with col2:
                # Generate HTML report
                html_report = report_tool.generate_html_report(results)
                st.download_button(
                    label="💾 Download HTML",
                    data=html_report,
                    file_name="adqia_report.html",
                    mime="text/html"
                )
            
            with col3:
                # Preview HTML report in new window
                if st.button("🌐 Preview HTML Report"):
                    st.session_state['show_html_preview'] = True
            
            # Show HTML preview if requested
            if st.session_state.get('show_html_preview', False):
                st.markdown("---")
                st.subheader("📄 HTML Report Preview")
                close_preview = st.button("❌ Close Preview")
                if close_preview:
                    st.session_state['show_html_preview'] = False
                    st.rerun()
                st.components.v1.html(html_report, height=800, scrolling=True)
        
        # Cleanup temp file
        if hasattr(uploaded_file, 'read') and os.path.exists("temp_upload.csv"):
            try:
                os.remove("temp_upload.csv")
            except:
                pass
    
    else:
        # Welcome message
        st.info("👆 Upload a CSV file or use the sample data to get started")
        
        st.markdown("### Features")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🔍 Data Quality**")
            st.write("Detect missing values, duplicates, and data integrity issues")
        
        with col2:
            st.markdown("**📊 Anomaly Detection**")
            st.write("Identify outliers using statistical methods")
        
        with col3:
            st.markdown("**💡 Insights**")
            st.write("Generate actionable recommendations for data cleaning")


if __name__ == "__main__":
    main()
