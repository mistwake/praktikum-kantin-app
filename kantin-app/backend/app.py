from flask import Flask, jsonify, request
from flask_cors import CORS
import os # import os untuk baca variabel lingkungan

app = Flask(__name__)
CORS(app)

# mengambil variabel nama dan nim dari environment yaml, kalau kosong pakai default
nama = os.getenv("NAMA", "Anonim")
nim = os.getenv("NIM", "000000")

kantin_data = {
    # menyuntikkan identitas ke nama kantin
    "nama_kantin": f"Kantin FPMIPA - {nama} ({nim})",
    "menu": ["Nasi Goreng", "Es Teh", "Gorengan"]
}

# membuat rute api untuk mengambil data info kantin
@app.route('/api/info', methods=['GET'])
def get_info():
    return jsonify(kantin_data)


# membuat rute api untuk menambahkan menu baru
@app.route('/api/add-menu', methods=['POST'])
def add_menu():
    new_item = request.json.get('item')
    if new_item:
        kantin_data["menu"].append(new_item)
        return jsonify({"message": "Menu berhasil ditambah!", "menu": kantin_data["menu"]}), 201
    return jsonify({"error": "Data tidak valid"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)