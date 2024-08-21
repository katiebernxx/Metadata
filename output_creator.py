import fitz
import pandas as pd
from speaker_count import top_three
from emotions import rank_emotions

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = []
    for page in doc:
        text.append(page.get_text())
    return "\n".join(text)

def process_script(pdf_path):
    # Extract text from the PDF
    script_text = extract_text_from_pdf(pdf_path)
    
    # Extract speaker count
    speakers = top_three(script_text)
    
    # Extract top-ranked emotions
    emotions = rank_emotions(script_text)

    return speakers, emotions

def update_csv_with_script_data(csv_path, pdf_paths):
    # Initialize an empty DataFrame or load existing CSV if it exists
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        df = pd.DataFrame()

    # Process each script and add data to the DataFrame
    for pdf_path in pdf_paths:
        script_data = process_script(pdf_path)
        
        # Use the script file name as the index (or any other unique identifier)
        script_name = pdf_path.split("/")[-1]

        # Convert the script data to a DataFrame row
        script_df = pd.DataFrame([script_data], index=[script_name])
        
        # Append to the existing DataFrame
        df = pd.concat([df, script_df], axis=0)

    # Save the updated DataFrame to the CSV
    df.to_csv(csv_path)


