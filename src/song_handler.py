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