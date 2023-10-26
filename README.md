#QRvCard-Firebase App
This Streamlit application allows users to create and manage virtual business cards (vCards) in the form of QR codes. Users can also view a list of QR codes they've generated. Additionally, it provides user authentication features with Firebase.

Table of Contents
Features
Installation
Setting Up Firebase
Running the App
License
Contributing
Features
User Authentication: Users can sign up and log into the application using their email.
QR vCard Creation: Generate a QR code for a vCard with user details.
QR List: View a list of generated QR codes.
Intuitive UI: User-friendly interface with clear navigation and error messages.
Installation
Clone the repository

bash
Copy code
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
Set up a virtual environment (Optional, but recommended)

bash
Copy code
python3 -m venv venv
source venv/bin/activate
Install the required packages

bash
Copy code
pip install -r requirements.txt
Setting Up Firebase
To use this app, you need to set up Firebase authentication:

Go to Firebase Console.
Create a new project or select an existing project.
Navigate to Authentication > Sign-in method.
Enable Email/Password sign-in.
Navigate to Project settings > Service accounts.
Click on Generate new private key. This will download a .json key.
Save the contents of the downloaded key as a secret in Streamlit (or in a .env file if running locally). The key in this project is named textkey.
Running the App
Locally:

bash
Copy code
streamlit run main.py
On Streamlit Sharing:

Push your repo to GitHub.
Create a new app on Streamlit Sharing and link your GitHub repo.
Add the Firebase private key content to Streamlit secrets in the format:
json
Copy code
{
    "textkey": "YOUR_FIREBASE_JSON_KEY_CONTENT"
}
Deploy and enjoy!
License
This project is licensed under the MIT License - see the LICENSE file for details.

Contributing
Fork the repository on GitHub.
Clone the forked repo to your machine.
Make your changes.
Push your changes to your fork on GitHub.
Create a pull request from your fork to the main repository.
