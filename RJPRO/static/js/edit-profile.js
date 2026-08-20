document.addEventListener('DOMContentLoaded', () => {
    loadProfileData();
    setupFormSubmission();
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
            document.getElementById('username').value = data.username;
            document.getElementById('email').value = data.email;
        } else {
            window.location.href = '/login';
        }
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

function setupFormSubmission() {
    const form = document.getElementById('editProfileForm');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        clearErrors();

        const formData = {
            username: document.getElementById('username').value,
            email: document.getElementById('email').value,
            currentPassword: document.getElementById('currentPassword').value,
            newPassword: document.getElementById('newPassword').value,
            confirmPassword: document.getElementById('confirmPassword').value
        };

        if (formData.newPassword && formData.newPassword !== formData.confirmPassword) {
            showError('confirmPassword', 'Passwords do not match');
            return;
        }

        try {
            const response = await fetch('/api/profile/update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getCookie('token')}`
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                window.location.href = '/profile';
            } else {
                if (data.errors) {
                    Object.keys(data.errors).forEach(key => {
                        showError(key, data.errors[key]);
                    });
                }
            }
        } catch (error) {
            console.error('Error updating profile:', error);
        }
    });
}

function showError(field, message) {
    const errorElement = document.getElementById(`${field}Error`);
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
}

function clearErrors() {
    const errorElements = document.querySelectorAll('.error-message');
    errorElements.forEach(element => {
        element.textContent = '';
        element.style.display = 'none';
    });
}
