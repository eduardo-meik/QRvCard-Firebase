# QR vCard Streamlit App

This Streamlit application allows users to create and manage virtual business cards (vCards) in the form of QR codes. Users can also view a list of QR codes they've generated. Additionally, it provides user authentication features with Firebase.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Setting Up Firebase](#setting-up-firebase)
- [Running the App](#running-the-app)
- [License](#license)
- [Contributing](#contributing)

## Features

- **User Authentication**: Users can sign up and log into the application using their email.
- **QR vCard Creation**: Generate a QR code for a vCard with user details.
- **QR List**: View a list of generated QR codes.
- **Intuitive UI**: User-friendly interface with clear navigation and error messages.

## Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/eduardo-meik/QRvCard-Firebase.git
    cd QRvCard-Firebase
    ```

2. **Set up a virtual environment** (Optional, but recommended)

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required packages**

    ```bash
    pip install -r requirements.txt
    ```

## Setting Up Firebase

To use this app, you need to set up Firebase authentication:

1. Go to [Firebase Console](https://console.firebase.google.com/).
2. Create a new project or select an existing project.
3. Navigate to **Authentication** > **Sign-in method**.
4. Enable Email/Password sign-in.
5. Navigate to **Project settings** > **Service accounts**.
6. Click on **Generate new private key**. This will download a `.json` key.
7. Save the contents of the downloaded key as a secret in Streamlit (or in a `.env` file if running locally). The key in this project is named `textkey`.

## Running the App

1. **Locally**:

    ```bash
    streamlit run main.py
    ```

2. **On Streamlit Sharing**:

    - Push your repo to GitHub.
    - Create a new app on Streamlit Sharing and link your GitHub repo.
    - Add the Firebase private key content to Streamlit secrets in the format:

    ```json
    {
        "textkey": "YOUR_FIREBASE_JSON_KEY_CONTENT"
    }
    ```

    - Deploy and enjoy!

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Contributing

1. Fork the repository on GitHub.
2. Clone the forked repo to your machine.
3. Make your changes.
4. Push your changes to your fork on GitHub.
5. Create a pull request from your fork to the main repository.

