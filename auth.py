import hashlib
import secrets
import streamlit as st

import database

# -------------------------------
# PASSWORD HASHING
# -------------------------------

def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100_000
    ).hex()

    return password_hash, salt


def verify_password(password, salt, password_hash):
    check_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(check_hash, password_hash)


# -------------------------------
# SIGNUP / LOGIN LOGIC
# -------------------------------

def signup(username, password, confirm_password):
    username = username.strip()

    if not username or not password:
        return False, "Username and password cannot be empty."

    if len(password) < 6:
        return False, "Password must be at least 6 characters long."

    if password != confirm_password:
        return False, "Passwords do not match."

    if database.get_user(username):
        return False, "That username is already taken."

    password_hash, salt = hash_password(password)
    created = database.create_user(username, password_hash, salt)

    if not created:
        return False, "That username is already taken."

    return True, "Account created successfully! You can now log in."


def login(username, password):
    username = username.strip()

    user = database.get_user(username)

    if not user:
        return False, "Invalid username or password."

    if not verify_password(password, user["salt"], user["password_hash"]):
        return False, "Invalid username or password."

    return True, "Logged in successfully!"


# -------------------------------
# SESSION STATE HELPERS
# -------------------------------

def init_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "username" not in st.session_state:
        st.session_state.username = None


def is_logged_in():
    init_session_state()
    return st.session_state.logged_in


def logout():
    st.session_state.logged_in = False
    st.session_state.username = None


def require_login():
    """Call at the top of any protected page. Stops the page if not logged in."""
    init_session_state()

    if not st.session_state.logged_in:
        st.warning("Please log in from the main Meditrak page to view this page.")
        st.stop()


# -------------------------------
# UI COMPONENTS
# -------------------------------

def login_form():
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Log In")

        if submitted:
            success, message = login(username, password)

            if success:
                st.session_state.logged_in = True
                st.session_state.username = username.strip()
                st.success(message)
                st.rerun()
            else:
                st.error(message)


def signup_form():
    with st.form("signup_form"):
        username = st.text_input("Choose a Username")
        password = st.text_input("Choose a Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        submitted = st.form_submit_button("Sign Up")

        if submitted:
            success, message = signup(username, password, confirm_password)

            if success:
                st.success(message)
            else:
                st.error(message)


def auth_gate():
    """Renders Login / Sign Up tabs. Returns True once the user is logged in."""
    init_session_state()

    if st.session_state.logged_in:
        return True

    st.title("Meditrak Demand Forecasting")
    st.write("Log in or create an account to continue.")

    login_tab, signup_tab = st.tabs(["Log In", "Sign Up"])

    with login_tab:
        login_form()

    with signup_tab:
        signup_form()

    return False


def logout_button():
    with st.sidebar:
        st.write(f"Logged in as **{st.session_state.username}**")

        if st.button("Log Out"):
            logout()
            st.rerun()
