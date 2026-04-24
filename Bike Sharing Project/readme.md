## Cara menjalankan dashboard

Proyek ini dilengkapi dengan dasbor interaktif menggunakan **Streamlit**. Ikuti langkah-langkah di bawah ini untuk menjalankan dasbor di komputer lokal Anda.

### 1. Persiapan Lingkungan (Setup Environment)
Sangat disarankan untuk menggunakan *virtual environment* agar dependensi library pada proyek ini tidak berbenturan dengan proyek Python Anda yang lain.

**Menggunakan `venv` (Bawaan Python):**
```bash
# Membuat virtual environment bernama 'env'
python -m venv env

# Mengaktifkan virtual environment (Windows)
env\Scripts\activate

# Mengaktifkan virtual environment (Mac/Linux)
source env/bin/activate

### 2. Install Dependensi
pip install -r requirements.txt

### 3. Jalankan Dashboard
streamlit run dashboard/dashboard.py

