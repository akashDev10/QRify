from flask import Flask, request, jsonify, send_file, url_for
import qrcode
import io
import os
import base64
from pathlib import Path
import barcode
from barcode.writer import SVGWriter
import uuid
from datetime import datetime

app = Flask(__name__, static_folder='.')

# Ensure the static/qrcodes directory exists
os.makedirs('static/qrcodes', exist_ok=True)

def generate_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img

def generate_barcode(data, barcode_type='code128'):
    """Generate a barcode using python-barcode library with SVG output for PDF compatibility"""
    if barcode_type == 'code128':
        bc = barcode.get_barcode_class('code128')
    elif barcode_type == 'ean13':
        bc = barcode.get_barcode_class('ean13')
    else:
        bc = barcode.get_barcode_class('code128')
    
    # Create BytesIO object to hold the SVG
    svg_byte_arr = io.BytesIO()
    
    # Generate barcode with SVGWriter for PDF compatibility
    writer = SVGWriter()
    bc(data, writer=writer).write(svg_byte_arr)
    
    # Reset BytesIO position
    svg_byte_arr.seek(0)
    
    return svg_byte_arr

def get_unique_filename(user_filename, file_ext):
    """Generate a unique filename using the user-provided name or a UUID"""
    if not user_filename:
        # Generate a unique filename based on timestamp and UUID
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{timestamp}_{unique_id}.{file_ext}"
    else:
        # Sanitize the user-provided filename
        sanitized_name = "".join(c for c in user_filename if c.isalnum() or c in ['-', '_']).lower()
        if not sanitized_name:
            sanitized_name = "qrcode"
        filename = f"{sanitized_name}.{file_ext}"
    
    # Check if file already exists, append number if needed
    file_path = os.path.join('static/qrcodes', filename)
    counter = 1
    base_name, ext = os.path.splitext(filename)
    
    while os.path.exists(file_path):
        filename = f"{base_name}_{counter}{ext}"
        file_path = os.path.join('static/qrcodes', filename)
        counter += 1
    
    return filename

@app.route('/generate_qr', methods=['POST'])
def generate_qr_code():
    data = request.json.get('data')
    qr_type = request.json.get('type')
    filename = request.json.get('filename', '')
    
    print(f"Data received: {data}, Type: {qr_type}, Filename: {filename}")
    
    if qr_type == 'URL':
        qr_data = data
    elif qr_type == 'vCard':
        # The vCard data should already be formatted by the frontend
        qr_data = data
    elif qr_type == 'Barcode':
        # Use QR code generation for barcodes instead of SVG barcode
        qr_data = data
    else:
        qr_data = data
    
    # Generate QR code image
    img = generate_qr(qr_data)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    # Get unique filename with .png extension
    unique_filename = get_unique_filename(filename, 'png')
    file_path = os.path.join('static/qrcodes', unique_filename)
    
    # Save the QR code to file
    with open(file_path, 'wb') as f:
        f.write(img_byte_arr.getvalue())
    
    # Reset buffer position
    img_byte_arr.seek(0)
    
    # Convert the image to base64 for preview
    encoded_img = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
    
    # Generate URL for the saved file
    file_url = f"/static/qrcodes/{unique_filename}"
    
    # Return JSON with both base64 and file URL
    return jsonify({
        'qr_code': encoded_img,
        'file_url': file_url,
        'filename': unique_filename
    })

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/static/qrcodes/<path:filename>')
def serve_qrcode(filename):
    """Serve QR code and barcode images from the static/qrcodes directory"""
    file_path = os.path.join('static/qrcodes', filename)
    if filename.endswith('.svg'):
        return send_file(file_path, mimetype='image/svg+xml')
    else:
        return send_file(file_path)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
