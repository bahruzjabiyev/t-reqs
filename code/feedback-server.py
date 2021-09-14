import socket
import threading
import re
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 8080))
s.listen()

def get_body(data):
    body = b'None'
    body_length = -1

    try:
        parts = data.split(b'\r\n\r\n')
        if parts:
            if len(parts) > 1:
                body = b'\r\n\r\n'.join(parts[1:])
                body_length = len(body)

                # Alternatively, a single type of character ('B' in this case) can 
                # be counted assuming that the body of received requests contains 
                # just that character. This would be useful in cases where the format 
                # of the body in received requests alternates between chunked and regular.


                # body_length = len(re.findall(b'(?<=B)B', body))
                # if body_length != 0:
                #     body_length += 1
            else:
                body = b''
                body_length = 0

    except Exception as exception:
        print(data)
        print("exception: {}".format(exception))

    return body, body_length

def handle_connection(conn):
    data = b''
    try:
        conn.settimeout(3)
        while True:
            try:
                conn_data = conn.recv(2048)
                if not conn_data:
                    break
                else:
                    data += conn_data
            except socket.timeout:
                break

        if b"debug=true" in data:
            body = data
            body_length = len(data)
        else:
            body, body_length = get_body(data)
    
        response_body = b"{body: '" + body + b"', body_length: " + str(body_length).encode() + b"}"
    
        response_headers = b"HTTP/1.1 200 OK\r\nConnection: close\r\nserver-name: someserver\r\nContent-Length: " + str(len(response_body)).encode() + b"\r\n\r\n"
        conn.sendall(response_headers + response_body)
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
    except Exception as exception:
        print(data)
        print("exception: {}".format(exception))

while True:
    try:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_connection, args=(conn,))
        thread.start()
    except Exception as exception:
        print("exception: {}".format(exception))
    
s.close()
