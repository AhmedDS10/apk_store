# APK Store Application

This is a simple APK store application built with Streamlit and SQLAlchemy.

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Initialize the database (first run will create the database):
```bash
python app.py
```

4. Run the application:
```bash
streamlit run app.py
```

## Features

- User authentication (login/register)
- Admin users can upload APK files
- Browse APKs in a card-style layout
- Download APK files
- Secure password hashing
- File upload support for APK files and icons

## Database Schema

- Users table: Stores user information and admin status
- APK_files table: Stores APK files and metadata

## Security Notes

- Passwords are hashed using SHA-256
- Admin privileges are required for uploading APKs
- Binary files are stored in SQLite database