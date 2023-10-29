import streamlit as st
import qrcode
import io
import base64
from PIL import Image
from firebase_admin import storage, firestore

def generate_qr(vcard_data):
    qr = qrcode.QRCode(
        version=None,  # Let the library decide the version
        box_size=10,
        border=5
    )
    qr.add_data(vcard_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def upload_to_firebase(img_bytes, filename):
    try:
        bucket = storage.bucket('pullmai-e0bb0.appspot.com')
        blob = bucket.blob(filename)
        blob.upload_from_string(img_bytes, content_type="image/png")
        blob.make_public()
        return blob.public_url
    except Exception as e:
        st.error(f"Error uploading to Firebase: {e}")
        return None

def square_crop(img_pil):
    """Crop the PIL image to a centered square."""
    width, height = img_pil.size
    new_dim = min(width, height)
    
    left = (width - new_dim)/2
    top = (height - new_dim)/2
    right = (width + new_dim)/2
    bottom = (height + new_dim)/2
    
    return img_pil.crop((left, top, right, bottom))


def circular_crop(img_pil):
    # Step 1: Resize while maintaining aspect ratio
    aspect = img_pil.width / img_pil.height
    if aspect > 1:
        # Width is greater than height
        new_width = int(aspect * 40)
        img_pil = img_pil.resize((new_width, 40))
    else:
        # Height is greater or equal to width
        new_height = int(40 / aspect)
        img_pil = img_pil.resize((40, new_height))

    # Step 2: Crop the center of the image to make it square
    left = (img_pil.width - 40) / 2
    top = (img_pil.height - 40) / 2
    right = (img_pil.width + 40) / 2
    bottom = (img_pil.height + 40) / 2

    img_pil = img_pil.crop((left, top, right, bottom))
    
    return img_pil

def display_qr():
    st.title('vCard QR Code Generator')

    # Upload profile photo
    uploaded_image = st.file_uploader("Choose a profile image...", type=["jpg", "png", "jpeg"])

    image_encoded = None  # Initialize image_encoded here

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

    # Construct vCard dictionary
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

    if uploaded_image:
        format = uploaded_image.type.split('/')[-1].upper()

        # Open the uploaded image with PIL
        img_pil = Image.open(uploaded_image)

        # Ensure the image is square by cropping
        width, height = img_pil.size
        if width > height:
            left = (width - height) / 2
            right = (width + height) / 2
            top = 0
            bottom = height
        else:
            top = (height - width) / 2
            bottom = (height + width) / 2
            left = 0
            right = width
        img_pil = img_pil.crop((left, top, right, bottom))

        # Resize image to 40x40
        img_pil = img_pil.resize((40, 40))

        # Save the resized square image to a BytesIO buffer in the determined format
        buffered = io.BytesIO()
        img_pil.save(buffered, format=format)

        # Convert the BytesIO buffer to Base64
        image_encoded = base64.b64encode(buffered.getvalue()).decode()

        # Adjust vCard key for image data
        if format == "JPEG":
            vCard["PHOTO;TYPE=JPEG;ENCODING=B"] = image_encoded
        elif format == "PNG":
            vCard["PHOTO;TYPE=PNG;ENCODING=B"] = image_encoded
        # Extend with other formats if needed

        # Display the 40x40 circular image in Streamlit
        st.markdown(
            f'<img src="data:image/{format.lower()};base64,{image_encoded}" style="border-radius: 50%; width: 40px; height: 40px;">',
            unsafe_allow_html=True
        )

    vcard_data = "\n".join(f"{key}:{value}" for key, value in vCard.items())

    if st.button('Generate QR Code'):
        img_pil = generate_qr(vcard_data)
        buffered = io.BytesIO()
        img_pil.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()

        filename = f"{full_name}.png"
        file_url = upload_to_firebase(img_bytes, filename)

        vCard["QR_URL"] = file_url
        vcard_ref.set(vCard,
