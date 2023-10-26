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
        except: 
            st.warning('Login Failed')

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False   
        st.session_state.username = ''

    if "signedout" not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False    

    if not st.session_state["signedout"]: 
        choice = st.radio('Choose an action', ('Login', 'Sign up'))
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')

        if choice == 'Sign up':
            confirm_password = st.text_input('Confirm Password', type='password')
            if st.button('Create my account'):
                if password == confirm_password:
                    try:
                        user = auth.create_user(email=email, password=password)
                        st.success('Account created successfully!')
                        st.markdown('Please Login using your email and password')
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error creating user: {e}")
                else:
                    st.error("Passwords don't match!")
        else:
            st.button('Login', on_click=f)

    if st.session_state.signout:
        st.text('Name ' + st.session_state.username)
        st.text('Email id: ' + st.session_state.useremail)
        st.button('Sign out', on_click=t)



            
        

        



