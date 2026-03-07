import os
import json
import hmac
import logging
import hashlib
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from dotenv import load_dotenv

# ============================================================
# Fix #1 - Load credentials securely from .env file
# ============================================================
load_dotenv()
DB_PASSWORD = os.getenv("DB_PASSWORD")
API_KEY = os.getenv("API_KEY")

# ============================================================
# Fix #7 - Setup logging and audit trail
# ============================================================
logging.basicConfig(
    filename='ml_audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ============================================================
# Fix #5 - Authorized users list
# ============================================================
AUTHORIZED_USERS = ["admin", "ml_engineer"]
SECRET_KEY = os.getenv("API_KEY").encode()

# ============================================================
# Fix #2 - Load data safely using JSON
# ============================================================
def load_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    if not file_path.endswith('.json'):
        raise ValueError("Only JSON files are accepted")
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

# ============================================================
# Fix #3 - Validate input data before processing
# ============================================================
def preprocess_data(data):
    if not isinstance(data, list):
        raise TypeError("Data must be a list")
    if len(data) == 0:
        raise ValueError("Data cannot be empty")
    for item in data:
        if not isinstance(item, (int, float)):
            raise TypeError(f"Invalid data type found: {type(item)}")
    return np.array(data)

# ============================================================
# Fix #4 - Use strong hashing algorithm
# ============================================================
def hash_sensitive_data(data):
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', data.encode(), salt, 100000)
    return salt.hex() + ":" + hashed.hex()

# ============================================================
# Fix #5 - Add access control to model training
# ============================================================
def train_model(data, labels, username):
    if username not in AUTHORIZED_USERS:
        raise PermissionError(f"Unauthorized user '{username}' attempted to train the model!")
    model = LogisticRegression()
    model.fit(data, labels)
    print(f"Model trained successfully by authorized user: {username}")
    return model

# ============================================================
# Fix #6 - Save model securely with integrity check
# ============================================================
def save_model(model, file_path):
    if not file_path.endswith('.pkl'):
        raise ValueError("Model file must have .pkl extension")
    joblib.dump(model, file_path)
    with open(file_path, 'rb') as f:
        file_content = f.read()
    signature = hmac.new(SECRET_KEY, file_content, hashlib.sha256).hexdigest()
    with open(file_path + '.sig', 'w') as f:
        f.write(signature)
    print(f"Model saved securely with integrity signature: {signature[:10]}...")

# ============================================================
# Fix #7 - Add logging and monitoring to predictions
# ============================================================
def predict(model, input_data, username):
    if username not in AUTHORIZED_USERS:
        logging.warning(f"UNAUTHORIZED prediction attempt by user: {username}")
        raise PermissionError(f"Unauthorized user '{username}' attempted to predict!")
    logging.info(f"Prediction requested by: {username}")
    result = model.predict(input_data)
    logging.info(f"Prediction completed successfully by: {username} | Result: {result}")
    return result

# ============================================================
# Fix #1 - Main execution, never expose credentials
# ============================================================
if __name__ == "__main__":
    if DB_PASSWORD is None or API_KEY is None:
        raise EnvironmentError("Missing credentials! Check your .env file")
    logging.info("Application started successfully")
    print("Application started - credentials loaded securely from .env file")
    print("No sensitive information will be displayed or logged")
