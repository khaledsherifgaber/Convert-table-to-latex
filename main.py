import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Table to LaTeX Converter", layout="wide")

st.title("📊 Table to LaTeX Converter")
st.markdown("Convert your CSV or Excel files to LaTeX table format")

# File upload
uploaded_file = st.file_uploader(
    "Upload a CSV or Excel file",
    type=["csv", "xlsx", "xls"],
    help="Select a CSV or Excel file to convert"
)

if uploaded_file is not None:
    try:
        df = None
        
        # Read the file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            # Get all sheet names for Excel files
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names
            
            st.subheader("📑 Select Sheet")
            
            # If multiple sheets, ask user to select one
            if len(sheet_names) > 1:
                selected_sheet = st.selectbox(
                    "This Excel file has multiple sheets. Which one would you like to convert?",
                    sheet_names
                )
            else:
                selected_sheet = sheet_names[0]
                st.info(f"Reading sheet: {selected_sheet}")
            
            df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
        
        # Display preview
        st.subheader("📋 Preview")
        st.dataframe(df, use_container_width=True)
        
        # Generate LaTeX
        st.subheader("LaTeX Code")
        
        # Get number of columns
        num_cols = len(df.columns)
        col_spec = "|" + "|".join(["c"] * num_cols) + "|"
        
        # Build LaTeX table
        latex_code = "\\begin{table}[h]\n"
        latex_code += "\\centering\n"
        latex_code += f"\\begin{{tabular}}{{{col_spec}}}\n"
        latex_code += "\\hline\n"
        
        # Add header
        header = " & ".join(str(col) for col in df.columns) + " \\\\\n"
        latex_code += header
        latex_code += "\\hline\n"
        
        # Add rows
        for _, row in df.iterrows():
            row_str = " & ".join(str(val) for val in row) + " \\\\\n"
            latex_code += row_str
        
        latex_code += "\\hline\n"
        latex_code += "\\end{tabular}\n"
        latex_code += "\\caption{Your table caption}\n"
        latex_code += "\\label{tab:table1}\n"
        latex_code += "\\end{table}"
        
        # Display LaTeX code
        st.code(latex_code, language="latex")
        
        # Copy and download buttons
        col1, col2 = st.columns(2)
        
        with col2:
            st.write("### Download")
            st.download_button(
                label="📥 Download as .tex file",
                data=latex_code,
                file_name="table.tex",
                mime="text/plain"
            )
        
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
else:
    st.info("👆 Upload a CSV or Excel file to get started")

