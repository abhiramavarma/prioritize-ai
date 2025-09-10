# PrioritizeAI - Intelligent Task Management System

## Overview

PrioritizeAI is an intelligent task management system designed to streamline the handling of incoming messages and requests by leveraging machine learning for automatic prioritization. This system is particularly useful in environments where a high volume of requests can lead to critical issues being overlooked due to inefficient processing methods. By analyzing message content, PrioritizeAI classifies issues into high, medium, or low priority, ensuring that urgent matters are addressed promptly.

## Features

-   **User Authentication & Authorization**: Secure login with email and password, supporting two roles:
    -   **Users**: Can submit new messages and track the status of their submissions.
    -   **Admins**: Have access to a comprehensive dashboard to view, manage, and override the priority and status of all messages.
-   **AI-Powered Priority Classification**: Utilizes the Google Gemini API for natural language processing to accurately predict message priority (high, medium, low) based on content.
-   **Intuitive Dashboard**: Admins can view messages sorted by priority, with visual indicators for status and priority levels.
-   **Real-time Updates**: The admin dashboard features an auto-refresh mechanism to display the latest messages and status changes.
-   **Message Management**: Admins can easily update message statuses (pending, in-progress, resolved) and override AI-predicted priorities.
-   **CSV Export**: Functionality to export all messages, including their details and priority, into a CSV file with built-in formula injection protection.
-   **Responsive Frontend**: Built with Flask templates, Bootstrap 5, and Font Awesome for a modern, responsive, and user-friendly interface.
-   **Secure**: Implements CSRF protection on all forms and uses Werkzeug for secure password hashing.

## System Architecture

### Backend

The backend is a **Flask-based web application** handling user authentication, message submission, and API interactions. It uses:
-   **SQLite database**: For data persistence, storing user credentials and message details.
-   **Werkzeug Security**: For robust password hashing and user session management.
-   **Google Gemini API**: Integrated for real-time, intelligent message prioritization.

### Frontend

The frontend is designed for clarity and ease of use, featuring:
-   **Jinja2 Templating**: For dynamic content rendering and consistent layout across pages.
-   **Bootstrap 5**: Provides a responsive and modern design framework.
-   **Font Awesome**: For a rich set of icons to enhance user interface elements.
-   **Dynamic UI**: JavaScript for features like auto-refreshing dashboards and interactive modals.

## Setup and Installation

To get PrioritizeAI up and running on your local machine, follow these steps:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/PrioritizeAI.git
    cd PrioritizeAI
    ```

2.  **Set up a virtual environment** (recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: If `requirements.txt` is not present, you can generate it from `pyproject.toml` using `pip install poetry` and then `poetry export -f requirements.txt --output requirements.txt --without-hashes`)*

4.  **Configure Environment Variables**:
    Create a `.env` file in the root directory and add the following:
    ```
    SECRET_KEY="your_super_secret_key_here"
    GEMINI_API_KEY="your_google_gemini_api_key_here"
    FLASK_DEBUG=True # Set to False for production
    ```
    -   `SECRET_KEY`: A strong, random string for Flask session security.
    -   `GEMINI_API_KEY`: Obtain this from the Google AI Studio or Google Cloud Console.
    -   `FLASK_DEBUG`: Set to `True` for development, `False` for production.

5.  **Initialize the Database**:
    The application will automatically initialize the SQLite database and create a default admin user (`admin@example.com` with password `admin`) on its first run.

6.  **Run the Application**:
    ```bash
    python app.py
    ```

    The application will be accessible at `http://127.0.0.1:5000`.

## Usage

### User Workflow

1.  **Register/Login**: Create a new user account or log in with existing credentials.
2.  **Submit Message**: Navigate to the "Submit New Message" page and describe your issue or request. The AI will automatically assign a priority.
3.  **View Messages**: Check your personal dashboard to see the status and priority of your submitted messages.

### Admin Workflow

1.  **Login**: Log in with admin credentials (`admin@example.com`, password `admin`).
2.  **Admin Dashboard**: View all submitted messages, sorted by priority.
3.  **Update Messages**: Click the "Edit" button to change a message's status or override its AI-predicted priority.
4.  **Export Data**: Download a CSV of all messages for record-keeping or further analysis.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please feel free to:
1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/YourFeature`).
3.  Make your changes and commit them (`git commit -m 'Add YourFeature'`).
4.  Push to the branch (`git push origin feature/YourFeature`).
5.  Open a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any questions or feedback, please open an issue on the GitHub repository.