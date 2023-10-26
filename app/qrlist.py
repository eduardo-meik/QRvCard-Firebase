import streamlit as st
from firebase_admin import firestore

def display_list():
   
    # Fetch the vCards for the authenticated user from Firestore
    db = firestore.client()
    vcard = db.collection('vcards').document(st.session_state.username).get().to_dict()

    if vcard:
        # Display the vCard details
        st.write(f"Name: {vcard.get('FN', 'N/A')}")
        st.write(f"Organization: {vcard.get('ORG', 'N/A')}")
        st.write(f"Role: {vcard.get('ROLE', 'N/A')}")
        st.write(f"Phone (Cell): {vcard.get('TEL;TYPE=CELL', 'N/A')}")
        st.write(f"Phone (Work): {vcard.get('TEL;TYPE=WORK', 'N/A')}")
        st.write(f"Email: {vcard.get('EMAIL;TYPE=WORK', 'N/A')}")
        st.write(f"Website: {vcard.get('URL', 'N/A')}")
        st.write(f"LinkedIn: {vcard.get('X-SOCIALPROFILE', 'N/A')}")
        
        # Display the QR code image (ensure that "QR_URL" always exists in the vcard)
        qr_url = vcard.get("QR_URL")
        if qr_url:
            st.image(qr_url, caption="QR Code", use_column_width=True)
            
        st.write("---")  # Separator
    else:
        st.write("No vCards found for this user.")



