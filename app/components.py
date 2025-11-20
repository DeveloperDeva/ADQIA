"""
Streamlit UI components for adqia app.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, Any


def display_dataset_info(info: Dict[str, Any]) -> None:
    """
    Display dataset information in Streamlit.
    
    Args:
        info: Dataset information dictionary
    """
    st.subheader("📊 Dataset Information")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rows", info.get('rows', 'N/A'))
    with col2:
        st.metric("Total Columns", info.get('columns', 'N/A'))
    with col3:
        st.metric("File", info.get('filepath', 'N/A').split('/')[-1])


def display_schema(schema: Dict[str, str]) -> None:
    """
    Display schema table in Streamlit.
    
    Args:
        schema: Schema dictionary
    """
    st.subheader("🔍 Schema")
    
    schema_df = pd.DataFrame([
        {'Column': col, 'Data Type': dtype}
        for col, dtype in schema.items()
    ])
    
    st.dataframe(schema_df, use_container_width=True)


def display_qa_results(qa_results: Dict[str, Any]) -> None:
    """
    Display QA results in Streamlit.
    
    Args:
        qa_results: QA results dictionary
    """
    st.subheader("✅ Data Quality Assessment")
    
    # Missing values
    missing = qa_results.get('missing_values', {})
    null_frac = qa_results.get('null_fraction', {})
    
    if missing:
        st.warning(f"Missing values detected in {len(missing)} column(s)")
        
        missing_data = []
        for col, count in missing.items():
            frac = null_frac.get(col, 0)
            missing_data.append({
                'Column': col,
                'Missing Count': count,
                'Percentage': f"{frac*100:.2f}%"
            })
        
        missing_df = pd.DataFrame(missing_data)
        st.dataframe(missing_df, use_container_width=True)
    else:
        st.success("✅ No missing values detected")
    
    # Duplicates
    duplicates = qa_results.get('duplicate_rows', 0)
    if duplicates > 0:
        st.warning(f"⚠️ {duplicates} duplicate row(s) found")
    else:
        st.success("✅ No duplicate rows")


def display_anomaly_results(anomaly_results: Dict[str, Any], df: pd.DataFrame = None) -> None:
    """
    Display anomaly detection results in Streamlit.
    
    Args:
        anomaly_results: Anomaly results dictionary
        df: Optional DataFrame for plotting
    """
    st.subheader("🔎 Anomaly Detection")
    
    outliers = anomaly_results.get('outliers', {})
    
    if outliers:
        st.warning(f"Outliers detected in {len(outliers)} column(s)")
        
        outlier_data = []
        for col, count in outliers.items():
            outlier_data.append({
                'Column': col,
                'Outlier Count': count
            })
        
        outlier_df = pd.DataFrame(outlier_data)
        st.dataframe(outlier_df, use_container_width=True)
        
        # Plot distribution for columns with outliers (if DataFrame provided)
        if df is not None and len(outliers) > 0:
            st.write("**Distribution Plots:**")
            
            for col in list(outliers.keys())[:3]:  # Limit to first 3 columns
                if col in df.columns:
                    fig, ax = plt.subplots(figsize=(8, 3))
                    df[col].hist(bins=20, ax=ax, edgecolor='black')
                    ax.set_title(f"Distribution of {col}")
                    ax.set_xlabel(col)
                    ax.set_ylabel("Frequency")
                    st.pyplot(fig)
                    plt.close()
    else:
        st.success("✅ No outliers detected")
    
    # Summary statistics
    stats = anomaly_results.get('summary_stats', {})
    if stats:
        st.write("**Summary Statistics:**")
        stats_data = []
        for col, stat in stats.items():
            stats_data.append({
                'Column': col,
                'Mean': f"{stat.get('mean', 0):.2f}",
                'Std': f"{stat.get('std', 0):.2f}",
                'Min': f"{stat.get('min', 0):.2f}",
                'Max': f"{stat.get('max', 0):.2f}"
            })
        
        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df, use_container_width=True)


def display_insights(insights_data, recommendations: list) -> None:
    """
    Display insights and recommendations in Streamlit with source badge and timing.
    
    Args:
        insights_data: Dict with 'text', 'source', 'generation_time' keys (or just string for backward compatibility)
        recommendations: List of recommendations
    """
    st.subheader("💡 Insights & Analysis")
    
    # Handle backward compatibility - check if dict or string
    if isinstance(insights_data, dict):
        insights_text = insights_data.get('text', str(insights_data))
        source = insights_data.get('source', 'rule-based')
        gen_time = insights_data.get('generation_time', 0)
    else:
        insights_text = str(insights_data)
        source = 'rule-based'
        gen_time = 0
    
    # Display badge and timing info
    col1, col2 = st.columns([3, 1])
    with col1:
        if source == 'gemini':
            st.markdown(
                '<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); '
                'color: white; padding: 12px 24px; border-radius: 10px; font-weight: bold; '
                'display: inline-block; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(118,75,162,0.4);">'
                '🤖 Generated by: Gemini AI</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); '
                'color: white; padding: 12px 24px; border-radius: 10px; font-weight: bold; '
                'display: inline-block; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(42,82,152,0.4);">'
                '📋 Generated by: Rule-Based Analysis</div>',
                unsafe_allow_html=True
            )
    with col2:
        st.metric("⏱️ Time", f"{gen_time:.2f}s")
    
    # Clean text from special characters
    clean_text = insights_text
    # Remove emoji and special characters
    clean_text = clean_text.replace('⚠️', 'WARNING:')
    clean_text = clean_text.replace('✅', 'SUCCESS:')
    clean_text = clean_text.replace('💡', 'NOTE:')
    clean_text = clean_text.replace('📊', '')
    clean_text = clean_text.replace('🎯', '')
    clean_text = clean_text.replace('✨', '')
    
    # Convert markdown bold to HTML
    import re
    clean_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', clean_text)
    
    # Format text with proper sections
    lines = clean_text.split('\n')
    formatted_html = []
    
    for line in lines:
        line = line.strip()
        if not line:
            formatted_html.append('<br>')
        elif 'WARNING:' in line:
            formatted_html.append(f'<div style="color: #fbbf24; margin: 10px 0; padding: 10px; background: rgba(245,158,11,0.1); border-radius: 6px; border-left: 3px solid #fbbf24;">⚠ {line}</div>')
        elif 'SUCCESS:' in line:
            formatted_html.append(f'<div style="color: #4ade80; margin: 10px 0; padding: 10px; background: rgba(34,197,94,0.1); border-radius: 6px; border-left: 3px solid #4ade80;">✓ {line}</div>')
        elif 'NOTE:' in line:
            formatted_html.append(f'<div style="color: #60a5fa; margin: 10px 0; padding: 10px; background: rgba(59,130,246,0.1); border-radius: 6px; border-left: 3px solid #60a5fa;">ℹ {line}</div>')
        elif line.startswith('-') or line.startswith('•'):
            formatted_html.append(f'<div style="margin-left: 20px; color: #cbd5e1; margin: 5px 0;">{line}</div>')
        elif line.startswith('  -') or line.startswith('  •'):
            formatted_html.append(f'<div style="margin-left: 40px; color: #94a3b8; margin: 3px 0; font-size: 0.95em;">{line}</div>')
        else:
            formatted_html.append(f'<div style="color: #e2e8f0; margin: 8px 0;">{line}</div>')
    
    formatted_content = ''.join(formatted_html)
    
    # Display insights in colored box with dark theme
    if source == 'gemini':
        # Dark purple/indigo theme for Gemini
        st.markdown(
            f'<div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); '
            f'padding: 30px; border-radius: 15px; '
            f'border-left: 6px solid #a855f7; '
            f'box-shadow: 0 8px 32px rgba(168,85,247,0.3); margin: 20px 0; '
            f'font-size: 15px; line-height: 1.8;">'
            f'{formatted_content}'
            f'<hr style="border: none; border-top: 1px solid #374151; margin: 20px 0;">'
            f'<em style="color: #a78bfa; font-size: 0.9em;">Powered by Google Gemini AI</em>'
            f'</div>',
            unsafe_allow_html=True
        )
    else:
        # Dark blue/slate theme for rule-based
        st.markdown(
            f'<div style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); '
            f'padding: 30px; border-radius: 15px; '
            f'border-left: 6px solid #3b82f6; '
            f'box-shadow: 0 8px 32px rgba(59,130,246,0.3); margin: 20px 0; '
            f'font-size: 15px; line-height: 1.8;">'
            f'{formatted_content}'
            f'<hr style="border: none; border-top: 1px solid #334155; margin: 20px 0;">'
            f'<em style="color: #60a5fa; font-size: 0.9em;">Rule-Based Analysis</em>'
            f'</div>',
            unsafe_allow_html=True
        )
    
    # Display recommendations
    if recommendations:
        st.write("**🎯 Actionable Recommendations:**")
        for i, rec in enumerate(recommendations, 1):
            st.write(f"{i}. {rec}")


def display_chat_interface(insight_agent, context: dict) -> None:
    """
    Display a chat interface for users to ask questions about their data.
    
    Args:
        insight_agent: InsightAgent instance
        context: Dictionary with dataset context (schema, qa_results, etc.)
    """
    st.subheader("💬 Ask Gemini About Your Data")
    
    # Initialize chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Check if Gemini is available
    if not insight_agent.gemini_enabled:
        st.warning("⚠️ Gemini chat is not available. Please enable LLM and ensure GEMINI_API_KEY is set.")
        return
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(
                f'<div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); '
                f'color: #e2e8f0; padding: 15px 20px; border-radius: 12px; '
                f'margin: 10px 0; border-left: 4px solid #3b82f6; '
                f'box-shadow: 0 4px 12px rgba(59,130,246,0.2);">'
                f'<strong style="color: #60a5fa;">You:</strong> {message["content"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); '
                f'color: #e4e4e7; padding: 15px 20px; border-radius: 12px; '
                f'margin: 10px 0; border-left: 4px solid #a855f7; '
                f'box-shadow: 0 4px 12px rgba(168,85,247,0.2);">'
                f'<strong style="color: #a78bfa;">🤖 Gemini:</strong> {message["content"]}</div>',
                unsafe_allow_html=True
            )
    
    # Chat input
    user_question = st.text_input(
        "Ask a question about your data:",
        placeholder="e.g., What are the main issues in this dataset? How should I handle missing values?",
        key="chat_input"
    )
    
    col1, col2 = st.columns([1, 5])
    with col1:
        send_button = st.button("🚀 Send", use_container_width=True)
    with col2:
        clear_button = st.button("🗑️ Clear Chat", use_container_width=True)
    
    if send_button and user_question:
        # Add user message to history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_question
        })
        
        # Get Gemini response
        with st.spinner("🤖 Gemini is thinking..."):
            response = insight_agent.chat_with_gemini(user_question, context)
        
        # Add Gemini response to history
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': response
        })
        
        # Rerun to display new messages
        st.rerun()
    
    if clear_button:
        st.session_state.chat_history = []
        st.rerun()


def create_download_button(report_content: str, filename: str, label: str) -> None:
    """
    Create a download button for reports.
    
    Args:
        report_content: Content to download
        filename: Suggested filename
        label: Button label
    """
    st.download_button(
        label=label,
        data=report_content,
        file_name=filename,
        mime="text/markdown"
    )
