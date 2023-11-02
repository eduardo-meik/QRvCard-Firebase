#account.py
import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, storage


def signout():
    st.session_state['signedout'] = True
    st.session_state['username'] = ''
    st.session_state['login_successful'] = False
    st.experimental_rerun()

def login_user(email, password):
    try:
        user = auth.get_user_by_email(email)
        st.session_state['username'] = user.uid
        st.session_state['useremail'] = user.email
        st.session_state['signedout'] = False
        st.session_state['login_successful'] = True
    except firebase_admin.auth.AuthError:
        st.error('Login Failed')
        st.session_state['login_successful'] = False

def create_account(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        st.success('Cuenta creada exitosamente. Por favor, ingrese con su email y contraseña.')
    except Exception as e:
        st.error(f"Error creating user: {e}")

def account():
    st.title('Tarjeta de presentación en QR')

    # If the user is signed out, clear the session
    if 'signedout' in st.session_state and st.session_state['signedout']:
        signout()

    # Display signout button if the user is logged in
    if st.session_state.get('login_successful'):
        if st.button('Sign out'):
            signout()

    # If the user is not logged in, display login and signup options
    else:
        login_tab, signup_tab = st.tabs(['Login', 'Sign up'])

        with login_tab:
            email = st.text_input('Email Address', key='login_email')
            password = st.text_input('Password', type='password', key='login_password')
            if st.button('Login', on_click=login_user, args=(email, password)):
                # Button callback handles login
                pass

        with signup_tab:
            signup_email = st.text_input('Email Address', key='signup_email')
            signup_password = st.text_input('Password', type='password', key='signup_password')
            confirm_password = st.text_input('Confirm Password', type='password', key='signup_confirm_password')
            if st.button('Crear cuenta'):
                if signup_password == confirm_password:
                    create_account(signup_email, signup_password)
                else:
                    st.error("Las contraseñas no coinciden.")





            
        

        



