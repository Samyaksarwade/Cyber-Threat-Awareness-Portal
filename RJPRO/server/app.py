from flask import Flask, request, jsonify, render_template, redirect, url_for, abort, send_from_directory
from flask_cors import CORS
from database import initialize_database, get_db_connection
from auth import register_user, login_user, verify_token
import functools
import requests
from datetime import datetime, timedelta
import os
import PyPDF2
import hashlib
import json
from config import YOUTUBE_API_KEY, YOUTUBE_CHANNELS
from youtube_api import YouTubeAPI
from video_updater import video_updater

app = Flask(__name__, 
    template_folder='../templates',
    static_folder='../static'
)
CORS(app)

# Add custom Jinja filters
@app.template_filter('date')
def date_filter(value, format='%B %d, %Y'):
    if value is None:
        return ""
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value)
        except ValueError:
            return value
    return value.strftime(format)

# Initialize database when app starts
with app.app_context():
    initialize_database()
    
# Start the video updater to periodically fetch new videos
video_updater.start()

# Authentication decorator
def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('token')
        if not token or not verify_token(token):
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

# Page routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/quizzes')
def quizzes_page():
    return render_template('quiz.html')

@app.route('/quiz/take')
def take_quiz_page():
    return render_template('take_quiz.html')

@app.route('/quiz/results')
def quiz_results_page():
    return render_template('quiz_results.html')

@app.route('/videos')
def videos_page():
    try:
        # Get videos from cache or fetch from YouTube if cache is not available
        video_categories = video_updater.get_cached_videos()
        
        # If we have videos, render the template with them
        if video_categories:
            return render_template('videos.html', video_categories=video_categories)
        
        # If no videos are available, render the template without them
        # The template will show the fallback static content
        return render_template('videos.html')
    except Exception as e:
        print(f"Error loading videos: {str(e)}")
        # Fallback to static content if there's an error
        return render_template('videos.html')

@app.route('/resources')
def resources_page():
    return render_template('resources.html')

@app.route('/case-studies')
def case_studies_page():
    # Get list of case studies from the caseinfo directory
    case_studies_dir = os.path.join(app.static_folder, 'caseinfo')
    case_studies = []
    
    for filename in os.listdir(case_studies_dir):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(case_studies_dir, filename)
            # Generate a proper title from filename
            raw_title = filename.replace('.pdf', '').replace('_', ' ').title()
            # Remove any C1, C2, etc. from the title
            title = ' '.join([word for word in raw_title.split() if not (word.startswith('C') and word[1:].isdigit())])
            
            case_studies.append({
                'title': title,
                'description': f'Click to view this detailed case study  {title}',
                'filename': filename,
                'date': datetime.fromtimestamp(os.path.getctime(pdf_path)).strftime('%b %d, %Y'),
                'tags': ['Case Study', 'Security Incident'],
                'image_url': '/static/images/case-studies/default.jpg',
                'pdf_url': url_for('static', filename='caseinfo/' + filename)
            })
    
    return render_template('case_studies.html', case_studies=case_studies)

@app.route('/guides')
def guides_page():
    return render_template('guides.html')

@app.route('/threat-map')
def threat_map_page():
    return render_template('threat_map.html')

@app.route('/news')
def news_page():
    news_articles = [
        {
            'title': 'North Korean Hackers Target Freelance Developers in Job Scam to Deploy Malware',
            'description': 'Freelance software developers are the target of an ongoing campaign that leverages job interview-themed lures to deliver cross-platform malware families...',
            'date': 'Feb 20, 2025',
            'image_url': '/static/images/news/korean.jpg',
            'url': url_for('news_detail', article_id='north-korean-hackers'),
            'categories': ['Malware', 'Cryptocurrency']
        },
        {
            'title': 'China-Linked Attackers Exploit Check Point Flaw to Deploy ShadowPad and Ransomware',
            'description': 'A previously unknown threat activity cluster targeted European organizations, particularly those in the healthcare sector, to deploy PlugX and its successor...',
            'date': 'Feb 20, 2025',
            'image_url': '/static/images/news/ransomware.jpg',
            'url': url_for('news_detail', article_id='china-linked-attackers'),
            'categories': ['Ransomware', 'Vulnerability']
        },
        {
            'title': 'DeepSeek limits registrations after large-scale cyber attack',
            'description':'DeepSeek has confirmed the attack and said it is taking precautionary steps to mitigate any further damage, though the extent of the attack remains unclear...',
            'date':'Jan 27 2025',
            'image_url':'/static/images/news/malware.jpg',
            'url': url_for('news_detail',article_id='deepseek-attackers'),
            'categories': ['Malware']
        },
        {
            'title': 'India faces 44% more cyberattacks per week than the rest of the world: Check Point study',
            'description':'Check Point Software report reveals that Indian organisations face 3,291 weekly cyberattacks, 44% above the global average...',
            'date':'Jan 24 2025',
            'image_url':'/static/images/news/india.jpg',
            'categories': ['Cyberattacks','Threat analysis']
        },  
         {
            'title': 'RBI Governor calls upon banks and NBFCs to mitigate cyber risks',
            'description':'RBI Governor Sanjay Malhotra stressed the need for enhanced cyber security in the financial sector.He urged banks...',
            'date':'Feb 07 2025',
            'image_url':'/static/images/news/rbi.jpg',
            'categories': ['Phishing','Financial Fraud']
        },
           {
            'title': 'Rajasthan Doctor Loses Over Rs 62 Lakh In Online Stock Trading Scam',
            'description':'A neurosurgeon from Jodhpur lost Rs 62.8 lakh to cyber criminals who lured him with promises of high returns on stock market investments...',
            'date':'Feb 06 2025',
            'image_url':'/static/images/news/doc.jpg',
            'categories': ['Online Investment Fraud']
        }          
        
    ]
    return render_template('news.html', news_articles=news_articles)

@app.route('/news/<article_id>')
def news_detail(article_id):
    try:
        if article_id == 'north-korean-hackers':
            # Get the absolute path to the PDF file
            pdf_path = os.path.join(app.static_folder, 'newsinfo', 'news1.pdf')
            
            # Check if file exists
            if not os.path.exists(pdf_path):
                print(f"PDF not found at path: {pdf_path}")
                return render_template('error.html', 
                    message="Sorry, the article content is currently unavailable."), 404

            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                content = ""
                for page in pdf_reader.pages:
                    content += page.extract_text()

            article = {
                'title': 'North Korean Hackers Target Freelance Developers in Job Scam to Deploy Malware',
                'date': 'Feb 20, 2025',
                'image_url': '/static/images/news/korean.jpg',
                'categories': ['Malware', 'Cryptocurrency'],
                'content': content.replace('\n', '<br>')
            }
            return render_template('news_detail.html', article=article)
        elif article_id == 'china-linked-attackers':
            # Get the absolute path to the PDF file
            pdf_path = os.path.join(app.static_folder, 'newsinfo', 'news2.pdf')
            
            # Check if file exists
            if not os.path.exists(pdf_path):
                print(f"PDF not found at path: {pdf_path}")
                return render_template('error.html', 
                    message="Sorry, the article content is currently unavailable."), 404

            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                content = ""
                for page in pdf_reader.pages:
                    content += page.extract_text()

            article = {
                'title': 'China-Linked Attackers Exploit Check Point Flaw to Deploy ShadowPad and Ransomware',
                'date': 'Feb 20, 2025',
                'image_url': '/static/images/news/ransomware.jpg',
                'categories': ['Ransomware', 'Vulnerability'],
                'content': content.replace('\n', '<br>')
            }
            return render_template('news_detail.html', article=article)
        elif article_id == 'deepseek-attackers':
            # Get the absolute path to the PDF file
            pdf_path = os.path.join(app.static_folder, 'newsinfo', 'news3.pdf')
            
            # Check if file exists
            if not os.path.exists(pdf_path):
                print(f"PDF not found at path: {pdf_path}")
                return render_template('error.html', 
                    message="Sorry, the article content is currently unavailable."), 404

            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                content = ""
                for page in pdf_reader.pages:
                    content += page.extract_text()

            article = {
                'title': 'DeepSeek limits registrations after large-scale cyber attack',
                'date': 'Jan 27, 2025',
                'image_url': '/static/images/news/malware.jpg',
                'categories': ['Malware'],
                'content': content.replace('\n', '<br>')
            }
            return render_template('news_detail.html', article=article)
        elif article_id == 'india-cyber-attack':
             # Get the absolute path to the PDF file
            pdf_path = os.path.join(app.static_folder, 'newsinfo', 'news4.pdf')
            
            # Check if file exists
            if not os.path.exists(pdf_path):
                print(f"PDF not found at path: {pdf_path}")
                return render_template('error.html', 
                    message="Sorry, the article content is currently unavailable."), 404

            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                content = ""
                for page in pdf_reader.pages:
                    content += page.extract_text()

            article = {
               'title': 'India faces 44% more cyberattacks per week than the rest of the world: Check Point study',
               'date':'Jan 24 2025',
               'image_url':'/static/images/news/india.jpg',
                'categories': ['Cyberattacks','Threat analysis'],
                'content': content.replace('\n', '<br>')
            }
            return render_template('news_detail.html', article=article)
        elif article_id == 'rbi-attack':
             # Get the absolute path to the PDF file
            pdf_path = os.path.join(app.static_folder, 'newsinfo', 'news5.pdf')
            
            # Check if file exists
            if not os.path.exists(pdf_path):
                print(f"PDF not found at path: {pdf_path}")
                return render_template('error.html', 
                    message="Sorry, the article content is currently unavailable."), 404

            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                content = ""
                for page in pdf_reader.pages:
                    content += page.extract_text()

            article = {
               'title': 'RBI Governor calls upon banks and NBFCs to mitigate cyber risks',
               'date':'Feb 07 2025',
               'image_url':'/static/images/news/rbi.jpg',
                'categories': ['Phishing','Financial Fraud'],
                'content': content.replace('\n', '<br>')
            }
            return render_template('news_detail.html', article=article)
        elif article_id == 'scammer-attack':
            # Get the absolute path to the PDF file
            pdf_path = os.path.join(app.static_folder, 'newsinfo', 'news6.pdf')
            
            # Check if file exists
            if not os.path.exists(pdf_path):
                print(f"PDF not found at path: {pdf_path}")
                return render_template('error.html', 
                    message="Sorry, the article content is currently unavailable."), 404

            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                content = ""
                for page in pdf_reader.pages:
                    content += page.extract_text()

            article = {
               'title': 'Rajasthan Doctor Loses Over Rs 62 Lakh In Online Stock Trading Scam',
               'date':'Feb 06 2025',
               'image_url':'/static/images/news/doc.jpg',
               'categories': ['Online Investment Fraud'],
               'content': content.replace('\n', '<br>')
            }
            return render_template('news_detail.html', article=article)
            
        else:
            return render_template('error.html', 
                message="Article not found."), 404
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
        return render_template('error.html', 
            message="An error occurred while loading the article."), 500

@app.route('/profile')
@login_required
def view_profile_page():
    token = request.cookies.get('token')
    user_id = verify_token(token)
    
    # Get user profile data
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get user basic info
    cursor.execute('''
        SELECT id, username, email, profile_image, bio, security_score, 
               job_title, organization, created_at 
        FROM users WHERE id = %s
    ''', (user_id,))
    user = cursor.fetchone()
    
    if not user:
        return redirect(url_for('login_page'))
    
    # Get quiz statistics
    cursor.execute('''
        SELECT COUNT(*) as total_quizzes, AVG(score) as avg_score, MAX(score) as highest_score
        FROM quiz_results WHERE user_id = %s
    ''', (user_id,))
    quiz_stats = cursor.fetchone()
    
    if not quiz_stats:
        quiz_stats = {
            'total_quizzes': 0,
            'avg_score': 0,
            'highest_score': 0
        }
    
    # Get recent activity
    cursor.execute('''
        SELECT activity_type, activity_id, completed, created_at
        FROM user_activity 
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 5
    ''', (user_id,))
    recent_activity = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Prepare profile data for template
    profile = {
        'username': user['username'],
        'email': user['email'],
        'bio': user['bio'] or '',
        'securityScore': user['security_score'] or 70,
        'jobTitle': user['job_title'] or '',
        'organization': user['organization'] or '',
        'joinDate': user['created_at'],
        'quizStats': {
            'totalQuizzes': quiz_stats['total_quizzes'] or 0,
            'averageScore': round(float(quiz_stats['avg_score'] or 0), 1),
            'highestScore': quiz_stats['highest_score'] or 0
        },
        'recentActivity': recent_activity or []
    }
    
    return render_template('profile.html', profile=profile)

@app.route('/profile/edit')
@login_required
def edit_profile_page():
    token = request.cookies.get('token')
    user_id = verify_token(token)
    
    # Get user profile data
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get user basic info
    cursor.execute('''
        SELECT id, username, email, profile_image, bio, security_score, 
               job_title, organization, created_at 
        FROM users WHERE id = %s
    ''', (user_id,))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if not user:
        return redirect(url_for('login_page'))
    
    # Prepare profile data for template
    profile = {
        'username': user['username'],
        'email': user['email'],
        'bio': user['bio'] or '',
        'jobTitle': user['job_title'] or '',
        'organization': user['organization'] or '',
    }
    
    return render_template('edit_profile.html', profile=profile)

@app.route('/articles')
def articles_page():
    """
    Renders the articles page with a list of articles.

    Each article contains an ID, title, filename, and description. 
    The articles are passed to the 'articles_list.html' template for rendering.
    """
    articles = [
        {'id': 1, 'title': ' Article 1', 'filename': 'a1.pdf', 'description': 'Learn about what are phishing attacks'},
        {'id': 2, 'title': ' Article 2', 'filename': 'a2.pdf', 'description': 'Understanding computer security'},
        {'id': 3, 'title': ' Article 3', 'filename': 'a3.pdf', 'description': 'Understand the concept of cyberwarfare'},
        {'id': 4, 'title': ' Article 4', 'filename': 'a4.pdf', 'description': 'Best cybersecurity information technologies'},
        {'id': 5, 'title': ' Article 5', 'filename': 'a5.pdf', 'description': 'What are Ransomeware attacks'}
    ]
    return render_template('articles_list.html', articles=articles)

@app.route('/articles/<filename>')
def view_article(filename):
    articles_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'articles')
    return send_from_directory(articles_dir, filename, as_attachment=False)

# Quiz questions organized by level
QUIZ_QUESTIONS = {
    'easy': [
        {
            'question': 'Which of the following is a strong password?',
            'options': ['12345', 'Password1', 'admin123', 'X7#9!PqT'],
            'correctAnswer': 3
        },
        {
            'question': 'What does a firewall do?',
            'options': [
                'Cleans your computer',
                'Prevents unauthorized access to networks',
                'Boosts internet speed',
                'Stores sensitive data'
            ],
            'correctAnswer': 1
        },
        {
            'question': 'What is phishing?',
            'options': [
                'A type of malware',
                'A method of email-based fraud',
                'A hardware malfunction',
                'An encrypted message'
            ],
            'correctAnswer': 1
        }
    ],
    'medium': [
        {
            'question': 'Which cybersecurity principle ensures data is protected from unauthorized access?',
            'options': ['Confidentiality', 'Integrity', 'Availability', 'Non-repudiation'],
            'correctAnswer': 0
        },
        {
            'question': 'What does two-factor authentication (2FA) require?',
            'options': [
                'Only a password',
                'Two different forms of verification',
                'A username and password',
                'Biometric data only'
            ],
            'correctAnswer': 1
        },
        {
            'question': 'Which type of malware replicates itself to spread to other systems?',
            'options': ['Trojan horse', 'Worm', 'Adware', 'Spyware'],
            'correctAnswer': 1
        }
    ],
    'hard': [
        {
            'question': 'What is the purpose of encryption?',
            'options': [
                'To compress data',
                'To ensure data availability',
                'To protect data by making it unreadable',
                'To format storage devices'
            ],
            'correctAnswer': 2
        },
        {
            'question': 'Which is NOT a good cybersecurity practice?',
            'options': [
                'Using strong and unique passwords',
                'Clicking on unknown links',
                'Updating software regularly',
                'Backing up data'
            ],
            'correctAnswer': 1
        },
        {
            'question': 'What does VPN stand for?',
            'options': [
                'Virtual Private Network',
                'Very Personal Network',
                'Virtual Protection Node',
                'Verified Private Node'
            ],
            'correctAnswer': 0
        }
    ],
    'extreme': [
        {
            'question': 'Which encryption algorithm is considered the most secure?',
            'options': ['DES', 'AES-256', 'MD5', 'SHA-1'],
            'correctAnswer': 1
        },
        {
            'question': 'What is a zero-day vulnerability?',
            'options': [
                'A vulnerability that has existed for 0 days',
                'A vulnerability that has no patch available',
                'A vulnerability that takes 0 days to exploit',
                'A vulnerability that affects day 0 of system installation'
            ],
            'correctAnswer': 1
        },
        {
            'question': 'Which network protocol is most secure for remote administration?',
            'options': ['Telnet', 'FTP', 'SSH', 'HTTP'],
            'correctAnswer': 2
        }
    ]
}

@app.route('/api/quiz/questions', methods=['GET'])
def get_quiz_questions():
    try:
        # Get the quiz level from the request
        level = request.args.get('level', 'easy').lower()
        
        # Validate the level
        if level not in QUIZ_QUESTIONS:
            return jsonify({'error': 'Invalid quiz level'}), 400
            
        # Get questions for the specified level
        questions = QUIZ_QUESTIONS[level]
        
        # Return questions without the correct answers
        return jsonify([{
            'question': q['question'],
            'options': q['options']
        } for q in questions])
        
    except Exception as e:
        print(f"Error getting quiz questions: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# API routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        user_id = register_user(
            data['username'],
            data['email'],
            data['password']
        )
        return jsonify({'success': True, 'user_id': user_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    result = login_user(data['username'], data['password'])
    if result:
        response = jsonify({'success': True, 'user': result['user']})
        response.set_cookie('token', result['token'])
        return response
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout')
def logout():
    response = redirect(url_for('login_page'))
    response.delete_cookie('token')
    return response

@app.route('/api/profile', methods=['GET'])
@login_required
def get_profile():
    try:
        token = request.cookies.get('token')
        decoded = verify_token(token)
        user_id = decoded
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get user basic info
        cursor.execute('''
            SELECT id, username, email, profile_image, bio, security_score, 
                   job_title, organization, created_at 
            FROM users WHERE id = %s
        ''', (user_id,))
        user = cursor.fetchone()
        
        # Get quiz statistics
        cursor.execute('''
            SELECT COUNT(*) as total_quizzes, AVG(score) as avg_score, MAX(score) as highest_score
            FROM quiz_results WHERE user_id = %s
        ''', (user_id,))
        quiz_stats = cursor.fetchone()
        
        # Get recent activity
        cursor.execute('''
            SELECT activity_type, activity_id, completed, created_at
            FROM user_activity 
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT 5
        ''', (user_id,))
        recent_activity = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        return jsonify({
            'username': user['username'],
            'email': user['email'],
            'profileImage': user['profile_image'],
            'bio': user['bio'] or '',
            'securityScore': user['security_score'],
            'jobTitle': user['job_title'] or '',
            'organization': user['organization'] or '',
            'joinDate': user['created_at'].isoformat() if user['created_at'] else None,
            'quizStats': {
                'totalQuizzes': quiz_stats['total_quizzes'],
                'averageScore': round(quiz_stats['avg_score'] or 0, 1),
                'highestScore': quiz_stats['highest_score'] or 0
            },
            'recentActivity': [
                {
                    'type': activity['activity_type'],
                    'id': activity['activity_id'],
                    'completed': activity['completed'],
                    'date': activity['created_at'].isoformat()
                } for activity in recent_activity
            ]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/profile/update', methods=['POST'])
@login_required
def update_profile():
    token = request.cookies.get('token')
    try:
        user_id = verify_token(token)
        
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        bio = data.get('bio')
        job_title = data.get('jobTitle')
        organization = data.get('organization')
        current_password = data.get('currentPassword')
        new_password = data.get('newPassword')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verify current password if changing password
        if new_password:
            cursor.execute('SELECT password FROM users WHERE id = %s', (user_id,))
            user = cursor.fetchone()
            if not user or user['password'] != hashlib.sha256(current_password.encode()).hexdigest():
                cursor.close()
                conn.close()
                return jsonify({'errors': {'currentPassword': 'Current password is incorrect'}}), 400
        
        # Update user data
        updates = []
        values = []
        if username:
            updates.append('username = %s')
            values.append(username)
        if email:
            updates.append('email = %s')
            values.append(email)
        if bio is not None:
            updates.append('bio = %s')
            values.append(bio)
        if job_title is not None:
            updates.append('job_title = %s')
            values.append(job_title)
        if organization is not None:
            updates.append('organization = %s')
            values.append(organization)
        # Set profile_image to default.png for all users
        updates.append('profile_image = %s')
        values.append('default.png')
        if new_password:
            updates.append('password = %s')
            values.append(hashlib.sha256(new_password.encode()).hexdigest())
        
        if updates:
            values.append(user_id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
            cursor.execute(query, values)
            conn.commit()
        
        cursor.close()
        conn.close()
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/quiz/submit', methods=['POST'])
def submit_quiz():
    try:
        data = request.get_json()
        user_answers = data.get('answers', [])
        
        if len(user_answers) != len(QUIZ_QUESTIONS['easy']):
            return jsonify({'error': 'Invalid number of answers'}), 400

        # Calculate results
        correct_count = 0
        results = []
        
        for i, (user_answer, question) in enumerate(zip(user_answers, QUIZ_QUESTIONS['easy'])):
            is_correct = user_answer == question['correctAnswer']
            if is_correct:
                correct_count += 1
            
            results.append({
                'correct': is_correct,
                'correctAnswer': question['correctAnswer']
            })

        score = int((correct_count / len(QUIZ_QUESTIONS['easy'])) * 100)
        
        # Save quiz result if user is logged in
        token = request.cookies.get('token')
        if token:
            try:
                decoded = verify_token(token)
                user_id = decoded['user_id']
                
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO quiz_results (user_id, quiz_name, score) VALUES (%s, %s, %s)",
                    (user_id, 'Cybersecurity Basics', score)
                )
                conn.commit()
                cursor.close()
                conn.close()
            except:
                pass  # Don't fail if we can't save the result
        
        return jsonify({
            'score': score,
            'correctCount': correct_count,
            'incorrectCount': len(QUIZ_QUESTIONS['easy']) - correct_count,
            'answers': results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/newsletter/subscribe', methods=['POST'])
def newsletter_subscribe():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
        
    # Here you would typically add the email to your newsletter database
    # For now, we'll just return a success response
    return jsonify({'success': True, 'message': 'Successfully subscribed to newsletter'})

@app.route('/api/user/stats', methods=['GET'])
@login_required
def get_user_stats():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        user_id = verify_token(request.cookies.get('token'))['user_id']

        # Get completed quizzes count
        cursor.execute("""
            SELECT COUNT(*) as quiz_count 
            FROM quiz_results 
            WHERE user_id = %s
        """, (user_id,))
        quiz_count = cursor.fetchone()['quiz_count']

        # Get read articles count
        cursor.execute("""
            SELECT COUNT(*) as article_count 
            FROM user_activity 
            WHERE user_id = %s AND activity_type = 'article' AND completed = TRUE
        """, (user_id,))
        article_count = cursor.fetchone()['article_count']

        # Fixed hygiene score at 85%
        hygiene_score = 85

        cursor.close()
        conn.close()

        return jsonify({
            'quiz_count': quiz_count,
            'article_count': article_count,
            'hygiene_score': hygiene_score
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user/activity', methods=['POST'])
@login_required
def track_user_activity():
    try:
        data = request.get_json()
        activity_type = data.get('type')
        activity_id = data.get('id')
        completed = data.get('completed', True)

        if not activity_type or not activity_id:
            return jsonify({'error': 'Missing required fields'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        user_id = verify_token(request.cookies.get('token'))['user_id']

        cursor.execute("""
            INSERT INTO user_activity (user_id, activity_type, activity_id, completed)
            VALUES (%s, %s, %s, %s)
        """, (user_id, activity_type, activity_id, completed))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notifications')
@login_required
def get_notifications():
    notifications = [
        {
            'type': 'new',
            'icon': 'fa-file-alt',
            'title': 'New Case Study Added',
            'message': 'A new case study on "Recent Banking Trojan Attacks" has been added. Check it out!',
            'link': url_for('case_studies_page'),
            'link_text': 'View Case Study →',
            'time': '2 hours ago'
        },
        {
            'type': 'alert',
            'icon': 'fa-exclamation-triangle',
            'title': 'Urgent Security Alert',
            'message': 'New phishing campaign targeting banking customers detected. Learn how to stay safe.',
            'link': url_for('articles_page'),
            'link_text': 'Read Advisory →',
            'time': '5 hours ago'
        },
        {
            'type': 'info',
            'icon': 'fa-play-circle',
            'title': 'New Video Tutorial',
            'message': 'Watch our latest video on "Protecting Against Social Engineering Attacks"',
            'link': url_for('videos_page'),
            'link_text': 'Watch Video →',
            'time': '1 day ago'
        },
        {
            'type': 'info',
            'icon': 'fa-book',
            'title': 'Article Recommendation',
            'message': 'Based on your interests: "Top 10 Cybersecurity Best Practices for Remote Work"',
            'link': url_for('articles_page'),
            'link_text': 'Read Article →',
            'time': '2 days ago'
        }
    ]
    return jsonify(notifications)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        # Make sure to stop the video updater when the app exits
        video_updater.stop()
