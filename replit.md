# PrioritizeAI - ML-Based Task Management System

## Overview

PrioritizeAI is an intelligent task management system that uses machine learning to automatically prioritize messages and requests. The system is designed for educational institutions where teachers and managers receive multiple problem reports and need efficient prioritization to handle urgent issues first. The application uses natural language processing to analyze message content and predict priority levels (high, medium, low), replacing inefficient FIFO processing with intelligent ML-based prioritization.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Web Framework & Backend
- **Flask-based web application** with session-based authentication
- **Role-based access control** with two user types: regular users (submit messages) and admins (manage and prioritize messages)
- **SQLite database** for data persistence, chosen for simplicity and Replit compatibility
- **Werkzeug security** for password hashing and user authentication

### Machine Learning Pipeline
- **Scikit-learn** for ML model training and inference
- **TF-IDF vectorization** for text feature extraction from message content
- **Logistic regression** classifier for priority prediction (high/medium/low)
- **Model persistence** using joblib for saving/loading trained models
- **Text preprocessing** with regex-based cleaning and normalization

### Database Schema
- **Users table**: Stores user credentials and roles (id, email, password_hash, role)
- **Messages table**: Stores messages with ML predictions and admin overrides (id, user_id, content, predicted_priority, final_priority, status, timestamp)
- **Foreign key relationships** linking messages to users

### Frontend Architecture
- **Bootstrap 5** for responsive UI design
- **Font Awesome** icons for visual enhancement
- **Jinja2 templating** with template inheritance for consistent layout
- **Color-coded priority system** with visual indicators for different priority levels
- **Status tracking** with visual badges for message states (pending, in-progress, resolved)

### Authentication & Authorization
- **Session-based authentication** using Flask sessions
- **Environment variable configuration** for admin account creation
- **Password validation** with minimum length requirements
- **Role-based route protection** ensuring proper access control

### Data Flow Architecture
1. **Message submission**: Users submit messages through web forms
2. **ML processing**: System applies trained model to predict priority
3. **Data persistence**: Messages stored with predicted priorities
4. **Admin workflow**: Admins view prioritized messages and can override priorities
5. **Status updates**: Admins update message status through workflow states
6. **User tracking**: Users can view their messages and status updates

### Training Data & Model
- **Sample dataset creation** with realistic educational institution scenarios
- **Balanced training data** across priority levels with domain-specific examples
- **Text preprocessing pipeline** for consistent feature extraction
- **Model evaluation** using classification reports for performance monitoring

## External Dependencies

### Core Frameworks
- **Flask**: Web application framework for routing and request handling
- **SQLite3**: Embedded database for data storage (built into Python)
- **Werkzeug**: Security utilities for password hashing

### Machine Learning Stack
- **scikit-learn**: ML library for training and inference
- **pandas**: Data manipulation for training data handling
- **joblib**: Model serialization and persistence

### Frontend Libraries
- **Bootstrap 5**: CSS framework for responsive design (CDN)
- **Font Awesome 6**: Icon library for UI enhancement (CDN)

### Python Standard Library
- **os**: Environment variable access and system operations
- **datetime**: Timestamp handling for message tracking
- **re**: Regular expressions for text preprocessing

### Environment Configuration
- **SECRET_KEY**: Flask session security (environment variable)
- **ADMIN_EMAIL/ADMIN_PASSWORD**: Default admin account creation (environment variables)