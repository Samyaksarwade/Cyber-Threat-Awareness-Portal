import threading
import time
import os
import json
from datetime import datetime
from youtube_api import YouTubeAPI
from config import YOUTUBE_API_KEY, YOUTUBE_CHANNELS
import logging

# Configure logging
logger = logging.getLogger('video_updater')

class VideoUpdater:
    def __init__(self, update_interval=3600):  # Default update interval: 1 hour
        self.update_interval = update_interval
        self.youtube = YouTubeAPI(YOUTUBE_API_KEY)
        self.running = False
        self.thread = None
        self.cache_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'content', 'videos_cache.json')
        
        # Create content directory if it doesn't exist
        content_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'content')
        if not os.path.exists(content_dir):
            os.makedirs(content_dir)
    
    def start(self):
        """Start the video updater thread"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._update_loop)
            self.thread.daemon = True  # Thread will exit when main program exits
            self.thread.start()
            logger.info(f"Video updater started. Will check for new videos every {self.update_interval} seconds.")
            print(f"Video updater started. Will check for new videos every {self.update_interval} seconds.")
    
    def stop(self):
        """Stop the video updater thread"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
            logger.info("Video updater stopped.")
            print("Video updater stopped.")
    
    def _update_loop(self):
        """Main update loop that runs in a separate thread"""
        while self.running:
            try:
                logger.info("Starting scheduled video update...")
                self.update_videos()
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                logger.info(f"Videos updated at {current_time}")
                print(f"Videos updated at {current_time}")
            except Exception as e:
                logger.error(f"Error updating videos: {str(e)}")
                print(f"Error updating videos: {str(e)}")
            
            # Sleep for the update interval
            logger.info(f"Next update scheduled in {self.update_interval} seconds")
            for _ in range(self.update_interval):
                if not self.running:
                    break
                time.sleep(1)
    
    def update_videos(self):
        """Fetch and cache videos from YouTube"""
        logger.info("Fetching videos from YouTube API...")
        video_categories = []
        
        # Cybersecurity keywords for filtering
        cybersec_keywords = [
            'cyber', 'security', 'hack', 'malware', 'virus', 'phishing', 'ransomware', 
            'encryption', 'firewall', 'vulnerability', 'exploit', 'breach', 'threat', 
            'authentication', 'password', 'privacy', 'infosec', 'pentest', 'penetration testing',
            'ctf', 'capture the flag', 'blue team', 'red team', 'purple team', 'soc', 'incident response',
            'forensics', 'digital forensics', 'dfir', 'osint', 'social engineering', 'zero day',
            'zero-day', '0day', 'buffer overflow', 'sql injection', 'xss', 'csrf', 'ddos',
            'kali', 'metasploit', 'wireshark', 'burp suite', 'nmap', 'cryptography'
        ]
        
        # Fetch videos for each category
        for category_name, channel_ids in YOUTUBE_CHANNELS.items():
            logger.info(f"Processing category: {category_name}")
            videos = []
            
            # Determine if it's a channel ID or playlist ID
            for channel_id in channel_ids:
                if channel_id.startswith('PL'):  # Playlist ID
                    logger.info(f"Fetching videos from playlist: {channel_id}")
                    category_videos = self.youtube.get_videos_from_playlist(channel_id, max_results=15)
                else:  # Channel ID
                    logger.info(f"Fetching videos from channel: {channel_id}")
                    category_videos = self.youtube.get_videos_from_channel(channel_id, max_results=15)
                
                # Filter videos to ensure they're cybersecurity related
                filtered_videos = []
                for video in category_videos:
                    title = video.get('title', '').lower()
                    description = video.get('description', '').lower()
                    content = title + ' ' + description
                    
                    # Check if any cybersecurity keyword is in the title or description
                    if any(keyword.lower() in content for keyword in cybersec_keywords):
                        filtered_videos.append(video)
                    else:
                        logger.info(f"Filtered out non-cybersecurity video: {video.get('title')}")
                
                videos.extend(filtered_videos)
            
            # Sort videos by date (newest first) and limit to 10
            videos = sorted(videos, key=lambda x: x.get('date_added', ''), reverse=True)[:10]
            logger.info(f"Added {len(videos)} cybersecurity videos to category: {category_name}")
            
            # Set appropriate icon for each category
            if category_name == 'Educational Videos':
                icon = 'fas fa-graduation-cap'
            elif category_name == 'Cybersecurity News':
                icon = 'fas fa-newspaper'
            elif category_name == 'Cybersecurity Tutorials':
                icon = 'fas fa-laptop-code'
            elif category_name == 'Cybersecurity Case Studies':
                icon = 'fas fa-search'
            else:
                icon = 'fas fa-shield-alt'
                
            video_categories.append({
                'name': category_name,
                'icon': icon,
                'videos': videos
            })
        
        # Save to cache file
        logger.info(f"Saving {len(video_categories)} categories to cache file: {self.cache_file}")
        with open(self.cache_file, 'w') as f:
            json.dump({'categories': video_categories}, f, indent=2)
        logger.info("Cache file updated successfully")
    
    def get_cached_videos(self):
        """Get videos from cache if available, otherwise fetch from YouTube"""
        if os.path.exists(self.cache_file):
            try:
                logger.info(f"Reading videos from cache file: {self.cache_file}")
                with open(self.cache_file, 'r') as f:
                    cache_data = json.load(f)
                logger.info(f"Successfully loaded {len(cache_data.get('categories', []))} categories from cache")
                return cache_data.get('categories', [])
            except Exception as e:
                logger.error(f"Error reading cache file: {str(e)}")
                print(f"Error reading cache file: {str(e)}")
        
        # If cache doesn't exist or is invalid, update and return fresh data
        logger.info("Cache not available, fetching fresh data from YouTube")
        self.update_videos()
        with open(self.cache_file, 'r') as f:
            cache_data = json.load(f)
        return cache_data.get('categories', [])

# Create a singleton instance
video_updater = VideoUpdater()
