from flask import Flask, render_template, request, jsonify
import re
from datetime import datetime

app = Flask(__name__)

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
    
    # Jika valid, kumpulkan informasi detail
    kode_fakultas = "09"
    kode_program = match.group(1)
    tahun_masuk_penuh = century + tahun_masuk
    tahun_keluar_penuh = century + tahun_keluar
    
    detail = {
        "kode_fakultas": kode_fakultas,
        "kode_program": kode_program,
        "tahun_masuk": tahun_masuk_penuh,
        "tahun_batas_studi": tahun_keluar_penuh,
        "nomor_urut": nomor_urut
    }
    
    return True, "NIM valid", detail

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    nim = request.form.get('nim', '')
    
    if len(nim) > 0:
        valid, message, *detail = validate_nim(nim)
        
        result = {
            'valid': valid,
            'message': message
        }
        
        if valid and detail:
            result['detail'] = detail[0]
        
        return jsonify(result)
    else:
        return jsonify({'valid': False, 'message': 'Masukkan NIM terlebih dahulu'})

if __name__ == '__main__':
    app.run(debug=True)