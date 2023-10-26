#account.py
import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, storage

def account():
    st.title('Tarjeta de presentación en QR')

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    def f():
        try:
            user = auth.get_user_by_email(email)
            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            st.session_state.signedout = True
            st.session_state.signout = True
            st.session_state.login_successful = True  # Set a new session state variable
        except:
            st.warning('Login Failed')
            st.session_state.login_successful = False


    def t():
        st.session_state.signout = False
        st.session_state.signedout = False   
        st.session_state.username = ''

    if "signedout" not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False    

    if not st.session_state["signedout"]: 
        login_tab, signup_tab = st.tabs(['Login', 'Sign up'])

        with login_tab:
            email = st.text_input('Email Address', key='login_email')
            password = st.text_input('Password', type='password', key='login_password')
            if st.button('Login'):
                f()

        with signup_tab:
            email = st.text_input('Email Address', key='signup_email')
            password = st.text_input('Password', type='password', key='signup_password')
            confirm_password = st.text_input('Confirm Password', type='password', key='signup_confirm_password')
            if st.button('Crear cuenta'):
                if password == confirm_password:
                    try:
                        user = auth.create_user(email=email, password=password)
                        st.success('Cuenta creada exitosamente')
                        st.markdown('Ingresar con email y  password') 
                    except Exception as e:
                        st.error(f"Error creating user: {e}")
                else:
                    st.error("Passwords incorrecto")






            
        

        



