import os
from ytmusicapi import YTMusic
from .header_handler import setup_new_auth

def setup_headers():
    """Setup headers authentication if not already done"""
    headers_path = 'config/headers_auth.json'
    if not os.path.exists(headers_path):
        print("The headers_auth.json file is missing. Let's create it.")
        if not setup_new_auth():
            raise FileNotFoundError("Failed to create headers_auth.json")
    return headers_path

def check_auth(ytmusic):
    """Check if authentication is valid"""
    try:
        ytmusic.get_library_songs(limit=1)
        return True
    except Exception as e:
        if "401" in str(e):
            print("Authentication headers have expired. Please generate new ones.")
            if setup_new_auth():
                return True
        else:
            print(f"Unknown error: {e}")
        return False