"""
Ayman Momin
UCID: 30192494
Assignment 1
CPSC 441
"""

import socket
import threading
import logging
from collections import Counter

# Set up logging
logging.basicConfig(filename='server_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Server configuration
HOST = 'localhost'
PORT = 12345
SHIFT_KEY = 3 # For encryption

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

def is_palindrome(input_string):
    """Check if the given string is a palindrome."""
    return input_string == input_string[::-1]

def can_form_palindrome(input_string):
    """
    Check if the string can be rearranged into a palindrome.
    Also calculates the complexity score (number of swaps required).
    """
    char_count = Counter(input_string)
    odd_count = sum(1 for count in char_count.values() if count % 2 != 0)
    
    if odd_count > 1:
        return False, 0  # Cannot form a palindrome
    
    s = list(input_string)
    swaps = 0
    left, right = 0, len(s) - 1
    odd_pos = -1  # Track the position of the odd character
    
    while left < right:
        if s[left] == s[right]:
            left += 1
            right -= 1
        else:
            # Find the rightmost character that matches s[left]
            mid = right
            while mid > left and s[mid] != s[left]:
                mid -= 1
            
            if mid == left:
                # No matching character found (odd character)
                odd_pos = left
                left += 1
            else:
                # Direct swap to the correct position (count as 1 swap)
                s[mid], s[right] = s[right], s[mid]
                swaps += 1
                left += 1
                right -= 1
    
    # Move the odd character to the center if needed (count as 1 swap)
    if odd_pos != -1:
        center = len(s) // 2
        if s[center] != s[odd_pos]:
            swaps += 1  # One swap to move the odd character to the center
    
    return True, swaps

def process_request(request_data):
    """Process the client's request and generate a response."""
    try:
        check_type, input_string = request_data.split('|')
        input_string = ''.join(e for e in input_string if e.isalnum()).lower()
        
        if check_type == 'simple':
             return f"Is palindrome: {is_palindrome(input_string)}"
        elif check_type == 'complex':
            result, swaps = can_form_palindrome(input_string)
            return f"Can form palindrome: {result}, Complexity score: {swaps}"
        else:
            return "Invalid check type."
    except Exception as e:
        return f"Error processing request: {e}"
    
def handle_client(client_socket, client_address):
    """Handle incoming client requests."""
    logging.info(f"Connection from {client_address}")
    
    try:
        while True:
            encrypted_request = client_socket.recv(1024).decode()
            request_data = caesar_decrypt(encrypted_request, SHIFT_KEY)
            if not request_data:
                break

            logging.info(f"Received request: {request_data}")
            response = process_request(request_data)
            encrypted_response = caesar_encrypt(response, SHIFT_KEY)
            client_socket.send(encrypted_response.encode())
            logging.info(f"Sent response: {response}")
    except Exception as e:
        logging.error(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()
        logging.info(f"Closed connection with {client_address}")

def start_server():
    """Start the server and listen for incoming connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        logging.info(f"Server started and listening on {HOST}:{PORT}")
        
        while True:
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=handle_client, args=(client_socket, client_address)).start()

if __name__ == '__main__':
    start_server()