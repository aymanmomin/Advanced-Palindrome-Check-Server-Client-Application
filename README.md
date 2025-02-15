# Advanced Palindrome Check Server-Client Application
## About
This application is a server-client system that checks for palindromes. The server handles two types of checks: 
1. **Simple Palindrome Check**: Determines if a string is a palindrome (ignoring case, spaces, and special characters).
2. **Complex Palindrome Check**: Determines if a string can be rearranged into a palindrome and calculates the minimum number of swaps required.

## Info
Ayman Momin<br>
UCID: 30192494

## Disclaimer
You may come across some codes snippets that aren't related to the problem, they were implemented for testing automation but doesn't affect the actual functionality or manual testing.


## Features
- **Server**:  
  - TCP socket-based communication.  
  - Multithreaded to handle multiple clients.  
  - Logs client requests/responses to `server_log.txt`.  
- **Client**:  
  - Menu-driven interface for simple/complex checks.  
  - Timeout handling with 3 retries.  

## Installation
1. **Prerequisites**:  
   - Python 3.6 or later.  
   - No external libraries required (uses built-in modules: `socket`, `threading`, `logging`).  

2. **Download Code**:  
   - `server.py`: Server code.  
   - `client.py`: Client code.  

## Usage
1. **Start the Server**:  
    ```bash
        python server.py
    ```
   - The server starts on `localhost:12345` and logs activity to `server_log.txt`.
  
2. **Run the Client**:
    ``` bash
    python client.py
    ```
    - Follow the menu to select checks. Example:
    ``` bash
   Menu:
   1. Simple Palindrome Check
   2. Complex Palindrome Check
   3. Exit
   Enter choice (1/2/3): 2
   Enter a string: ivicc
    ```
3. **WireShark tracking**
    - To check the optional implementation
    - Open WireShark
    - Filter `tcp.port == 12345`
    - Follow step 1 and 2

## Example Inputs and Outputs
**Simple Check**

Input: "A man, a plan, a canal, Panama" <br>Output: Is palindrome: True

**Complex Check**
Input: "ivicc" <br>Output: Can form palindrome: True, Complexity score: 2

Input: "aabb"<br>Output: Can form palindrome: True, Complexity score: 1

## Logging (Server)
Log File: server_log.txt

- Logged Data:
- Client IP address.
- Request type (simple/complex).
- Input string.
- Result (true/false) and complexity score.

Example Log Entry:
```bash
2023-10-10 12:00:00 - Connection from ('127.0.0.1', 54321)
2023-10-10 12:00:05 - Received request: complex|ivicc
2023-10-10 12:00:05 - Sent response: Can form palindrome: True, Complexity score: 2
```

## Extra Credit (Optional)
Basic Encryption: Implemented basic encryption for data transmitted between the server and client using caesar cipher.

## Referred Links
- https://www.baeldung.com/cs/palindrome-count-minimum-swap
- https://www.geeksforgeeks.org/count-minimum-swap-to-make-string-palindrome/