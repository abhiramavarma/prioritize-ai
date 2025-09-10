import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import re

def preprocess_text(text):
    """Clean and preprocess text data"""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def create_sample_data():
    """Create sample training data for message prioritization"""
    sample_messages = [
        # High priority messages
        ("Server down completely, students cannot access online exam", "high"),
        ("Critical security breach detected in student database", "high"),
        ("Fire alarm system malfunctioning in dormitory", "high"),
        ("Payment system crashed, cannot process tuition payments", "high"),
        ("Network outage affecting entire campus", "high"),
        ("Emergency evacuation needed in building A", "high"),
        ("Database corruption, losing student records", "high"),
        ("Website compromised, personal data at risk", "high"),
        ("Heating system failed in winter dormitory", "high"),
        ("Critical assignment system down before deadline", "high"),
        
        # Medium priority messages
        ("Printer in library not working properly", "medium"),
        ("WiFi connection slow in computer lab", "medium"),
        ("Projector bulb needs replacement in classroom 205", "medium"),
        ("Student portal login issues reported by few users", "medium"),
        ("Cafeteria POS system occasionally freezing", "medium"),
        ("Air conditioning unit making noise in office", "medium"),
        ("Some students having trouble with course registration", "medium"),
        ("Email notifications arriving with delay", "medium"),
        ("Library computer runs slowly", "medium"),
        ("Parking gate sensor needs calibration", "medium"),
        ("Classroom whiteboard marker dried out", "medium"),
        ("Online gradebook shows incorrect formatting", "medium"),
        
        # Low priority messages
        ("Request for new software installation on personal laptop", "low"),
        ("Question about how to change password", "low"),
        ("Suggestion to improve cafeteria menu", "low"),
        ("Request for additional parking spaces", "low"),
        ("Inquiry about campus tour schedule", "low"),
        ("Feedback about website design preferences", "low"),
        ("Request for more comfortable chairs in library", "low"),
        ("Question about IT support hours", "low"),
        ("Suggestion for new recreational activities", "low"),
        ("Request for additional power outlets in study areas", "low"),
        ("Inquiry about software training sessions", "low"),
        ("General feedback about campus facilities", "low"),
        ("Request for updated campus map", "low"),
        ("Question about printer paper refill process", "low"),
        ("Suggestion for extended library hours", "low")
    ]
    
    # Convert to DataFrame with explicit column specification
    df = pd.DataFrame(sample_messages)
    df.columns = ['message', 'priority']
    return df

def train_model():
    """Train the priority prediction model"""
    print("Creating sample training data...")
    df = create_sample_data()
    
    print(f"Training data shape: {df.shape}")
    print(f"Priority distribution:\n{df['priority'].value_counts()}")
    
    # Preprocess text data
    print("Preprocessing text data...")
    df['processed_message'] = df['message'].apply(preprocess_text)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        df['processed_message'], df['priority'], 
        test_size=0.2, random_state=42, stratify=df['priority']
    )
    
    # Create TF-IDF vectorizer
    print("Creating TF-IDF vectors...")
    vectorizer = TfidfVectorizer(
        max_features=1000,
        stop_words='english',
        ngram_range=(1, 2)
    )
    
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # Train model
    print("Training Logistic Regression model...")
    model = LogisticRegression(random_state=42, class_weight='balanced')
    model.fit(X_train_vec, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test_vec)
    print("\nModel Performance:")
    print(classification_report(y_test, y_pred))
    
    # Save model and vectorizer
    print("Saving model...")
    model_data = {
        'model': model,
        'vectorizer': vectorizer
    }
    
    joblib.dump(model_data, 'priority_model.pkl')
    print("Model saved as priority_model.pkl")
    
    # Test with sample predictions
    print("\nSample predictions:")
    test_messages = [
        "Server is completely down and students cannot login",
        "Printer in room 101 is out of paper",
        "Suggestion for better food in cafeteria"
    ]
    
    for msg in test_messages:
        processed = preprocess_text(msg)
        prediction = model.predict(vectorizer.transform([processed]))[0]
        print(f"Message: '{msg}' -> Priority: {prediction}")

if __name__ == "__main__":
    train_model()