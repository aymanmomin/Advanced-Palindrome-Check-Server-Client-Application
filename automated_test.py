import socket
import threading
import time
import unittest
import server
import client

class TestPalindromeServerClient(unittest.TestCase):
    server_thread = None
    server_socket = None

    @classmethod
    def setUpClass(cls):
        """Start server once before all tests"""
        cls.start_server()

    @classmethod
    def start_server(cls):
        cls.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        cls.server_socket.bind((client.SERVER_HOST, client.SERVER_PORT))
        cls.server_socket.listen(5)
        
        cls.server_thread = threading.Thread(target=server.start_server)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(2)  # Allow server to bind

    @classmethod
    def tearDownClass(cls):
        """Clean up resources"""
        if cls.server_socket:
            cls.server_socket.close()
        time.sleep(1)

    def setUp(self):
        """Ensure server is running before each test"""
        if not self.is_server_running():
            self.__class__.start_server()
            time.sleep(1)

    def is_server_running(self):
        """Check if server port is open"""
        try:
            test_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_sock.connect((client.SERVER_HOST, client.SERVER_PORT))
            test_sock.close()
            return True
        except:
            return False

    def test_simple_palindrome_valid(self):
        response = client.send_request('simple', 'A man, a plan, a canal, Panama')
        self.assertEqual(response, "Is palindrome: True")

    def test_simple_palindrome_invalid(self):
        response = client.send_request('simple', 'Hello')
        self.assertEqual(response, "Is palindrome: False")

    def test_complex_palindrome_valid(self):
        response = client.send_request('complex', 'ivicc')
        self.assertEqual(response, "Can form palindrome: True, Complexity score: 2")

    def test_complex_palindrome_invalid(self):
        response = client.send_request('complex', 'abc')
        self.assertEqual(response, "Can form palindrome: False, Complexity score: 0")

    def test_timeout_retry_mechanism(self):
        """Test timeout by simulating server downtime"""
        # Gracefully stop server
        self.__class__.server_socket.close()
        time.sleep(1)
        
        # Run test
        response = client.send_request('simple', 'test')
        self.assertIn("Error", response)
        
        # Restart server for subsequent tests
        self.__class__.start_server()
        time.sleep(1)

if __name__ == '__main__':
    unittest.main()