document.addEventListener('DOMContentLoaded', () => {
    loadProfileData();
    setupEventListeners();
});

async function loadProfileData() {
    try {
        const response = await fetch('/api/profile', {
            headers: {
                'Authorization': `Bearer ${getCookie('token')}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('profileUsername').textContent = data.username;
            document.getElementById('profileEmail').textContent = data.email;
            document.getElementById('profileJoinDate').textContent = new Date(data.joinDate).toLocaleDateString();
        } else {
            window.location.href = '/login';
        }
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

function setupEventListeners() {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            try {
                const response = await fetch('/api/logout', {
                    method: 'POST'
                });
                if (response.ok) {
                    localStorage.removeItem('token');
                    window.location.href = '/login';
                }
            } catch (error) {
                console.error('Error during logout:', error);
            }
        });
    }
}
