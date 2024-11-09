# medi_ar_helper.py
import sqlite3
import cv2
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import json

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize the lemmatizer and stop words
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Initialize SQLite database connection
def init_database():
    conn = sqlite3.connect('medi_ar_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MedicalData (
            id INTEGER PRIMARY KEY,
            query TEXT,
            response TEXT,
            image_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function for NLP-based medical response
def analyze_text(query):
    tokens = word_tokenize(query.lower())
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalpha() and word not in stop_words]
    keywords = ' '.join(tokens)
    
    # Dummy response based on keyword matching
    response_map = {
        "fever": "For fever, drink plenty of fluids and rest. If fever persists, consult a doctor.",
        "headache": "For headaches, try staying hydrated and taking a break. Persistent pain may need consultation."
    }
    response = response_map.get(keywords, "I'm sorry, I don't have information on that condition right now.")
    save_response_to_db(query, response)
    
    return response

# Function to save query and response to the database
def save_response_to_db(query, response, image_path=None):
    conn = sqlite3.connect('medi_ar_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO MedicalData (query, response, image_path) VALUES (?, ?, ?)", (query, response, image_path))
    conn.commit()
    conn.close()

# Function for image processing - convert image for AR display
def process_image(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None:
            return "Error: Unable to read the image file."

        # Convert to grayscale and resize for AR display
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        resized_img = cv2.resize(gray_img, (300, 300))

        # Save processed image
        processed_path = image_path.split('.')[0] + "_processed.png"
        cv2.imwrite(processed_path, resized_img)
        
        # Save processed image path to database
        save_response_to_db(query=None, response=None, image_path=processed_path)
        
        return f"Processed image saved at: {processed_path}"
    except Exception as e:
        return f"Image processing failed: {e}"

# Function to retrieve all records from the database
def get_all_records():
    conn = sqlite3.connect('medi_ar_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM MedicalData")
    records = cursor.fetchall()
    conn.close()
    
    return json.dumps(records, indent=4)

# Initialize the database upon module load
init_database()

# Example usage
if __name__ == "__main__":
    # Text analysis example
    query = "What should I do if I have a headache?"
    response = analyze_text(query)
    print(f"Response: {response}")

    # Image processing example
    processed_image_info = process_image("sample_medical_image.jpg")
    print(processed_image_info)

    # Retrieve and display all records
    all_records = get_all_records()
    print("Database records:", all_records)
