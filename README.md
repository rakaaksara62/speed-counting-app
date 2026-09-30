# PRISMA Kalkulator Tangan - Streamlit

## Menjalankan di komputer

```bash
pip install -r requirements.txt
streamlit run app.py
```

Lalu buka alamat yang diberikan Streamlit, biasanya:
`http://localhost:8501`

## Fitur

- Waktu per soal dapat diatur, misalnya 5 detik.
- Soal otomatis berganti setelah waktu habis.
- Jumlah soal 10-200.
- Mode Campuran, Horizontal saja, atau Vertikal saja.
- Soal diacak setiap sesi.
- Bentuk soal dibuat mengikuti pola pada kisi-kisi PRISMA Kategori II.
- Jawaban dapat dimasukkan saat latihan dan skor dihitung setelah selesai.
- Kunci jawaban dapat ditampilkan setelah sesi.

## Pola soal

Horizontal:
- 2-6 bilangan.
- Penjumlahan dan pengurangan.
- Bilangan kecil sampai 2 digit.
- Hasil tidak dibuat negatif.

Vertikal:
- Penjumlahan/pengurangan 3-4 digit.
- Dua bilangan seperti contoh nomor 31-40 pada gambar.


### Bank soal
40 soal pada gambar yang diberikan dimasukkan secara eksplisit:
- Nomor 1-30: operasi horizontal.
- Nomor 31-40: penjumlahan/pengurangan vertikal.
Jika jumlah soal lebih dari 40, aplikasi menambahkan soal baru yang dibuat secara acak dengan pola yang sama.
