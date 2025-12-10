from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import hashlib
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'
DATABASE = 'database.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with schema"""
    conn = sqlite3.connect(DATABASE)
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.close()

def hash_password(password):
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

# Home/Login Page
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = hash_password(request.form['password'])
        role = request.form.get('role', 'student')
        
        conn = get_db()
        try:
            conn.execute('INSERT INTO User (name, email, password, role) VALUES (?, ?, ?, ?)',
                        (name, email, password, role))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            flash('Email already exists!', 'error')
        finally:
            conn.close()
    return render_template('register.html')

# Login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = hash_password(request.form['password'])
    
    conn = get_db()
    user = conn.execute('SELECT * FROM User WHERE email = ? AND password = ?',
                       (email, password)).fetchone()
    conn.close()
    
    if user:
        session['user_id'] = user['user_id']
        session['user_name'] = user['name']
        session['user_role'] = user['role']
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid email or password!', 'error')
        return redirect(url_for('index'))

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    conn = get_db()
    
    # Get all posts with user info, likes count, and comments count
    posts = conn.execute('''
        SELECT p.*, u.name as user_name, u.profile_pic,
               COUNT(DISTINCT l.like_id) as like_count,
               COUNT(DISTINCT c.comment_id) as comment_count
        FROM Post p
        JOIN User u ON p.user_id = u.user_id
        LEFT JOIN Likes l ON p.post_id = l.post_id
        LEFT JOIN Comment c ON p.post_id = c.post_id
        GROUP BY p.post_id
        ORDER BY p.created_at DESC
    ''').fetchall()
    
    # Get comments for each post
    comments_dict = {}
    for post in posts:
        comments = conn.execute('''
            SELECT c.*, u.name as user_name
            FROM Comment c
            JOIN User u ON c.user_id = u.user_id
            WHERE c.post_id = ?
            ORDER BY c.created_at ASC
        ''', (post['post_id'],)).fetchall()
        comments_dict[post['post_id']] = comments
    
    # Check which posts user has liked
    user_likes = conn.execute('''
        SELECT post_id FROM Likes WHERE user_id = ?
    ''', (session['user_id'],)).fetchall()
    liked_posts = {row['post_id'] for row in user_likes}
    
    conn.close()
    
    return render_template('dashboard.html', posts=posts, comments_dict=comments_dict, 
                         liked_posts=liked_posts)

# Create Post
@app.route('/post/create', methods=['POST'])
def create_post():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    content = request.form['content']
    media_url = request.form.get('media_url', '')
    
    conn = get_db()
    conn.execute('INSERT INTO Post (user_id, content, media_url) VALUES (?, ?, ?)',
                (session['user_id'], content, media_url))
    conn.commit()
    conn.close()
    
    flash('Post created successfully!', 'success')
    return redirect(url_for('dashboard'))

# Like/Unlike Post
@app.route('/post/<int:post_id>/like', methods=['POST'])
def toggle_like(post_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    conn = get_db()
    existing_like = conn.execute('SELECT * FROM Likes WHERE post_id = ? AND user_id = ?',
                                (post_id, session['user_id'])).fetchone()
    
    if existing_like:
        conn.execute('DELETE FROM Likes WHERE post_id = ? AND user_id = ?',
                    (post_id, session['user_id']))
        flash('Post unliked!', 'info')
    else:
        conn.execute('INSERT INTO Likes (post_id, user_id) VALUES (?, ?)',
                    (post_id, session['user_id']))
        flash('Post liked!', 'success')
    
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

# Add Comment
@app.route('/post/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    comment_text = request.form['comment_text']
    
    conn = get_db()
    conn.execute('INSERT INTO Comment (post_id, user_id, comment_text) VALUES (?, ?, ?)',
                (post_id, session['user_id'], comment_text))
    conn.commit()
    conn.close()
    
    flash('Comment added!', 'success')
    return redirect(url_for('dashboard'))

# Events Page
@app.route('/events')
def events():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    conn = get_db()
    events = conn.execute('''
        SELECT e.*, u.name as user_name
        FROM Events e
        JOIN User u ON e.user_id = u.user_id
        ORDER BY e.event_date ASC
    ''').fetchall()
    conn.close()
    
    return render_template('events.html', events=events)

# Create Event
@app.route('/event/create', methods=['POST'])
def create_event():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    title = request.form['title']
    description = request.form.get('description', '')
    event_date = request.form['event_date']
    image = request.form.get('image', '')
    
    conn = get_db()
    conn.execute('INSERT INTO Events (user_id, title, description, event_date, image) VALUES (?, ?, ?, ?, ?)',
                (session['user_id'], title, description, event_date, image))
    conn.commit()
    conn.close()
    
    flash('Event created successfully!', 'success')
    return redirect(url_for('events'))

# Resources Page
@app.route('/resources')
def resources():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    conn = get_db()
    resources = conn.execute('''
        SELECT r.*, u.name as user_name
        FROM Resources r
        JOIN User u ON r.user_id = u.user_id
        ORDER BY r.created_at DESC
    ''').fetchall()
    conn.close()
    
    return render_template('resources.html', resources=resources)

# Create Resource
@app.route('/resource/create', methods=['POST'])
def create_resource():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    title = request.form['title']
    description = request.form.get('description', '')
    file_url = request.form.get('file_url', '')
    
    conn = get_db()
    conn.execute('INSERT INTO Resources (user_id, title, description, file_url) VALUES (?, ?, ?, ?)',
                (session['user_id'], title, description, file_url))
    conn.commit()
    conn.close()
    
    flash('Resource created successfully!', 'success')
    return redirect(url_for('resources'))

# Messages Page
@app.route('/messages')
def messages():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    conn = get_db()
    
    # Get all users for messaging
    users = conn.execute('SELECT user_id, name, email FROM User WHERE user_id != ?',
                        (session['user_id'],)).fetchall()
    
    # Get conversations (messages sent to or received from current user)
    conversations = conn.execute('''
        SELECT DISTINCT 
            CASE 
                WHEN sender_id = ? THEN receiver_id 
                ELSE sender_id 
            END as other_user_id,
            u.name as other_user_name
        FROM Message m
        JOIN User u ON (CASE WHEN m.sender_id = ? THEN m.receiver_id ELSE m.sender_id END = u.user_id)
        WHERE sender_id = ? OR receiver_id = ?
        ORDER BY (SELECT MAX(created_at) FROM Message 
                 WHERE (sender_id = ? AND receiver_id = other_user_id) 
                 OR (sender_id = other_user_id AND receiver_id = ?)) DESC
    ''', (session['user_id'], session['user_id'], session['user_id'], session['user_id'], 
          session['user_id'], session['user_id'])).fetchall()
    
    # Get selected conversation messages
    other_user_id = request.args.get('user_id', type=int)
    messages = []
    if other_user_id:
        messages = conn.execute('''
            SELECT m.*, u1.name as sender_name, u2.name as receiver_name
            FROM Message m
            JOIN User u1 ON m.sender_id = u1.user_id
            JOIN User u2 ON m.receiver_id = u2.user_id
            WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
            ORDER BY m.created_at ASC
        ''', (session['user_id'], other_user_id, other_user_id, session['user_id'])).fetchall()
        
        # Mark messages as read
        conn.execute('UPDATE Message SET is_read = 1 WHERE sender_id = ? AND receiver_id = ?',
                    (other_user_id, session['user_id']))
        conn.commit()
    
    conn.close()
    
    return render_template('messages.html', users=users, conversations=conversations, 
                         messages=messages, selected_user_id=other_user_id)

# Send Message
@app.route('/message/send', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    receiver_id = request.form['receiver_id']
    content = request.form['content']
    
    conn = get_db()
    conn.execute('INSERT INTO Message (sender_id, receiver_id, content) VALUES (?, ?, ?)',
                (session['user_id'], receiver_id, content))
    conn.commit()
    conn.close()
    
    flash('Message sent!', 'success')
    return redirect(url_for('messages', user_id=receiver_id))

if __name__ == '__main__':
    # Initialize database if it doesn't exist
    if not os.path.exists(DATABASE):
        init_db()
        print(f"Database '{DATABASE}' initialized!")
    
    app.run(debug=True, host='0.0.0.0', port=5001)

