# app/analyzer.py
import pandas as pd
import re
from .patterns import patterns
from .llm_helper import LLMHelper

def analyze_dataset(df: pd.DataFrame):
    """
    Analyze the dataset for structure, sensitive information, and AI-generated recommendations.
    """
    summary = {
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "missing_values": int(df.isnull().sum().sum()),
        "columns": list(df.columns)
    }

    # Find sensitive data matches
    sensitive_data = {}
    for name, pattern in patterns.items():
        matches = set()
        for col in df.columns:
            try:
                for value in df[col].dropna().astype(str):
                    if re.search(pattern, value):
                        matches.add(value)
            except Exception:
                continue
        if matches:
            sensitive_data[name] = list(matches)

    # Build report summary text
    analysis_prompt = f"""
    You are SecureDataGPT, a data security analyst AI. Analyze the provided dataset summary and recommend specific, practical privacy improvements.  
    Summary:  
    - Rows: {summary['num_rows']}  
    - Columns: {summary['num_columns']}  
    - Missing values: {summary['missing_values']}  
    - Sensitive data detected: {', '.join(sensitive_data.keys()) if sensitive_data else 'None'}  

    Provide concise, actionable recommendations in bullet points, prioritizing data protection, compliance, and risk mitigation.
    """

    # Generate AI-based recommendations
    llm = LLMHelper()
    ai_recommendations = llm.generate_text(analysis_prompt)

    report = {
        "summary": summary,
        "sensitive_data": sensitive_data,
        "ai_recommendations": ai_recommendations
    }

    return report
