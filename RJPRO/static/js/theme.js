/**
 * Theme management for RJPRO application
 * Handles dark mode toggle and persistence across pages
 */

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeTheme();
    setupThemeToggle();
});

/**
 * Initialize theme based on saved preference
 */
function initializeTheme() {
    // Check for saved theme preference
    const darkMode = localStorage.getItem('darkMode') === 'true';
    
    // Apply theme to body
    if (darkMode) {
        document.body.classList.add('dark-mode');
        
        // Update toggle if it exists
        const darkModeToggle = document.getElementById('darkModeToggle');
        if (darkModeToggle) {
            darkModeToggle.checked = true;
        }
    }
}

/**
 * Setup event listener for theme toggle
 */
function setupThemeToggle() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('change', function() {
            toggleDarkMode(this.checked);
        });
    }
}

/**
 * Toggle dark mode on/off
 * @param {boolean} enable - Whether to enable dark mode
 */
function toggleDarkMode(enable) {
    if (enable) {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.remove('dark-mode');
    }
    
    // Save preference to localStorage
    localStorage.setItem('darkMode', enable);
}
