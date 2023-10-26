import streamlit as st
from firebase_admin import firestore

def display_list():
    st.title("Store QR")

    # Fetch the vCards for the authenticated user from Firestore
    db = firestore.client()
    vcard_ref = db.collection('vcards').document(st.session_state.username).get()
    vcards = vcard_ref.to_dict()

    if vcards:
        for full_name, data in vcards.items():
            # Display the vCard details
            st.write(f"Name: {full_name}")
            st.write(f"Organization: {data.get('ORG', 'N/A')}")
            st.write(f"Role: {data.get('ROLE', 'N/A')}")
            st.write(f"Phone (Cell): {data.get('TEL;TYPE=CELL', 'N/A')}")
            st.write(f"Phone (Work): {data.get('TEL;TYPE=WORK', 'N/A')}")
            st.write(f"Email: {data.get('EMAIL;TYPE=WORK', 'N/A')}")
            st.write(f"Website: {data.get('URL', 'N/A')}")
            st.write(f"LinkedIn: {data.get('X-SOCIALPROFILE', 'N/A')}")
            
            # Display the QR code image (ensure that "QR_URL" always exists in the data)
            qr_url = data.get("QR_URL")
            if qr_url:
                st.image(qr_url, caption="QR Code", use_column_width=True)
            
            st.write("---")  # Separator
    else:
        st.write("No vCards found for this user.")

