### 🤖 AI Chatbot Senn

Semantic Search–Based AI Chatbot using Sentence Transformers & Flask

---

### 📌 Deskripsi Proyek

**AI Chatbot Senn** adalah aplikasi chatbot berbasis web yang menggunakan **semantic search** untuk menjawab pertanyaan pengguna berdasarkan basis pengetahuan (knowledge base). Chatbot ini tidak menggunakan rule-based sederhana, melainkan **embedding vektor** dari model NLP (*Sentence Transformer*) untuk mencari jawaban paling relevan secara semantik.

Aplikasi ini dikembangkan menggunakan **Flask** sebagai backend dan mendukung:
- Multi-chat session
- Penyimpanan history percakapan
- Pencarian jawaban berbasis kemiripan makna (cosine similarity)

---

### 🎯 Tujuan
- Menerapkan konsep **Natural Language Processing (NLP)**
- Mengimplementasikan **semantic search** menggunakan embedding
- Membangun chatbot edukatif berbasis AI
- Mendukung kebutuhan tugas / proyek mata kuliah **Kecerdasan Buatan**

---

### 🧠 Teknologi yang Digunakan
- **Python 3.10**
- **Flask**
- **Sentence-Transformers**
- **PyTorch (CPU)**
- **Pandas**
- **HTML, CSS, JavaScript**

---

### 📂 Struktur Folder
```text
search_engine_project/
│
├─ app.py                 # Main Flask application
├─ kb/
│   └─ kb.csv             # Database csv
├─ src/
│   └─ search.py          # Logic embedding & semantic search
│
├─ templates/             # HTML templates
├─ static/                # CSS / JS assets
│
├─ flask_session/         # (ignored) Flask session storage
├─ models/                # (ignored) AI models / embeddings
├─ venv/                  # (ignored) Virtual environment
│
├─ .gitignore
├─ requirements.txt
└─ README.md
```
---

### ⚙️ Cara Menjalankan Aplikasi
1️⃣ Clone Repository
```text
git clone https://github.com/USERNAME/REPO.git
cd search_engine_project
```
2️⃣ Buat Virtual Environment
```text
py -3.10 -m venv venv
venv\Scripts\activate
```
3️⃣ Install Dependencies
```text
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install sentence-transformers flask flask-session pandas
```
4️⃣ Jalankan Aplikasi
```text
python app.py
```
Akses melalui browser:
```text
http://127.0.0.1:5000
```
---

### 💬 Fitur Utama
🔍 Semantic Search menggunakan embedding vektor

🤖 Jawaban berdasarkan kemiripan makna, bukan kata kunci

🗂️ Multi-chat session (bisa banyak percakapan)

💾 History chat tersimpan selama session aktif

🌐 Antarmuka berbasis web

### 🧪 Contoh Alur Kerja
- Pengguna memasukkan pertanyaan
- Pertanyaan diubah menjadi embedding vektor
- Sistem membandingkan embedding dengan knowledge base
- Jawaban dengan skor tertinggi dikembalikan ke pengguna

### 🚫 File yang Tidak Di-Commit
Beberapa folder tidak di-upload ke GitHub demi keamanan & efisiensi:
```text
venv/
models/
flask_session/
__pycache__/
Detail ada di file .gitignore.
```
### 📖 Catatan Penting
- Proyek ini menggunakan PyTorch CPU (tanpa GPU)
- Disarankan menggunakan Python 3.10 untuk stabilitas
- Cocok untuk pengembangan chatbot edukatif / penelitian NLP dasar

### 👨‍🎓 Konteks Akademik
Proyek ini dikembangkan sebagai bagian dari:

Mata Kuliah: Kecerdasan Buatan

Topik: Chatbot Berbasis Semantic Search

---

### 📜 Lisensi
Proyek ini dibuat untuk keperluan akademik dan pembelajaran.
