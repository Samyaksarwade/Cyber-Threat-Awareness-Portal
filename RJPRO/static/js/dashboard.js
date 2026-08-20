document.addEventListener('DOMContentLoaded', () => {
    // Check if user is logged in
    const token = getCookie('token');
    if (!token) {
        window.location.href = '/login';
        return;
    }

    // Initialize components
    loadUserProfile();
    loadUserStats();
    loadSecurityTips();
    setupEventListeners();
    displayCurrentDate();

    // Refresh stats periodically
    setInterval(() => {
        loadUserStats();
    }, 60000); // Refresh every minute
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function loadUserProfile() {
    try {
        const response = await fetch('http://localhost:5000/api/profile', {
            headers: {
                'Authorization': `Bearer ${getCookie('token')}`
            }
        });
        
        if (response.ok) {
            const userData = await response.json();
            document.getElementById('userName').textContent = userData.username;
        }
    } catch (error) {
        console.error('Error loading user profile:', error);
    }
}

async function loadUserStats() {
    try {
        const response = await fetch('/api/user/stats', {
            credentials: 'same-origin'  // This will send the cookies
        });
        
        if (response.ok) {
            const stats = await response.json();
            updateDashboardStats(stats);
        }
    } catch (error) {
        console.error('Error loading user stats:', error);
    }
}

function updateDashboardStats(stats) {
    if (stats) {
        document.getElementById('hygieneScore').textContent = '85%';  // Fixed at 85%
        document.getElementById('quizCount').textContent = stats.quiz_count || '-';
        document.getElementById('articleCount').textContent = stats.article_count || '-';
    }
}

function initializeThreatMap() {
    // Placeholder for threat map initialization
    const mapContainer = document.getElementById('threatMap');
    // Add your threat map implementation here
}

async function loadSecurityTips() {
    const tipsContainer = document.getElementById('securityTips');
    const securityTips = [
        {
            title: "Strong Password Practices",
            tip: "Use a combination of letters, numbers, and special characters. Never reuse passwords across accounts.",
            icon: "fa-key"
        },
        {
            title: "Two-Factor Authentication",
            tip: "Enable 2FA wherever possible to add an extra layer of security to your accounts.",
            icon: "fa-lock"
        },
        {
            title: "Phishing Awareness",
            tip: "Be cautious of unexpected emails. Never click suspicious links or download attachments from unknown sources.",
            icon: "fa-envelope"
        },
        {
            title: "Regular Updates",
            tip: "Keep your software and systems updated to protect against known vulnerabilities.",
            icon: "fa-sync"
        }
    ];

    tipsContainer.innerHTML = securityTips.map(tip => `
        <div class="tip-item">
            <i class="fas ${tip.icon}"></i>
            <h3>${tip.title}</h3>
            <p>${tip.tip}</p>
        </div>
    `).join('');
}

async function loadNotifications() {
    const notificationsList = document.getElementById('notificationsList');
    try {
        const response = await fetch('/api/notifications', {
            credentials: 'same-origin'  // This will send the cookies
        });
        
        if (response.ok) {
            const notifications = await response.json();
            notificationsList.innerHTML = notifications.map(notification => `
                <div class="notification-item ${notification.type}">
                    <div class="notification-title">
                        <i class="fas ${notification.icon}"></i>
                        ${notification.title}
                    </div>
                    <p>${notification.message}</p>
                    <a href="${notification.link}" class="notification-link">${notification.link_text}</a>
                    <div class="notification-time">${notification.time}</div>
                </div>
            `).join('');
        } else {
            // Keep the existing static notifications if API call fails
            console.warn('Could not load dynamic notifications, keeping static ones');
        }
    } catch (error) {
        // Keep the existing static notifications if API call fails
        console.warn('Could not load dynamic notifications, keeping static ones:', error);
    }
}

function setupEventListeners() {
    // Profile dropdown toggle
    const userProfile = document.getElementById('userProfile');
    if (userProfile) {
        const profileDropdown = userProfile.parentElement;
        
        userProfile.addEventListener('click', (e) => {
            e.preventDefault();
            profileDropdown.classList.toggle('active');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!profileDropdown.contains(e.target)) {
                profileDropdown.classList.remove('active');
            }
        });
    }

    // Logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            handleLogout();
        });
    }

    // Quick action buttons
    const actionButtons = document.querySelectorAll('.action-btn');
    actionButtons.forEach(button => {
        button.addEventListener('click', () => {
            const action = button.textContent.trim();
            handleQuickAction(action);
        });
    });
}

async function handleLogout() {
    try {
        // Clear cookies
        document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        document.cookie = 'user=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        
        // Redirect to login page
        window.location.href = '/login';
    } catch (error) {
        console.error('Error during logout:', error);
    }
}

function handleQuickAction(action) {
    switch(action) {
        case 'Take a Quiz':
            window.location.href = '/quizzes';
            break;
        case 'Watch Video':
            window.location.href = '/videos';
            break;
        case 'Read Article':
            window.location.href = '/articles';
            break;
    }
}

// Function to display current date
function displayCurrentDate() {
    const dateElement = document.getElementById('currentDate');
    if (dateElement) {
        const now = new Date();
        const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        dateElement.textContent = now.toLocaleDateString('en-US', options);
    }
}

// Track article completion
async function trackArticleRead(articleId) {
    try {
        const response = await fetch('http://localhost:5000/api/user/activity', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getCookie('token')}`
            },
            body: JSON.stringify({
                type: 'article',
                id: articleId,
                completed: true
            })
        });
        
        if (response.ok) {
            // Refresh stats after tracking activity
            loadUserStats();
        }
    } catch (error) {
        console.error('Error tracking article:', error);
    }
}

// Track quiz completion
async function trackQuizCompleted(quizName) {
    try {
        const response = await fetch('http://localhost:5000/api/user/activity', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getCookie('token')}`
            },
            body: JSON.stringify({
                type: 'quiz',
                id: quizName,
                completed: true
            })
        });
        
        if (response.ok) {
            // Refresh stats after tracking activity
            loadUserStats();
        }
    } catch (error) {
        console.error('Error tracking quiz:', error);
    }
}
