import hashlib
from database import SessionLocal, User

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username, password):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user and user.password == hash_password(password):
            # Return a dictionary with user information instead of the SQLAlchemy object
            return {
                'id': user.id,
                'username': user.username,
                'is_admin': user.is_admin
            }
        return None
    finally:
        db.close()

def create_user(username, password, is_admin=False):
    db = SessionLocal()
    try:
        # Check if this is the first user
        user_count = db.query(User).count()
        # If it's the first user, make them an admin
        if user_count == 0:
            is_admin = True
            
        user = User(
            username=username,
            password=hash_password(password),
            is_admin=is_admin
        )
        db.add(user)
        db.commit()
        # Return user info as dictionary instead of SQLAlchemy object
        return {
            'id': user.id,
            'username': user.username,
            'is_admin': user.is_admin
        }
    except:
        db.rollback()
        return None
    finally:
        db.close()