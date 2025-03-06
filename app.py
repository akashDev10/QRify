from flask import Flask, request, jsonify, send_file, render_template_string
import qrcode
import io

app = Flask(__name__)

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

@app.route('/generate_qr', methods=['POST'])
def generate_qr_code():
    data = request.json.get('data')
    qr_type = request.json.get('type')
    print(f"Data received: {data}, Type: {qr_type}")
    
    if qr_type == 'url':
        qr_data = data
    elif qr_type == 'vcard':
        qr_data = f"BEGIN:VCARD\nVERSION:3.0\n{data}\nEND:VCARD"
    else:
        qr_data = data

    img = generate_qr(qr_data)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return send_file(img_byte_arr, mimetype='image/png')

@app.route('/')
def index():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>QR Code Generator</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }
            .form-group {
                margin-bottom: 15px;
            }
            label {
                display: block;
                margin-bottom: 5px;
            }
            input, select, button {
                padding: 8px;
                width: 100%;
            }
            button {
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
                margin-top: 10px;
            }
            button:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <h1>QR Code Generator</h1>
        <form id="qrForm">
            <div class="form-group">
                <label for="qrType">QR Code Type:</label>
                <select id="qrType" name="type">
                    <option value="url">URL</option>
                    <option value="vcard">vCard</option>
                    <option value="text">Plain Text</option>
                </select>
            </div>
            <div class="form-group">
                <label for="qrData">Data:</label>
                <input type="text" id="qrData" name="data" placeholder="Enter URL, vCard data, or text">
            </div>
            <button type="submit">Generate QR Code</button>
        </form>
        <div id="result" style="margin-top: 20px; text-align: center;"></div>

        <script>
            document.getElementById('qrForm').addEventListener('submit', function(e) {
                e.preventDefault();
                
                const data = document.getElementById('qrData').value;
                const type = document.getElementById('qrType').value;
                
                if (!data) {
                    alert('Please enter data for the QR code');
                    return;
                }
                
                fetch('/generate_qr', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        data: data,
                        type: type
                    }),
                })
                .then(response => {
                    if (response.ok) {
                        return response.blob();
                    }
                    throw new Error('Network response was not ok');
                })
                .then(blob => {
                    const imgUrl = URL.createObjectURL(blob);
                    const resultDiv = document.getElementById('result');
                    resultDiv.innerHTML = `
                        <h3>Your QR Code:</h3>
                        <img src="${imgUrl}" alt="QR Code">
                        <p><a href="${imgUrl}" download="qrcode.png">Download QR Code</a></p>
                    `;
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error generating QR code');
                });
            });
        </script>
    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)
