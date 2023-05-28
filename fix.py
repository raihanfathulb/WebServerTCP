
from socket import * #untuk berinteraksi dengan socket dan komunikasi jaringan
import sys #terminasi program (mengakses fungsi-fungsi berkaitan dengan sistem)

def handleRequest(connectionSocket): 
#handle Request yang valid
#untuk memproses permintaan dari klien
   
    #membaca pesan yang diterima didecode dari byte menjadi string 
    message = connectionSocket.recv(1024).decode() 
    
    #Memeriknya pesan yang diterima tidak kosong
    if message != '':
        #memecah pesan menjadi potongan2 berdasarkan delimeter "/"
        #potongan akan menjadi nama file yang diminta oleh klien
        fileName = message.split('/')[1].split()[0]

        #Membuka file dengan nama yang diminta klien dan ditampung
        with open(fileName, 'rb') as f:
            outputFile = f.read() 
        
        #Mengirim respon HTTP dengan kode status 200 OK ke klien melalui CS
        #Respon di kirim dalam bentuk byte (encode)
        connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n'.encode())

        #Isi file telah dibaca dikirim ke klien melalui CS
        connectionSocket.sendall(outputFile)
        #Mengirimkan karakter newline sebagai penanda akhir respon
        connectionSocket.send('\r\n'.encode())
        
        #Mencetak nama file yang diminta klien sebagai informasi
        print(fileName)
       
        #CS ditutup setelah selesai memproses permintaan klien
        connectionSocket.close()

#untuk menangani jika terjadi kesalahan dalam memproses permintaan klien
def deniedRequest(connectionSocket):
        #membuka file html dalam mode baca (read binary) dan membaca isinya
        with open('notfound.html', 'rb') as f:
            outputFile = f.read()

        """Mengirimkan respon HTTP dengan kode status 404 Not Found
           beserta isi file notfound.html ke klien.
           Respon dikirim dalam bentuk byte (encode).
           New line dikirim sebagai penanda akhir respon"""
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
        connectionSocket.sendall(outputFile)
        connectionSocket.send('\r\n'.encode())

        #CS ditutup setelah selesai mengirimkan respons
        connectionSocket.close()

def main(): 
    
    #membuat socket TCP 
    #AF_INET Menunjukan socket digunakan untuk protokol IPv4
    #SOCK_STREAM menunjukan bahwa socket menggunakan TCP
    serverSocket = socket(AF_INET, SOCK_STREAM)

    #Mengikat socket server ke alamat IP dan port tertentu
    serverPort = 8090
    #alamat IP dikosongkan tandanya server menerima koneksi dari semua antarmuka jaringan
    serverSocket.bind(('', serverPort)) 
    
    #mengatur socket server dalam mode mendengarkan dengan jumlah koneksi dpt diterima 1
    serverSocket.listen(1)

    #Memberi pesan ke konsol bahwa server telah siap
    print('Web Server ready to serve clients...')
    
    #looping
    while True:
        #menerima koneksi masuk dari klien (accept())
        #CS: objek socket baru digunakan untuk berkomunikasi engan klien
        #addr: tuple yang berisi alamat IP dan port dari klien yang terhubung
        connectionSocket, addr = serverSocket.accept()
       
        #memproses permintaan dari klien. jika ada kesalahan fungsi denied dipanggil
        try:
            handleRequest(connectionSocket)
        except IOError:
            deniedRequest(connectionSocket)
        
        #mencentak pesan ke konsol bahwa file talh berhasil dikirim
        #format string digunakan dengan format() untuk menggabungkan IP dan Port
        print('Succesfully send file to host {}, with port number {}'.format(addr[0], addr[1]))
    
    #Menutup socket server dan mengakhiri program
    serverSocket.close()
    sys.exit()
    
#memastikan fungsi main hanya akan dijalankan jika skrip ini dieksekusi langsung, bukan sebgaia modul yang diimpor skrip lain 
if __name__ == '__main__':
    main()