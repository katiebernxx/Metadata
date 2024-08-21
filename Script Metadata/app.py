import streamlit as st
import fitz
import pandas as pd
from speaker_count import top_three
from emotions import rank_emotions

def extract_text_from_pdf(pdf_file):
    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = []
        for page in doc:
            text.append(page.get_text())
        return "\n".join(text)
    except UnicodeDecodeError as e:
        st.error(f"Error reading PDF: {e}")
        return ""

def process_script(pdf_file):
    # Extract text from the PDF
    script_text = extract_text_from_pdf(pdf_file)
    
    # Extract speaker count
    speakers = top_three(script_text)
    
    # Extract top-ranked emotions
    emotions = rank_emotions(script_text)

    return speakers, emotions

def update_csv_with_script_data(csv_path, uploaded_files):
    # Initialize an empty DataFrame or load existing CSV if it exists
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Script Name", "Top Characters", "Top Emotions"])

    # Process each script and add data to the DataFrame
    for uploaded_file in uploaded_files:
        script_name = uploaded_file.name
        characters, emotions = process_script(uploaded_file)
        script_df = pd.DataFrame({
            'Script Name': [script_name],
            'Top Characters': [", ".join(characters)],
            'Top Emotions': [", ".join(emotions)]
        })
        df = pd.concat([df, script_df], axis=0, ignore_index=True)

    # Save the updated DataFrame to the CSV
    df.to_csv(csv_path, encoding='utf-8', index=False)
    return df.to_csv(index=False).encode('utf-8')

st.title("Script Analyzer")

# User input for CSV path
csv_path = st.text_input("Enter CSV path to save script data:", "scripts_data.csv")

uploaded_files = st.file_uploader("Upload Script PDFs", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    csv = update_csv_with_script_data(csv_path, uploaded_files)
    
    st.download_button(
        label="Download Script Metadata Here",
        data=csv,
        file_name=csv_path,
        mime='text/csv',
    )
