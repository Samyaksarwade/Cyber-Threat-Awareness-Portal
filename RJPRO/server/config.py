import os

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'cyber_security_portal'),
    'auth_plugin': os.getenv('DB_AUTH_PLUGIN', 'mysql_native_password')
}

# App configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-development')
JWT_EXPIRATION = 24 * 60 * 60  # 24 hours in seconds

# YouTube API configuration
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', '')

# YouTube Channel and Playlist IDs for different categories
YOUTUBE_CHANNELS = {
    'Educational Videos': [
        'UC0ArlFuFYMpEewyRBzdLHiw',   # The Cyber Mentor
        'UCL4JGzitDkX5TOwzs9A02Kg',   # David Bombal
        'UCVeW9qkBjo3zosnqUbG7CFw'    # John Hammond
    ],
    'Cybersecurity News': [
        'UCJ6q9Ie29ajGqKApbLqfBOg',   # BlackHat
        'UCsgzmECRIFCI_4uGjgpT_wQ',   # Cybersecurity & Infrastructure Security Agency
        'UCnctXOUIeRFu1BR5O0W5e9w'    # SANS Offensive Operations
    ],
    'Cybersecurity Tutorials': [
        'UC0ZTPkdxlAKf-V33tqXwi3Q',   # Hackersploit
        'UC9x0AN7BWHpCDHSm9NiJFJQ',   # NetworkChuck
        'UCkefXKtInZ9PLsoGRtml2FQ'    # The PC Security Channel
    ],
    'Cybersecurity Case Studies': [
        'PL96C35uN7xGLux5q2c4P_IqbKF11-pfsR',   # Cybersecurity Case Studies Playlist
        'PLhixgUqwRTjxglIswKp9mpkfPNfHkzyeN',   # LiveOverflow Security
        'PLW8bTPKFyQglB7I5PwN7OFKrqW8_wQjXX'    # Cybersecurity Incidents Analysis
    ]
}
