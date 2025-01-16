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