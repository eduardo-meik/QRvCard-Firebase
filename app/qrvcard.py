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
    last_name, first_name = full_name.split(' ', 1) if ' ' in full_name else (full_name, '')
    organization = st.text_input("Organización", saved_vCard.get("ORG", "Ejemplo Ltda."))
    title = st.text_input("Puesto", saved_vCard.get("TITLE", "CEO"))
    role = st.text_input("Rol", saved_vCard.get("ROLE", "Manager"))
    phone_cell = st.text_input("Teléfono (Celular)", saved_vCard.get("TEL;TYPE=CELL", "(555) 555-5555"))
    phone_work = st.text_input("Teléfono (Trabajo)", saved_vCard.get("TEL;TYPE=WORK", "(555) 555-5555"))
    email = st.text_input("Email (Trabajo)", saved_vCard.get("EMAIL;TYPE=WORK", "john.smith@example.com"))
    url = st.text_input("Website", saved_vCard.get("URL", "https://www.example.com"))
    linkedin = st.text_input("LinkedIn", saved_vCard.get("X-SOCIALPROFILE", "https://www.linkedin.com/in/juansoto/"))

# Handle image upload
    vCard = {
        "BEGIN": "VCARD",
        "VERSION": "3.0",
        "KIND": "INDIVIDUAL",
        "FN": full_name,
        "N": f"{last_name};{first_name};;;",
        "EMAIL;TYPE=WORK": email,
        "TITLE": title,
        "ROLE": role,
        "TEL;TYPE=CELL": phone_cell,
        "TEL;TYPE=WORK": phone_work,
        "URL": url,
        "ORG": organization,
        "X-SOCIALPROFILE": linkedin,
        "END": "VCARD",
    }

    uploaded_image = st.file_uploader("Upload your image", type=['png', 'jpg', 'jpeg'])

    if uploaded_image:
        # Save uploaded image to a temporary file
        tmp_filename = "tmp_uploaded_image." + uploaded_image.type.split("/")[-1]
        with open(tmp_filename, "wb") as f:
            f.write(uploaded_image.getvalue())

        # Upload user's photo to Firebase and retrieve its URL
        user_photo_url = upload_to_firebase(uploaded_image.getvalue(), tmp_filename)

        if user_photo_url:
            # Add to vCard
            photo_enc_type = "image/jpeg" if uploaded_image.type == "image/jpeg" else "image/png"
            vCard[f"PHOTO;ENCODING=b;TYPE={photo_enc_type}"] = b64_image(tmp_filename)

        # Optional: Remove the temporary file after processing
        os.remove(tmp_filename)

        vcard_data = "\n".join(f"{key}:{value}" for key, value in vCard.items())

    if st.button('Generate QR Code'):
        img_pil = generate_qr(vcard_data)
        if img_pil is None:
            return

        buffered = io.BytesIO()
        img_pil.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()

        # Upload the QR code image to Firebase
        filename = f"{full_name}_QR.png"
        qr_file_url = upload_to_firebase(img_bytes, filename)
        if qr_file_url:
            vCard["QR_URL"] = qr_file_url

        st.image(img_bytes, caption='Generated QR Code', use_column_width=True)
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

