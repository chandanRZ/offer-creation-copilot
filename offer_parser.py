# import pandas as pd
# from io import BytesIO

# def parse_offer_excel(uploaded_file):
#     try:
#         df = pd.read_excel(uploaded_file)
#         return df
#     except Exception as e:
#         print(f"Error reading file: {e}")
#         return None

# def generate_excel_from_rows(rows):
#     df = pd.DataFrame(rows)
#     output = BytesIO()
#     with pd.ExcelWriter(output, engine='openpyxl') as writer:
#         df.to_excel(writer, index=False, sheet_name="Offer Construct")
#     output.seek(0)
#     return output

    
# import streamlit as st
# import pandas as pd
# from offer_parser import parse_offer_file
# from gpt_utils import generate_offer_construct

# st.set_page_config(page_title="Offer Copilot Demo", layout="wide")
# st.title("💼 Offer Copilot Demo")
# st.markdown("Upload your raw offer input file to auto-generate an Offer Construct")

# uploaded_file = st.file_uploader("Upload offer input Excel file", type=[".xlsx"])

# if uploaded_file:
#     st.success(f"File '{uploaded_file.name}' uploaded successfully!")

#     brand_name = st.text_input("Enter brand name for this offer")

#     st.write("Uploaded file name:", uploaded_file.name)
#     st.write("Brand name entered:", brand_name)

#     if brand_name:
#         with st.spinner("Parsing input file..."):
#             parsed_data = parse_offer_file(uploaded_file, brand_name)

#         if parsed_data is not None and not parsed_data.empty:
#             st.subheader("Parsed Data")
#             st.dataframe(parsed_data)
#         else:
#             st.warning("Parsed data is empty or invalid. Showing sample fallback construct.")

#         with st.spinner("Generating AI-enhanced Offer Construct using GPT..."):
#             offer_construct_df = generate_offer_construct(parsed_data, brand_name)

#         st.subheader("🤖 AI-Enhanced Offer Construct")
#         if offer_construct_df is not None and not offer_construct_df.empty:
#             st.dataframe(offer_construct_df)

#             # Allow download
#             csv_data = offer_construct_df.to_csv(index=False).encode('utf-8')
#             st.download_button(
#                 label="Download Offer Construct as CSV",
#                 data=csv_data,
#                 file_name=f"{brand_name}_offer_construct.csv",
#                 mime="text/csv"
#             )
#         else:
#             st.warning("Offer construct generation failed. Showing a sample construct as fallback.")
#             sample_construct = pd.DataFrame({
#                 "Brand": ["Vivo"],
#                 "Model": ["Vivo X100"],
#                 "Tenure": [6],
#                 "Consumer EMI": [3333],
#                 "Cashback": [1000],
#                 "Subvention": [1500],
#                 "Bank": ["HDFC"],
#                 "Effective Price": [18000]
#             })
#             st.dataframe(sample_construct)
#             st.info("This is a fallback sample. Check your file input for issues.")
#     else:
#         st.info("Please enter brand name to proceed.")

import pandas as pd
import re
import difflib

REQUIRED_HEADERS = ["Tenure", "Subvention", "Offer Code"]
HEADER_ALIASES = {
    "tenure": "Tenure",
    "emi tenure": "Tenure",
    "brand emi tenures": "Tenure",
    "sub": "Subvention",
    "subvention": "Subvention",
    "offer code": "Offer Code",
    "code": "Offer Code"
}

def normalize_header(header):
    header = header.strip().lower()
    return HEADER_ALIASES.get(header, header.title())

def parse_offer_excel(file):
    try:
        df = pd.read_excel(file, sheet_name=0, header=None)

        # Detect if file is in key-value format (2-column layout)
        if df.shape[1] == 2 and df.shape[0] > 1:
            # Convert to dict for fuzzy mapping
            raw_dict = dict(zip(df.iloc[:, 0].astype(str), df.iloc[:, 1].astype(str)))
            parsed_data = {}
            missing_headers = []

            for req in REQUIRED_HEADERS:
                found = False
                for key in raw_dict:
                    norm_key = normalize_header(key)
                    if norm_key == req:
                        parsed_data[req] = raw_dict[key]
                        found = True
                        break
                if not found:
                    missing_headers.append(req)

            if missing_headers:
                raise ValueError(f"Missing headers: {', '.join(missing_headers)}")

            return parsed_data, []

        # Else try as standard table with headers
        df = pd.read_excel(file)
        original_headers = df.columns.tolist()

        header_map = {}
        for col in original_headers:
            norm_col = normalize_header(str(col))
            for key, canonical in HEADER_ALIASES.items():
                if key in str(col).strip().lower():
                    header_map[col] = canonical

        canonical_headers = list(set(header_map.values()))
        missing_headers = [h for h in REQUIRED_HEADERS if h not in canonical_headers]

        if missing_headers:
            raise ValueError(f"Missing headers: {', '.join(missing_headers)}")

        df.rename(columns=header_map, inplace=True)
        return df, []

    except Exception as e:
        return None, [f"❌ Error reading file: {str(e)}"]
