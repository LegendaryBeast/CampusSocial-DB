# Social Platform Database Project

A complete working database system with a minimal web interface for a social/community platform.

## password

Email: abdullah500@gmail.com | Password: Abdullah123
Email: zubayer22@gmail.com | Password: zubzub123
Email: ishtiaque-cse@sust.edu | Password: teacher123
Email: tanzimp6@gmail.com | Password: admin123
Live link : https://campussocial-db.onrender.com/
note : use the already created account, because free version of Render do not support SQLite.

## Features

- **User Management**: Registration, login, and user profiles
- **Posts**: Create posts with content and media URLs
- **Likes**: Like and unlike posts
- **Comments**: Comment on posts
- **Events**: Create and view events
- **Resources**: Share and view resources
- **Messages**: Send and receive messages between users

## Database Schema

The database consists of 7 tables:
- **User**: User accounts with name, email, password, role, and profile picture
- **Post**: User posts with content and media URLs
- **Like**: Post likes by users
- **Comment**: Comments on posts
- **Events**: Events created by users
- **Resources**: Resources shared by users
- **Message**: Messages between users

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize the database:**
   The database will be automatically created when you first run the application.

## Running the Application

1. **Start the Flask server:**
   ```bash
   python app.py
   ```

2. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

## Usage

1. **Register a new account:**
   - Click "Register here" on the login page
   - Fill in your name, email, password, and role
   - Submit the form

2. **Login:**
   - Enter your email and password
   - Click "Login"

3. **Create Posts:**
   - Go to Dashboard
   - Write your post content
   - Optionally add a media URL
   - Click "Post"

4. **Interact with Posts:**
   - Like posts by clicking the "Like" button
   - Add comments by typing in the comment box and clicking "Comment"

5. **Create Events:**
   - Navigate to "Events" in the navbar
   - Fill in event details (title, description, date, image URL)
   - Click "Create Event"

6. **Share Resources:**
   - Navigate to "Resources" in the navbar
   - Add resource details (title, description, file URL)
   - Click "Add Resource"

7. **Send Messages:**
   - Navigate to "Messages" in the navbar
   - Select a user from the conversations list or start a new conversation
   - Type your message and click "Send"

## Database File

The database is stored in `database.db` (SQLite format). You can inspect it using any SQLite browser or command-line tool.

## Project Structure

```
DB_Project/
├── app.py              # Flask application
├── schema.sql          # Database schema
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── database.db         # SQLite database (created automatically)
└── templates/          # HTML templates
    ├── base.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── events.html
    ├── resources.html
    └── messages.html
```

## Notes

- Passwords are hashed using SHA-256 (for production, consider using bcrypt)
- The application uses SQLite for simplicity (no database server required)
- All foreign key relationships are properly enforced
- The database schema matches the ER diagram provided

## Security Considerations

For production use, consider:
- Using bcrypt or Argon2 for password hashing
- Implementing CSRF protection
- Using environment variables for the secret key
- Adding input validation and sanitization
- Implementing rate limiting
- Using HTTPS

