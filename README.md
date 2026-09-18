# 🥗 Diet Project - Sistem Rekomendasi Menu Makanan Sehat

Aplikasi berbasis web menggunakan framework **Django** yang berfungsi untuk menghitung kebutuhan gizi harian pengguna (AKG/BMR), indeks massa tubuh (BMI), serta memberikan rekomendasi menu makanan sehat menggunakan metode **Analytic Hierarchy Process (AHP)** dan **Fuzzy Logic (Defuzzifikasi TFN)**.

---

## 🚀 Fitur Utama

- **Kalkulator BMI & Saran Berat Badan**: Menghitung Indeks Massa Tubuh (BMI), kategori berat badan (Kurus, Normal, Overweight, Obesitas), serta saran penyesuaian berat badan ideal.
- **Kalkulator AKG (Angka Kecukupan Gizi)**: Menghitung kebutuhan harian Kalori (BMR/AKG), Karbohidrat, Protein, Lemak, Serat, dan Natrium berdasarkan jenis kelamin, usia, berat badan, tinggi badan, serta tingkat aktivitas harian.
- **Pembobotan Kriteria AHP**: Menghitung pembobotan kriteria gizi (Serat, Protein, Karbohidrat) secara presisi menggunakan matriks perbandingan berpasangan AHP.
- **Rekomendasi Makanan Berbasis Fuzzy**: Melakukan defuzzifikasi pada setiap makanan untuk mendapatkan skor akhir dan ranking rekomendasi makanan sumber Karbohidrat, Protein, Serat, dan Buah.
- **Halaman Manajemen Admin (CRUD)**: Memungkinkan admin untuk melihat, menambah, memperbarui, dan menghapus data nutrisi makanan.
- **Rekomendasi Paket Menu**: Menyediakan pilihan kombinasi menu makanan lengkap sehari-hari.

---

## 🛠️ Teknologi yang Digunakan

- **Backend Framework**: Python 3 & Django 5
- **Database**: SQLite3
- **Data Visualization & Math**: Matplotlib, NumPy
- **Frontend**: HTML5, CSS3, FontAwesome 6

---

## 📦 Panduan Instalasi & Penggunaan

### 1. Prasyarat
Pastikan Anda sudah menginstal **Python 3.10+** dan **Git** di komputer Anda.

### 2. Clone Repository
```bash
git clone https://github.com/faisaldzkr04/diet_project.git
cd diet_project
```

### 3. Buat dan Aktifkan Virtual Environment
- **Windows (PowerShell/CMD):**
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```
- **Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Install Dependensi
```bash
pip install django matplotlib django-extensions
```

### 5. Jalankan Migrasi Database
```bash
python manage.py migrate
```

### 6. Jalankan Server Pengembangan
```bash
python manage.py runserver
```
Buka browser Anda dan akses aplikasi di: **`http://127.0.0.1:8000/`**

---

## 📂 Struktur Project

```text
diet_project/
├── diet_app/               # Aplikasi utama Django
│   ├── templates/          # Template HTML (User, Admin, Main)
│   ├── forms.py            # Form penginputan data makanan
│   ├── models.py           # Model database Food
│   ├── urls.py             # URL routing diet_app
│   └── views.py            # Logika AHP, Fuzzy, BMI, AKG, & Admin
├── diet_project/           # Konfigurasi utama Django project
│   ├── settings.py         # Pengaturan project
│   └── urls.py             # Root URL routing
├── tests/                  # Pengujian (Selenium & Locust)
├── db.sqlite3              # Database SQLite
├── manage.py               # Skrip manajemen Django
├── .gitignore              # File igrasi Git
└── README.md               # Dokumentasi project
```

---

## 👤 Pengembang

- **Faisal Dzikri** - [faisaldzkr04](https://github.com/faisaldzkr04)
