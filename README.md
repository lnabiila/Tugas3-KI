| Name                         | NRP        | Kelas       | Pembagian Kerja |
|------------------------------|------------|-------------|-----------------|
| Lathiifah Nabiila Bakhtiar   | 5025221130 | Keamanan Informasi B     | Server, RSA     |
| Athaya Rohadatul Yaqutah     | 5025221235 | Keamanan Informasi B     | Client          |

implementasi komunikasi client-server menggunakan Python yang menggabungkan konsep RSA (Rivest–Shamir–Adleman) dan DES (Data Encryption Standard) untuk melakukan komunikasi yang aman.

## **Tujuan Utama Kode**

1. **Mengamankan komunikasi antara klien dengan server.**
   - RSA digunakan untuk pertukaran kunci DES secara aman.
   - DES digunakan untuk enkripsi dan dekripsi pesan selama sesi komunikasi.

2. **Mendukung komunikasi antar-klien melalui server.**
   - Server bertindak sebagai relay untuk mengarahkan pesan antar-klien.

## **Cara Kerja**

1. **Memulai Server:**
   - Jalankan `server.py`.
   - Server akan mendengarkan koneksi pada `127.0.0.1` port `8888`.

2. **Klien Bergabung:**
   - Jalankan `client.py`.
   - Klien akan:
     - Mengirimkan public key RSA ke server.
     - Menerima daftar klien lain dan public key mereka.
   - Setiap klien memiliki ID unik yang ditampilkan saat bergabung.

3. **Pertukaran Kunci RSA:**
   - Klien melakukan otentikasi dengan saling bertukar nilai `n1` dan `n2` untuk memastikan pengirim sah.
   - Setelah otentikasi, kunci DES didistribusikan melalui RSA.

4. **Komunikasi Aman:**
   - Setelah kunci DES didistribusikan:
     - Pesan yang dikirim antar-klien dienkripsi menggunakan DES.
     - Hanya penerima yang dapat mendekripsi pesan.
    
## **Cara Menjalankan Kode**
### Langkah 1: Jalankan Server
```bash
python server.py
```

### Langkah 2: Jalankan Klien
- Jalankan `client.py` di terminal berbeda.
```bash
python client.py
```
- Ketika diminta, masukkan ID target untuk mengobrol.
- Perlu menjalankan lebih dari satu instance `client.py` agar komunikasi antar-klien dapat diuji.

### Langkah 3: Berkomunikasi
- Gunakan perintah di klien:
  - `'L'` untuk melihat daftar klien.
  - Masukkan ID target untuk memulai komunikasi.
  - Kirim pesan dan lihat pesan terenkripsi serta dekripsinya di terminal.
 
## **Preview**

### Server
![image](https://github.com/user-attachments/assets/7f612e56-1efe-4ce6-9437-bba55f0b1d95)

### Client 1 - Client 2
![image](https://github.com/user-attachments/assets/561e2aef-d916-4c37-9478-a5f00f63f3c8)
