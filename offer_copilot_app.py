# # import streamlit as st
# # import pandas as pd
# # from offer_parser import parse_offer_excel, generate_excel_from_rows
# # from gpt_utils import generate_subvention_split, generate_offer_details, generate_marketing_copy, detect_anomalies, generate_full_offer_from_text

# # st.set_page_config(page_title="Offer Creation Copilot", layout="wide")
# # st.title("💡 Offer Creation Copilot - Razorpay Hackathon")

# # uploaded_file = st.file_uploader("📤 Upload Offer Input File", type=["xlsx"])
# # if uploaded_file:
# #     brand = st.text_input("Enter Brand Name", "Vivo")
# #     df = parse_offer_excel(uploaded_file)
# #     if df is not None:
# #         st.subheader("📊 Parsed Data")
# #         st.dataframe(df)

# #         # Process each row and add AI-generated columns
# #         rows = []
# #         st.subheader("🤖 AI-Enhanced Offer Construct")
# #         for _, row in df.iterrows():
# #             row_dict = row.to_dict()
# #             row_dict["Subvention Split"] = generate_subvention_split(row_dict, brand)
# #             row_dict["Offer Name"] = generate_offer_details(row_dict, brand, "name")
# #             row_dict["Offer Description"] = generate_offer_details(row_dict, brand, "desc")
# #             row_dict["CTA"] = generate_offer_details(row_dict, brand, "cta")
# #             row_dict["Push Title"] = generate_marketing_copy(row_dict, brand, "title")
# #             row_dict["Push Description"] = generate_marketing_copy(row_dict, brand, "desc")
# #             row_dict["TnC"] = generate_marketing_copy(row_dict, brand, "tnc")
# #             row_dict["Anomaly"] = detect_anomalies(row_dict)
# #             rows.append(row_dict)

# #         result_df = pd.DataFrame(rows)
# #         st.dataframe(result_df)

# #         if st.download_button("📥 Download Offer Construct Excel", data=generate_excel_from_rows(rows), file_name="Offer_Construct.xlsx"):
# #             st.success("Downloaded successfully!")

# # st.markdown("---")
# # st.subheader("💬 Chat-based Offer Generation")
# # text_prompt = st.text_area("Describe your offer in plain English")
# # if st.button("Generate Offer"):
# #     if text_prompt:
# #         output = generate_full_offer_from_text(text_prompt)
# #         st.code(output, language="markdown")


# import streamlit as st
# import pandas as pd
# import io
# from offer_parser import parse_offer_excel

# # Title
# st.title("📦 Offer Copilot")

# # Upload
# uploaded_file = st.file_uploader("Upload Offer File (Excel)", type=["xlsx"])

# parsed_data = None
# brand_name = None
# offer_excel_bytes = None

# if uploaded_file:
#     try:
#         parsed_data = parse_offer_excel(uploaded_file)
#         st.success("✅ File parsed successfully!")
#         st.write("### Parsed Data")
#         st.dataframe(parsed_data)
#     except Exception as e:
#         st.error(f"❌ Error reading file: {e}")

#     # Brand input
#     brand_name = st.text_input("Enter Brand Name")

#     # Dummy Offer Construct Generator
#     def generate_mock_offer_construct(brand):
#         data = [
#             {"Brand": brand, "Model": "Redmi Note 13", "Bank": "ICICI", "Tenure": "6", "Interest": "No Cost", "Subvention": "500"},
#             {"Brand": brand, "Model": "Redmi Note 13 Pro", "Bank": "HDFC", "Tenure": "9", "Interest": "Low Cost", "Subvention": "800"},
#             {"Brand": brand, "Model": "Redmi 12", "Bank": "ICICI", "Tenure": "3", "Interest": "No Cost", "Subvention": "300"},
#         ]
#         df = pd.DataFrame(data)
#         output = io.BytesIO()
#         with pd.ExcelWriter(output, engine='openpyxl') as writer:
#             df.to_excel(writer, index=False, sheet_name="Offer Construct")
#         return output.getvalue()

#     if brand_name:
#         st.markdown("---")
#         st.subheader("🤖 AI-Enhanced Offer Construct (Mock)")

#         offer_excel_bytes = generate_mock_offer_construct(brand_name)

#         st.success("✅ Offer Construct ready!")
#         st.download_button(
#             label="📥 Download Offer Construct Excel",
#             data=offer_excel_bytes,
#             file_name=f"{brand_name}_Offer_Construct.xlsx",
#             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )


# import streamlit as st
# import pandas as pd
# import os
# from io import BytesIO
# from offer_parser import parse_offer_excel, generate_excel_from_rows

# # Set page config
# st.set_page_config(page_title="Offer Copilot", layout="wide")

# st.title("🦈 RazorShark Offer Copilot")

# uploaded_file = st.file_uploader("Upload Offer Input Excel", type=["xlsx"])

# if uploaded_file:
#     try:
#         parsed_df = parse_offer_excel(uploaded_file)
#         st.success("✅ File parsed successfully!")

#         # Display Parsed Data
#         st.subheader("📄 Parsed Data")
#         st.dataframe(parsed_df, use_container_width=True)
#         # Auto-detect brand from Offer Code
#         brand_detected = ""
#         if 'Offer Code' in parsed_df.columns:
#             offer_code_raw = parsed_df['Offer Code'].dropna().astype(str).iloc[0]
#             st.write(f"🔍 Detected Offer Code: `{offer_code_raw}`")
#             if "_" in offer_code_raw:
#                 brand_detected = offer_code_raw.split("_")[0].strip().upper()
#                 st.write(f"✨ Auto-detected brand: `{brand_detected}`")

#         # brand_name = st.text_input("Enter Brand Name", value=brand_detected)


#         st.subheader("🤖 AI-Enhanced Offer Construct")

#         # Placeholder sample construct
#         sample_construct = pd.DataFrame({
#             # "Brand": [brand_name],
#             "Tenure": [6],
#             "Interest Rate": [13],
#             "Subvention": ["Brand 5%, Razorpay 3%"],
#             "Offer Start": ["2023-11-01"],
#             "Offer End": ["2023-11-15"],
#             "Offer Code": [parsed_df['Offer Code'].iloc[0] if 'Offer Code' in parsed_df.columns else "NA"]
#         })

#         # Show sample
#         st.dataframe(sample_construct, use_container_width=True)

#         # Download sample
#         def to_excel(df):
#             output = BytesIO()
#             with pd.ExcelWriter(output, engine='openpyxl') as writer:
#                 df.to_excel(writer, index=False, sheet_name='OfferConstruct')
#             return output.getvalue()

#         excel_data = to_excel(sample_construct)
#         st.download_button("⬇️ Download Offer Construct", data=excel_data, file_name="offer_construct_mock.xlsx")

#     except Exception as e:
#         st.error(f"❌ Error reading file: {str(e)}")
#         st.info("Showing mock offer construct for demo purposes.")

#         mock_df = pd.DataFrame({
#             # "Brand": ["DEMO"],
#             "Tenure": [6],
#             "Interest Rate": [14],
#             "Subvention": ["Brand 6%, Razorpay 2%"],
#             "Offer Start": ["2023-11-01"],
#             "Offer End": ["2023-11-15"],
#             "Offer Code": ["DEMO_BRAND_OFFER"]
#         })

#         st.dataframe(mock_df, use_container_width=True)
#         excel_data = to_excel(mock_df)
#         st.download_button("⬇️ Download Offer Construct", data=excel_data, file_name="mock_offer_construct.xlsx")


import streamlit as st
import pandas as pd
from io import BytesIO
from offer_parser import parse_offer_excel

# Set page config
st.set_page_config(page_title="Offer Copilot", layout="wide")
st.title("🦈 RazorShark Offer Copilot")

uploaded_file = st.file_uploader("Upload Offer Input Excel", type=["xlsx"])
parsed_df = None
offer_code_value = "CHAT_OFFER"  # Default in case file isn't uploaded

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='OfferConstruct')
    return output.getvalue()

# -------- File Upload Section --------
if uploaded_file:
    try:
        parsed_df, header_errors = parse_offer_excel(uploaded_file)

        if header_errors:
            for err in header_errors:
                st.error(f"⚠️ {err}")
        else:
            st.success("✅ All required headers are present!")

        # Display Parsed Data
        st.subheader("📄 Parsed Data")
        st.dataframe(parsed_df, use_container_width=True)

        # Auto-detect brand from Offer Code
        brand_detected = ""
        if 'Offer Code' in parsed_df.columns:
            offer_code_raw = parsed_df['Offer Code'].dropna().astype(str).iloc[0]
            st.write(f"🔍 Detected Offer Code: `{offer_code_raw}`")
            if "_" in offer_code_raw:
                brand_detected = offer_code_raw.split("_")[0].strip().upper()
                st.write(f"✨ Auto-detected brand: `{brand_detected}`")
            offer_code_value = offer_code_raw

        st.subheader("🤖 AI-Enhanced Offer Construct")

        sample_construct = pd.DataFrame({
            "Tenure": [6],
            "Interest Rate": [13],
            "Subvention": ["Brand 5%, Razorpay 3%"],
            "Offer Start": ["2023-11-01"],
            "Offer End": ["2023-11-15"],
            "Offer Code": [offer_code_value]
        })

        st.dataframe(sample_construct, use_container_width=True)

        excel_data = to_excel(sample_construct)
        st.download_button("⬇️ Download Offer Construct", data=excel_data, file_name="offer_construct_mock.xlsx")

    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")

# -------- Chatbox Section (Always Visible) --------
st.markdown("---")
st.subheader("💬 Chat with Offer Copilot")

user_input = st.text_area(
    "Describe your offer in text (optional)",
    placeholder="E.g., Create a cashback offer for Vivo with ₹2000 cashback on 6-month EMI",
    height=100
)

if st.button("🛠 Generate Mock Construct from Chat"):
    if user_input.strip():
        st.success("✅ Generated based on your input!")

        chat_mock_df = pd.DataFrame({
            "Tenure": [6],
            "Interest Rate": [12],
            "Subvention": ["Brand 7%, Razorpay 1%"],
            "Offer Start": ["2023-11-01"],
            "Offer End": ["2023-11-15"],
            "Offer Code": [offer_code_value]
        })

        st.dataframe(chat_mock_df, use_container_width=True)

        excel_data_chat = to_excel(chat_mock_df)
        st.download_button(
            "⬇️ Download Chat-based Construct",
            data=excel_data_chat,
            file_name="chat_offer_construct_mock.xlsx"
        )
    else:
        st.warning("⚠️ Please enter some text to generate a construct.")
