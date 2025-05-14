import re
from datetime import datetime

def validate_nim(nim):
    # Validasi dasar dengan regex
    pattern = r'^09((0[1-3]0)|(0[1-3]1)|(012))[0-9][28](\d{2})(\d{2})(\d{3})$'
    
    match = re.match(pattern, nim)
    
    if not match:
        return False, "NIM tidak sesuai format"
    
    # Ekstrak tahun masuk, keluar, dan nomor mahasiswa
    tahun_masuk = int(match.group(5))
    tahun_keluar = int(match.group(6))
    nomor_urut = match.group(7)  # Tambahkan grup untuk nomor urut mahasiswa
    
    # Validasi nomor urut mahasiswa (001-999)
    if nomor_urut == "000":
        return False, "Nomor urut mahasiswa harus dalam rentang 001-999"
    
    # Menentukan tahun penuh berdasarkan 2 digit
    current_year = datetime.now().year % 100
    century = 2000 if tahun_masuk <= current_year else 1900
    
    tahun_masuk_penuh = century + tahun_masuk
    tahun_keluar_ekspektasi = (tahun_masuk_penuh + 5) % 100  # 5 tahun setelah tahun masuk
    
    if tahun_keluar != tahun_keluar_ekspektasi:
        return False, "Tahun batas studi harus 5 tahun setelah tahun masuk"
    
    return True, "NIM valid"

# Contoh valid: 
nim1 = "09021282328074"
print(validate_nim(nim1))

# Contoh tidak valid
nim2 = "090212825300000"
print(validate_nim(nim2))