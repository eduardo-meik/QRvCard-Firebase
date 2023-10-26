import streamlit as st
from firebase_admin import firestore

def display_list():
    st.title("Store QR")

    # Fetch the vCards for the authenticated user from Firestore
    db = firestore.client()
    vcard_ref = db.collection('vcards').document(st.session_state.username).get()
    vcards = vcard_ref.to_dict()

    # Print the fetched data to console
    st.write("Fetched Data:", vcards)

    if vcards and isinstance(vcards, dict):
        # Create a list to store table data
        table_data = []

        for full_name, data in vcards.items():
            if isinstance(data, dict):
                row_data = {
                    "Name": full_name,
                    "Organization": data.get('ORG', 'N/A'),
                    "Role": data.get('ROLE', 'N/A'),
                    "Phone (Cell)": data.get('TEL;TYPE=CELL', 'N/A'),
                    "Phone (Work)": data.get('TEL;TYPE=WORK', 'N/A'),
                    "Email": data.get('EMAIL;TYPE=WORK', 'N/A'),
                    "Website": data.get('URL', 'N/A'),
                    "LinkedIn": data.get('X-SOCIALPROFILE', 'N/A')
                }
                table_data.append(row_data)

                # Display the QR code image with an option to expand
                st.image(data.get("QR_URL"), caption=f"QR Code for {full_name}", use_column_width=True)
                if st.checkbox(f"Expand QR for {full_name}"):
                    st.image(data.get("QR_URL"), use_column_width='auto')
                st.write("---")  # Separator

        # Display table
        st.table(table_data)

    else:
        st.write("No vCards found or unexpected data format.")


