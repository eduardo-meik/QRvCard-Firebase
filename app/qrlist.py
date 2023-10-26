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
            st.write(f"Organization: {data['ORG']}")
            st.write(f"Role: {data['ROLE']}")
            st.write(f"Phone (Cell): {data['TEL;TYPE=CELL']}")
            st.write(f"Phone (Work): {data['TEL;TYPE=WORK']}")
            st.write(f"Email: {data['EMAIL;TYPE=WORK']}")
            st.write(f"Website: {data['URL']}")
            st.write(f"LinkedIn: {data['X-SOCIALPROFILE']}")
            # Display the QR code image
            st.image(data["QR_URL"], caption="QR Code", use_column_width=True)
            st.write("---")  # Separator
    else:
        st.write("No vCards found for this user.")
