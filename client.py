"""
Ayman Momin
UCID: 30192494
Assignment 1
CPSC 441
"""

import socket
import time

# Server configuration
SERVER_HOST = 'localhost'
SERVER_PORT = 12345
SHIFT_KEY = 3 # Caesar cipher shift value same as the server

def caesar_encrypt(text, shift):
    """Encrypt text using Caesar cipher (handles all printable ASCII characters)."""
    encrypted = []
    for char in text:
        if 32 <= ord(char) <= 126: # Check if char is printable ASCII
            encrypted.append(chr((ord(char) - 32 + shift) % 95 + 32))
        else:
            encrypted.append(char)
    return ''.join(encrypted)

def caesar_decrypt(text, shift):
    """Decrypt text using Caesar cipher (handles all printable ASCII characters)."""
    return caesar_encrypt(text, -shift)

def connect_to_server():
    """Connect to the server with a 5-second timeout."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5)
    try:
        client.connect((SERVER_HOST, SERVER_PORT))
        return client
    except socket.timeout:
        print("Connection timed out. Retrying...")
        return None
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return None

def send_request(check_type, input_string):
    """Send request with robust error handling"""
    for _ in range(3):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                s.connect((SERVER_HOST, SERVER_PORT))
                
                # Encrypt and send request
                request = f"{check_type}|{input_string}"
                encrypted_request = caesar_encrypt(request, SHIFT_KEY)
                s.send(encrypted_request.encode())
                
                # Receive and decrypt response
                encrypted_response = s.recv(1024).decode()
                response = caesar_decrypt(encrypted_response, SHIFT_KEY)
                return response

        except socket.timeout:
            if _ == 2:
                return "Error: Connection timed out"
        except ConnectionRefusedError:
            if _ == 2:
                return "Error: Server unavailable"
        except Exception as e:
            if _ == 2:
                return f"Error: {str(e)}"
        time.sleep(0.5)
    return "Error: Connection failed after 3 attempts"


def main():
    """Main function to run the client."""
    while True:
        print("\nMenu:")
        print("1. Simple Palindrome Check")
        print("2. Complex Palindrome Check")
        print("3. Exit")
        choice = input("Enter choice (1/2/3): ").strip()
        
        if choice in ('1', '2'):
            input_string = input("Enter a string: ")
            check_type = 'simple' if choice == '1' else 'complex'
            print(send_request(check_type, input_string))
        elif choice == '3':
            print("Exiting the client...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()