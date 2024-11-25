import streamlit as st
import io
from PIL import Image
from database import SessionLocal, APKFile, User
from auth import verify_user, create_user

def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user' not in st.session_state:
        st.session_state.user = None

def login_page():
    st.title("APK Store - Login")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            user = verify_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    with tab2:
        new_username = st.text_input("New Username", key="reg_username")
        new_password = st.text_input("New Password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
        
        if st.button("Register"):
            if new_password != confirm_password:
                st.error("Passwords don't match")
            else:
                user = create_user(new_username, new_password)
                if user:
                    if user['is_admin']:
                        st.success("Registration successful! You have been registered as an admin user. Please login.")
                    else:
                        st.success("Registration successful! Please login.")
                else:
                    st.error("Username already exists")

def upload_apk():
    st.title("Upload APK")
    
    name = st.text_input("APK Name")
    version = st.text_input("Version")
    description = st.text_area("Description")
    icon_file = st.file_uploader("Upload Icon", type=['png', 'jpg', 'jpeg'])
    apk_file = st.file_uploader("Upload APK", type=['apk'])
    
    if st.button("Upload"):
        if name and version and icon_file and apk_file:
            # Process icon
            icon_bytes = icon_file.read()
            
            # Process APK file
            apk_bytes = apk_file.read()
            
            db = SessionLocal()
            try:
                new_apk = APKFile(
                    name=name,
                    version=version,
                    description=description,
                    icon=icon_bytes,
                    file=apk_bytes,
                    uploaded_by=st.session_state.user['id']
                )
                db.add(new_apk)
                db.commit()
                st.success("APK uploaded successfully!")
            except Exception as e:
                db.rollback()
                st.error(f"Error uploading APK: {str(e)}")
            finally:
                db.close()
        else:
            st.error("Please fill all required fields")

def display_apks():
    st.title("Available APKs")
    
    db = SessionLocal()
    apks = db.query(APKFile).all()
    
    # Display APKs in a grid layout
    cols = st.columns(2)
    for idx, apk in enumerate(apks):
        col = cols[idx % 2]
        with col:
            # Create card-like container
            with st.container():
                st.markdown("""
                    <style>
                        .apk-card {
                            padding: 1rem;
                            border: 1px solid #ddd;
                            border-radius: 8px;
                            margin-bottom: 1rem;
                        }
                    </style>
                """, unsafe_allow_html=True)
                
                # Display icon
                if apk.icon:
                    icon = Image.open(io.BytesIO(apk.icon))
                    st.image(icon, width=100)
                
                st.markdown(f"**{apk.name}**")
                st.markdown(f"Version: {apk.version}")
                if apk.description:
                    st.markdown(f"Description: {apk.description}")
                
                # Download button
                if st.download_button(
                    "Download APK",
                    data=apk.file,
                    file_name=f"{apk.name}-{apk.version}.apk",
                    mime="application/vnd.android.package-archive"
                ):
                    st.success("Download started!")
                st.markdown("------")
    
    db.close()

def main():
    init_session_state()
    
    if not st.session_state.logged_in:
        login_page()
    else:
        st.sidebar.title(f"Welcome, {st.session_state.user['username']}")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
        
        # Navigation
        pages = {
            "Browse APKs": display_apks
        }
        
        if st.session_state.user['is_admin']:
            pages["Upload APK"] = upload_apk
        
        page = st.sidebar.selectbox("Navigation", list(pages.keys()))
        pages[page]()

if __name__ == "__main__":
    main()
