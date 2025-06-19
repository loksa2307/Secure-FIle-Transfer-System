import socket
import ssl

# Step 1: SSL context (no certificate verification)
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# Step 2: Connect to server
with socket.create_connection(('localhost', 4443)) as sock:
    with context.wrap_socket(sock, server_hostname='localhost') as ssock:
        print("🔐 Connected securely.")

        # Step 3: Send authentication
        ssock.send(b"admin:letmein123")
        response = ssock.recv(1024)
        if response != b"AUTH_OK":
            print("❌ Authentication failed.")
            exit()
        print("✅ Authenticated.")

        # Step 4: Send file
        try:
            with open("file_to_send.txt", "rb") as f:
                ssock.sendall(f.read())
                print("📤 File sent successfully.")
        except FileNotFoundError:
            print("❌ file_to_send.txt not found.")
