# Mengimpor modul socket untuk berkomunikasi melalui jaringan
import socket
# Mengimpor modul os untuk memeriksa keberadaan file
import os

# 1. Implementasi pembuatan TCP socket dan mengaitkannya ke alamat dan port tertentu (poin: 20) 

# Menentukan alamat host dan nomor port yang akan digunakan server
HOST = 'localhost'
PORT = 80

# Membuat server socket
# Parameter AF_INET menunjukkan bahwa jaringan yang mendasarinya menggunakan IPv4
# Parameter SOCK_STREAM menunjukkan bahwa soket bertipe SOCK_STREAM yang berarti soket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Mengikat alamat host dan nomor port ke server socket
server_socket.bind((HOST, PORT))

# Server mendengarkan permintaan koneksi TCP dari klien
server_socket.listen()

print(f"Server is running on {HOST}:{PORT}...")

# 2. Program web server dapat menerima dan memparsing HTTP request yang dikirimkan oleh browser (poin: 20) 

# Fungsi handle_request untuk menangani permintaan yang masuk
def handle_request(conn, addr): 
    print(f"Connection established from {addr}")
    
    # Menerima request dari klien dan menyimpannya ke variabel request_data
    request_data = conn.recv(1024)

    # Memisahkan request menjadi baris-baris dan menyimpannya ke variabel request_lines
    request_lines = request_data.split(b"\r\n")
    
    # Memisahkan baris pertama request, menambahkan spasi sebagai pemisah, dan menyimpannya ke variabel request_part
    request_parts = request_lines[0].split(b" ")

    # Mendapatkan metode request
    request_method = request_parts[0].decode("utf-8")

    # Mendapatkan path file yang diminta dari request_parts
    file_path = request_parts[1].decode("utf-8")
    
    # Menentukan halaman utama default
    if file_path == "/":
        file_path = "/index.html"
    
    # 3. Web server dapat mencari dan mengambil file (dari file system) yang diminta oleh client (poin: 15) 

    # Menambahkan titik di depan file_path sehingga path menjadi valid
    file_path = f".{file_path}"

    # Memeriksa apakah file yang diminta ada di sistem
    if os.path.isfile(file_path):
        # Memisahkan ekstensi file dan menyimpannya ke variabel file_extension
        _, file_extension = os.path.splitext(file_path)
        
        # Menentukan content type berdasarkan ektensi file dan menyimpannya ke variabel content_type
        if file_extension == ".html":
            content_type = "text/html"
        elif file_extension == ".css":
            content_type = "text/css"
        elif file_extension == ".js":
            content_type = "application/javascript"
        elif file_extension in [".jpg", ".jpeg", ".png", ".gif"]:
            content_type = f"image/{file_extension[1:]}"
        elif file_extension == ".txt":
            content_type = "text/plain"
        else:
            content_type = "application/octet-stream"
        
        # Membuka file, membaca seluruh isi file, dan menyimpannya ke variabel file_content
        with open(file_path, "rb") as f:
            file_content = f.read()

        '''
        4. Web server dapat membuat HTTP response message yang terdiri dari header dan konten file yang diminta (poin: 20)

        5. Web server dapat mengirimkan response message yang sudah dibuat ke browser (client) 
        dan dapat ditampilkan dengan benar di sisi client (poin: 15)
        '''

        # Membuat header respons HTTP berhasil yang berisi status kode (200 OK), tipe konten, dan panjang konten
        response_header = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(file_content)}\r\n\r\n"
        response_header = response_header.encode("utf-8")
        
        # Mengirimkan header dan konten file ke klien menggunakan soket conn
        conn.sendall(response_header)
        conn.sendall(file_content)
    
    # Jika file yang diminta tidak ada di sistem
    else:
        '''
        6. Jika file yang diminta oleh client tidak tersedia, web server dapat mengirimkan pesan “404 Not Found”
        dan dapat ditampilkan dengan benar di sisi client. (poin: 10)
        '''
        
        # Membuat header respons HTTP gagal yang berisi status kode (404 Not Found) dan panjang konten
        response_header = "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n"
        response_header = response_header.encode("utf-8")
        
        # Mengirimkan header ke klien menggunakan soket conn
        conn.sendall(response_header)
    
    # Menutup koneksi dengan klien
    conn.close()
    print(f"Connection from {addr} closed")

while True:
    # Memanggil metode accept untuk server socket dan membuat soket baru di server dengan nama conn
    # Variable addr menyimpan IP klien dan nomor port klien
    conn, addr = server_socket.accept()

    # Memanggil fungsi handle_request dengan parameter conn dan addr
    handle_request(conn, addr)