"""Konstanta bersama untuk spesifikasi komponen: grup, status, dan pilihan isian.

Hanya data murni, tanpa Streamlit. Dipakai oleh specs/core.py, specs/extra.py,
dan dire-ekspor oleh specs/__init__.py.
"""
GROUP_ORDER = [
    "Dasar", "Navigasi", "Aksi", "Informasi", "Data",
    "Formulir", "Media", "Sosial", "Toko",
]
STATUS_KINDS = {"info": "Info", "success": "Sukses", "warning": "Peringatan", "error": "Galat"}
STATUS_ICONS = {"info": "info", "success": "check_circle", "warning": "warning", "error": "error"}
ICON_HINT = "Nama ikon mengikuti Material Symbols (contoh: home, search, person). Daftar lengkap: fonts.google.com/icons"
# Daftar jenis isian untuk komponen formulir (dipakai specs/extra.py dan render/extra.py).
INPUT_KIND_LIST = {"text": "Teks", "email": "Email", "password": "Kata sandi", "number": "Angka", "tel": "Telepon"}
VIEW_KINDS = {"grid": "Grid", "list": "Daftar"}
STOCK_KINDS = {"ready": "Tersedia", "low": "Terbatas", "out": "Habis"}
PLAY_KINDS = {"pause": "Sedang diputar", "play": "Berhenti"}  # status pemutar
ALIGN_KINDS = {"left": "Kiri", "center": "Tengah", "right": "Kanan"}
