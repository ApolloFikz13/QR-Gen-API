from flask import Flask, request, send_file
import qrcode
import io

app = Flask(__name__)

@app.route('/generate-qr-SAP', methods=['GET'])
def generate_qr():
    data = request.args.get('teks')
    size = request.args.get('size', '700x700') 

    if not data:
        return {"error": "'teks' data tidak ditemukan/kosong"}, 400

    try:
        width, height = map(int, size.lower().split('x'))
    except ValueError:
        return {"error": "Size salah, contoh ukuran: 500x500"}, 400

    qr = qrcode.QRCode(
        version=3, #pilih versi QR
        error_correction=qrcode.constants.ERROR_CORRECT_H,  
        box_size=30,  
        border=1  
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    img = img.resize((width, height), resample=3)  

    img_io = io.BytesIO()
    img.save(img_io, 'PNG', quality=100)  
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
