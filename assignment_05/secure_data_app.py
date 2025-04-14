import streamlit as st
import hashlib           # Used to hash passkeys for security.
from cryptography.fernet import Fernet  # From the cryptography library, used to encrypt and decrypt your data securely.

# Initialize session state variables
if 'fernet_key' not in st.session_state:
    st.session_state.fernet_key = Fernet.generate_key()
    st.session_state.cipher = Fernet(st.session_state.fernet_key)

if 'stored_data' not in st.session_state:
    st.session_state.stored_data = {}  # {username: {"encrypted_text": ..., "passkey": ...}}

if 'users' not in st.session_state:
    st.session_state.users = {}  # {username: hashed_passkey}

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0

# Function to hash passkey
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Function to encrypt data
def encrypt_data(text):
    return st.session_state.cipher.encrypt(text.encode()).decode()

# Function to decrypt data
def decrypt_data(encrypted_text):
    return st.session_state.cipher.decrypt(encrypted_text.encode()).decode()

# Streamlit UI
st.title("\U0001F512 Secure Data Encryption System")

# Navigation
menu = ["Home", "Register", "Login", "Store Data", "Retrieve Data"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Home":
    st.subheader("\U0001F3E0 Welcome to the Secure Data System")
    st.write("Use this app to **register**, **login**, and securely **store** and **retrieve** data.")

elif choice == "Register":
    st.subheader("📅 Register New User")
    new_username = st.text_input("Choose a username")
    new_passkey = st.text_input("Choose a passkey", type="password")

    if st.button("Register"):
        if new_username in st.session_state.users:
            st.error("Username already exists. Please choose another one.")
        elif new_username and new_passkey:
            st.session_state.users[new_username] = hash_passkey(new_passkey)
            st.success("User registered successfully! You can now login.")
        else:
            st.error("Both fields are required!")

elif choice == "Login":
    st.subheader("🔑 Login")
    username = st.text_input("Username")
    passkey = st.text_input("Passkey", type="password")

    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username] == hash_passkey(passkey):
            st.session_state.current_user = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid username or passkey.")

elif choice == "Store Data":
    if not st.session_state.current_user:
        st.warning("Please login first.")
    else:
        st.subheader("\U0001F4C2 Store Data Securely")
        user_data = st.text_area("Enter Data:")

        if st.button("Encrypt & Save"):
            if user_data:
                encrypted_text = encrypt_data(user_data)
                st.session_state.stored_data[st.session_state.current_user] = {
                    "encrypted_text": encrypted_text,
                    "passkey": st.session_state.users[st.session_state.current_user]
                }
                st.success("\u2705 Data stored securely!")
                st.text_area("Your Encrypted Data:", encrypted_text, height=100)
            else:
                st.error("\u26A0\uFE0F Data field is required!")

elif choice == "Retrieve Data":
    if not st.session_state.current_user:
        st.warning("Please login first.")
    else:
        st.subheader("\U0001F50D Retrieve Your Data")

        if st.session_state.current_user in st.session_state.stored_data:
            encrypted_text = st.session_state.stored_data[st.session_state.current_user]["encrypted_text"]
            decrypted_text = decrypt_data(encrypted_text)
            st.success(f"\u2705 Your Decrypted Data: {decrypted_text}")
        else:
            st.info("No data stored for this user yet.")