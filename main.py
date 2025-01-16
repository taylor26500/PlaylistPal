from src.auth_manager import setup_headers, check_auth
from src.header_handler import reset_headers_file
from src.playlist_manager import create_playlist
from src.song_handler import read_song_list, search_songs
from ytmusicapi import YTMusic

def main():
    try:
        # Initialize
        reset_headers_file()
        headers_path = setup_headers()
        ytmusic = YTMusic(headers_path)
        
        # Check authentication
        if not check_auth(ytmusic):
            print("Authentication failed. Please try running the script again.")
            return

        print("Authentication successful!")

        # Get input file and read songs
        input_file = input("\nEnter the name of your input file (default: music_list.txt): ").strip() or "music_list.txt"
        song_list = read_song_list(input_file)
        
        if not song_list:
            print("No songs were loaded. Please check your input file.")
            return

        print(f"Loaded {len(song_list)} songs from file")

        # Search songs
        video_ids = search_songs(ytmusic, song_list)

        if video_ids:
            # Get playlist details
            playlist_name = input("\nEnter playlist name (default: My Music Collection): ").strip() or "My Music Collection"
            playlist_description = input("Enter playlist description (optional): ").strip() or "Playlist created using ytmusicapi"

            print("\nBefore creating the playlist, you'll need to refresh the authentication.")
            print("Please paste the new headers when prompted.")
            
            # Create playlist
            playlist_id = create_playlist(ytmusic, playlist_name, playlist_description, video_ids)
            if playlist_id:
                print(f"\nSuccess! You can view your playlist at:")
                print(f"https://music.youtube.com/playlist?list={playlist_id}")
        else:
            print("\nNo songs were found to add to the playlist.")
            
    finally:
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