import streamlit as st
import qrcode
import io
import base64
from PIL import Image
from firebase_admin import storage, firestore
import os
from datetime import timedelta  # Import timedelta

def b64_image(filename):
    with open(filename, 'rb') as f:
        b64 = base64.b64encode(f.read())
        return b64.decode('utf-8')

def generate_qr(vcard_data):
    try:
        qr = qrcode.QRCode(
            version=None,  # Let the library decide the version
            box_size=10,
            border=5
        )
        qr.add_data(vcard_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        return img
    except ValueError:
        st.error("Failed to generate QR code. Please try reducing the amount of data.")
        return None

def upload_to_firebase(img_bytes, filename):
    try:
        # Adding the photos directory
        bucket = storage.bucket('pullmai-e0bb0.appspot.com')
        blob = bucket.blob(f"photos/{filename}")
        blob.upload_from_string(img_bytes, content_type="image/png")
        blob.make_public()

        # Return the constructed Firebase Storage URL
        token = blob.generate_signed_url(timedelta(seconds=3600), method='GET').split('token=')[-1]
        return f"https://firebasestorage.googleapis.com/v0/b/pullmai-e0bb0.appspot.com/o/{filename}?alt=media&token={token}"
    except Exception as e:
        st.error(f"Error uploading to Firebase: {e}")
        return None


def display_qr():
    st.title('vCard QR Code Generator')

    # Retrieve saved vCard data from Firestore
    db = firestore.client()
    vcard_ref = db.collection('vcards').document(st.session_state.username)
    saved_vCard = vcard_ref.get().to_dict() or {}

    # Populate input fields with saved data or default values
    full_name = st.text_input("Nombre Completo", saved_vCard.get("FN", "Juan Soto"))
    # ... [rest of the input fields]

    # Handle image upload
    vCard = {
        "BEGIN": "VCARD",
        # ... [rest of the vCard dictionary]
        "END": "VCARD",
    }

    uploaded_image = st.file_uploader("Upload your image", type=['png', 'jpg', 'jpeg'])

    if uploaded_image:
        # ... [rest of the uploaded_image block]

        vcard_data = "\n".join(f"{key}:{value}" for key, value in vCard.items())

    img_bytes = None  # Initialize img_bytes to ensure it's always defined

    if st.button('Generate QR Code'):
        img_pil = generate_qr(vcard_data)
        if img_pil is None:
            return

        buffered = io.BytesIO()
        img_pil.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()

        # ... [rest of the QR code generation block]

    if img_bytes:
        st.download_button(
            label="Download QR Code",
            data=img_bytes,
            file_name=filename,
            mime="image/png"
        )
        st.write(f"Uploaded to Firebase Storage: [Link]({qr_file_url})")

# Call the function
display_qr()

