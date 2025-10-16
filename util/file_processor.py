# utils/file_processor.py
import pandas as pd
import tempfile
import csv

def preprocess_and_save(file):
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file, encoding='utf-8', na_values=['NA', 'N/A', 'missing'])
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file, na_values=['NA', 'N/A', 'missing'])
        else:
            raise ValueError("Unsupported format")
        print(df)
        # Clean strings
        for col in df.select_dtypes(include=['object']):
            print(col)
            df[col] = df[col].astype(str).replace({r'"': '""'}, regex=True)
        print(df)
        # Parse dates and numbers
        for col in df.columns:
            if 'date' in col.lower():
                
                df[col] = pd.to_datetime(df[col], errors='coerce')

        # Save to temp
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        df.to_csv(temp_file.name, index=False, quoting=csv.QUOTE_ALL)
        temp_file.close()
        
        return temp_file.name, df.columns.tolist(), df

    except Exception as e:

        return None, None, None