# Cyber Security Awareness Portal

A comprehensive web application for cyber security awareness and education.

## Project Structure
```
/Project
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── dashboard.css
│   ├── js/
│   │   ├── main.js
│   │   └── dashboard.js
│   └── images/
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── server/
│   ├── app.py
│   ├── database.py
│   └── config.py
└── database/
    └── schema.sql
```

## Setup Instructions
1. Install required Python packages:
   ```
   pip install flask mysql-connector-python flask-cors
   ```

2. Set up MySQL database using schema.sql

3. Run the application:
   ```
   python server/app.py
   ```

4. Access the application at http://localhost:5000
