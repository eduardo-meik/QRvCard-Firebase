import streamlit as st
from firebase_admin import firestore, storage
from datetime import timedelta

def display_list():
    st.title("QR List")

    # Fetch the vCard for the authenticated user from Firestore
    db = firestore.client()
    vcard_data = db.collection('vcards').document(st.session_state.username).get().to_dict()

    if vcard_data:
        # Display the vCard details
        st.write(f"Name: {vcard_data.get('FN', 'N/A')}")
        st.write(f"Organization: {vcard_data.get('ORG', 'N/A')}")
        st.write(f"Role: {vcard_data.get('ROLE', 'N/A')}")
        st.write(f"Phone (Cell): {vcard_data.get('TEL;TYPE=CELL', 'N/A')}")
        st.write(f"Phone (Work): {vcard_data.get('TEL;TYPE=WORK', 'N/A')}")
        st.write(f"Email: {vcard_data.get('EMAIL;TYPE=WORK', 'N/A')}")
        st.write(f"Website: {vcard_data.get('URL', 'N/A')}")
        st.write(f"LinkedIn: {vcard_data.get('X-SOCIALPROFILE', 'N/A')}")

        qr_image_url = vcard_data.get("QR_URL", "")
        
        # Create a button to display the QR code image in fullscreen
        if st.button("Show QR Code"):
            st.image(qr_image_url, caption="QR Code", use_container_width=True)

        st.write("---")  # Separator
    else:
        st.write("No vCard found for this user.")
