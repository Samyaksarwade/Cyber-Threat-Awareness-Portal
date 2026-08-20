import requests
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('youtube_api')

# This is a simple implementation using YouTube Data API v3
# In a production environment, you should handle API keys more securely
# and implement proper caching and error handling

class YouTubeAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
    def get_videos_from_playlist(self, playlist_id, max_results=10):
        """Fetch videos from a specific playlist"""
        logger.info(f"Fetching videos from playlist: {playlist_id}")
        url = f"{self.base_url}/playlistItems"
        params = {
            "part": "snippet,contentDetails",
            "maxResults": max_results,
            "playlistId": playlist_id,
            "key": self.api_key
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            videos = []
            
            for item in data.get("items", []):
                snippet = item.get("snippet", {})
                content_details = item.get("contentDetails", {})
                
                # Extract the video information
                video_id = content_details.get("videoId")
                title = snippet.get("title")
                description = snippet.get("description")
                thumbnail = snippet.get("thumbnails", {}).get("high", {}).get("url")
                published_at = snippet.get("publishedAt")
                
                # Format the date
                if published_at:
                    try:
                        published_date = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
                        formatted_date = published_date.strftime("%Y-%m-%d")
                    except:
                        formatted_date = published_at
                else:
                    formatted_date = "Unknown"
                
                videos.append({
                    "id": video_id,
                    "title": title,
                    "description": description,
                    "thumbnail": thumbnail,
                    "date_added": formatted_date
                })
            
            logger.info(f"Successfully fetched {len(videos)} videos from playlist: {playlist_id}")
            return videos
        else:
            logger.error(f"Error fetching videos from playlist {playlist_id}: HTTP {response.status_code}")
            logger.error(f"Response: {response.text}")
            return []
    
    def get_videos_from_channel(self, channel_id, max_results=10):
        """Fetch videos from a specific channel"""
        logger.info(f"Fetching videos from channel: {channel_id}")
        # First, get the uploads playlist ID for the channel
        url = f"{self.base_url}/channels"
        params = {
            "part": "contentDetails",
            "id": channel_id,
            "key": self.api_key
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if not data.get("items"):
                logger.warning(f"No items found for channel: {channel_id}")
                return []
                
            # Get the uploads playlist ID
            uploads_playlist_id = data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            logger.info(f"Found uploads playlist ID for channel {channel_id}: {uploads_playlist_id}")
            
            # Now fetch videos from this playlist
            return self.get_videos_from_playlist(uploads_playlist_id, max_results)
        else:
            logger.error(f"Error fetching channel {channel_id}: HTTP {response.status_code}")
            logger.error(f"Response: {response.text}")
            return []
    
    def search_videos(self, query, max_results=10):
        """Search for videos with a specific query"""
        logger.info(f"Searching for videos with query: {query}")
        url = f"{self.base_url}/search"
        params = {
            "part": "snippet",
            "maxResults": max_results,
            "q": query,
            "type": "video",
            "key": self.api_key
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            videos = []
            
            for item in data.get("items", []):
                snippet = item.get("snippet", {})
                
                # Extract the video information
                video_id = item.get("id", {}).get("videoId")
                title = snippet.get("title")
                description = snippet.get("description")
                thumbnail = snippet.get("thumbnails", {}).get("high", {}).get("url")
                published_at = snippet.get("publishedAt")
                
                # Format the date
                if published_at:
                    try:
                        published_date = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
                        formatted_date = published_date.strftime("%Y-%m-%d")
                    except:
                        formatted_date = published_at
                else:
                    formatted_date = "Unknown"
                
                videos.append({
                    "id": video_id,
                    "title": title,
                    "description": description,
                    "thumbnail": thumbnail,
                    "date_added": formatted_date
                })
            
            logger.info(f"Successfully fetched {len(videos)} videos for query: {query}")
            return videos
        else:
            logger.error(f"Error searching videos with query {query}: HTTP {response.status_code}")
            logger.error(f"Response: {response.text}")
            return []
