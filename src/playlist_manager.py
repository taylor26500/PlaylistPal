from ytmusicapi import YTMusic
from .header_handler import setup_new_auth

def create_playlist(ytmusic, playlist_name, playlist_description, video_ids):
    """Create a new playlist with the found songs"""
    print("\nRefreshing authentication before creating playlist...")
    
    # Refresh authentication
    if setup_new_auth():
        # Reinitialize YTMusic with new headers
        ytmusic = YTMusic('headers_auth.json')
        
        print("\nCreating a new playlist...")
        try:
            playlist_id = ytmusic.create_playlist(playlist_name, playlist_description, video_ids=video_ids)
            print(f"Playlist '{playlist_name}' created successfully!")
            print(f"Playlist ID: {playlist_id}")
            return playlist_id
        except Exception as e:
            print(f"Error creating playlist: {e}")
            return None
    else:
        print("Failed to refresh authentication.")
        return None