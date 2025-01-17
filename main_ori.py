from ytmusicapi import YTMusic
import os
import json

def convert_raw_headers_to_auth(raw_headers, cookie):
    """Convert raw headers text to the required authentication format"""
    headers_dict = {}
    
    current_key = None
    current_value = []
    
    # Split the raw headers into lines
    lines = raw_headers.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if ':' in line:
            # If we have a stored key and value, save it before processing new one
            if current_key and current_value:
                headers_dict[current_key.lower()] = ' '.join(current_value)
            
            # Split at first occurrence of ':' as header values might contain ':'
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # Skip protocol-specific headers (those starting with ':')
            if key.startswith(':'):
                current_key = None
                current_value = []
                continue
            
            current_key = key
            current_value = [value] if value else []
        elif line and current_key:  # Continue previous header value
            current_value.append(line)
    
    # Save the last header if exists
    if current_key and current_value:
        headers_dict[current_key.lower()] = ' '.join(current_value)

    # Create the required headers format
    auth_headers = {
        "accept": headers_dict.get("accept", "*/*"),
        "accept-language": headers_dict.get("accept-language", "en-US,en;q=0.9"),
        "authorization": headers_dict.get("authorization", ""),
        "cookie": cookie.replace("\n", ""),
        "user-agent": headers_dict.get("user-agent", ""),
        "x-goog-authuser": headers_dict.get("x-goog-authuser", "0"),
        "x-origin": headers_dict.get("origin", "https://music.youtube.com")
    }
    
    return auth_headers

def save_headers_to_file(headers, filename='headers_auth.json'):
    """Save headers to a JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(headers, f, indent=4)
        print(f"Headers successfully saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving headers: {e}")
        return False

def reset_headers_file(filename='headers_auth.json'):
    """Reset all header values to empty strings"""
    empty_headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": "",
        "cookie": "",
        "user-agent": "",
        "x-goog-authuser": "0",
        "x-origin": "https://music.youtube.com"
    }
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(empty_headers, f, indent=4)
        print(f"Headers file reset successfully")
    except Exception as e:
        print(f"Error resetting headers file: {e}")

def setup_new_auth():
    """Setup new authentication headers"""
    print("\nPaste your raw headers below and type 'END' on a new line when finished:")
    raw_headers = ""
    
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        raw_headers += line + "\n"
    
    print("\nPaste your cookie below and type 'END' on a new line when finished:")
    cookie = ""

    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        cookie += line + "\n"

    if not raw_headers.strip():
        print("No headers were provided.")
        return False
    
    try:
        headers = convert_raw_headers_to_auth(raw_headers, cookie)
        if save_headers_to_file(headers):
            print("\nAuthentication headers have been saved successfully!")
            return True
    except Exception as e:
        print(f"\nError during setup: {e}")
        return False

def setup_headers():
    """Setup headers authentication if not already done"""
    headers_path = 'headers_auth.json'
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
                # Reinitialize YTMusic with new headers
                return True
        else:
            print(f"Unknown error: {e}")
        return False

def clean_song_name(filename):
    """Clean up the filename to create a better search query"""
    # Remove .mp3 extension
    song = filename.replace('.mp3', '')
    # Remove special characters that might interfere with search
    song = song.replace('［', '[').replace('］', ']')
    return song

def read_song_list(filename):
    """Read songs from a text file"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # Skip 'desktop.ini' and 'Folder.jpg' and empty lines
            songs = [line.strip() for line in file 
                    if line.strip() and 'desktop.ini' not in line 
                    and 'Folder.jpg' not in line]
        return [clean_song_name(song) for song in songs]
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def search_songs(ytmusic, song_list):
    """Search for songs and collect their video IDs"""
    print("\nSearching for songs...")
    video_ids = []
    not_found = []
    
    for i, song in enumerate(song_list, 1):
        print(f"Searching ({i}/{len(song_list)}): {song}")
        try:
            results = ytmusic.search(song, filter="songs", limit=1)
            if results:
                video_id = results[0]['videoId']
                video_ids.append(video_id)
                print(f"Found: {results[0]['title']} by {results[0]['artists'][0]['name']}")
            else:
                print(f"Song not found: {song}")
                not_found.append(song)
        except Exception as e:
            print(f"Error searching for {song}: {e}")
            not_found.append(song)
    
    if not_found:
        print("\nSongs not found:")
        for song in not_found:
            print(f"- {song}")
    
    return video_ids

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

def main():
    # Initialize
    reset_headers_file()
    # Setup headers authentication
    headers_path = setup_headers()
    # Initialize YTMusic with headers
    ytmusic = YTMusic(headers_path)
    
    # Check authentication
    if not check_auth(ytmusic):
        print("Authentication failed. Please try running the script again.")
        return
    print("Authentication successful!")

    # Get input file name
    input_file = input("\nEnter the name of your input file (default: music_list.txt): ").strip() or "music_list.txt"
    song_list = read_song_list(input_file)

    if not song_list:
        print("No songs were loaded. Please check your input file.")
        return

    print(f"Loaded {len(song_list)} songs from file")

    # Search for songs and collect their video IDs
    video_ids = search_songs(ytmusic, song_list)

    if video_ids:
        # Get playlist details from user
        playlist_name = input("\nEnter playlist name (default: My Music Collection): ").strip() or "My Music Collection"
        playlist_description = input("Enter playlist description (optional): ").strip() or "Playlist created using ytmusicapi"

        print("\nBefore creating the playlist, you'll need to refresh the authentication.")
        print("Please paste the new headers when prompted.")
        
        # Create the playlist with fresh authentication
        playlist_id = create_playlist(ytmusic, playlist_name, playlist_description, video_ids)
        if playlist_id:
            print(f"\nSuccess! You can view your playlist at:")
            print(f"https://music.youtube.com/playlist?list={playlist_id}")
    else:
        print("\nNo songs were found to add to the playlist.")
    reset_headers_file()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        print("\nProgram finished.")