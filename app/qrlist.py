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

        qr_url = vcard_data.get("QR_URL", "")
        
        # Check if the QR_URL is in the expected format
        if "gs://pullmai-e0bb0.appspot.com/" in qr_url:
            # Create a button to fetch and display the QR code image
            if st.button("Show QR Code"):
                # Get the QR image's path from Firestore data (the part after the bucket name)
                path_in_bucket = qr_url.split("gs://pullmai-e0bb0.appspot.com/")[1]
                bucket = storage.bucket()
                blob = bucket.blob(path_in_bucket)

                # Generate a signed URL for the blob, valid for 5 minutes
                qr_image_url = blob.generate_signed_url(timedelta(minutes=5))
                
                # Display the image fullscreen
                st.image(qr_image_url, caption="QR Code", width=st.get_option('deprecation.showPyplotGlobalUse'))
        else:
            st.write("Invalid QR URL format")

        st.write("---")  # Separator
    else:
        st.write("No vCard found for this user.")









