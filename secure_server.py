import socket
import ssl

# Step 1: Setup server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 4443))
server_socket.listen(5)
print("🔒 Server is waiting for a connection...")

# Step 2: Wrap with SSL
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

# Step 3: Accept and authenticate
with context.wrap_socket(server_socket, server_side=True) as ssock:
    conn, addr = ssock.accept()
    print(f"🔗 Connection from {addr}")

    creds = conn.recv(1024).decode().strip()
    if creds != "admin:letmein123":
        conn.send(b"AUTH_FAIL")
        print("❌ Authentication failed.")
        conn.close()
    else:
        conn.send(b"AUTH_OK")
        print("✅ Client authenticated.")

        # Step 4: Receive file
        with open("received_file.txt", "wb") as f:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                f.write(data)
        print("📁 File received successfully.")
