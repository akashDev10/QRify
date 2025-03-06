# ScanCraft

A versatile QR code generator web application built with Flask.

![ScanCraft Logo](https://via.placeholder.com/150?text=ScanCraft)

## Features

- **Multiple QR Code Types**: Generate QR codes for:
  - URLs
  - vCards (contact information)
  - Plain text
- **User-Friendly Interface**: Simple, intuitive web interface
- **Preview Functionality**: See your QR code before downloading
- **Download Option**: Save generated QR codes to your device
- **Responsive Design**: Works on desktop and mobile devices

## Screenshots

![ScanCraft Screenshot](https://via.placeholder.com/800x450?text=ScanCraft+Screenshot)

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ScanCraft.git
   cd ScanCraft
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv env
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     env\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source env/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install flask qrcode pillow
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your web browser and navigate to `http://localhost:5000`

## Usage

1. **Select QR Code Type**
   - Choose between URL, vCard, or Plain Text

2. **Enter Data**
   - For URLs: Enter a valid web address (e.g., https://example.com)
   - For vCards: Fill in contact information (name, phone, email, etc.)
   - For Plain Text: Enter any text you wish to encode

3. **Generate QR Code**
   - Click the "Generate QR Code" button

4. **Preview & Download**
   - Review the generated QR code
   - Click the "Download" button to save it to your device

## Customization

You can customize various aspects of your QR codes by modifying the parameters in the `app.py` file:

- QR code size
- Error correction level
- Border size
- QR code color

## Development

### Project Structure

```
ScanCraft/
├── app.py            # Main Flask application file
├── index.html        # HTML template
├── requirements.txt  # Python dependencies
├── static/           # Static files (CSS, JS, images)
└── env/              # Virtual environment (not tracked by Git)
```

### Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature-branch`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/) - The web framework used
- [qrcode](https://github.com/lincolnloop/python-qrcode) - Python QR Code generator
- [Pillow](https://python-pillow.org/) - Python Imaging Library

## Contact

If you have any questions or suggestions, feel free to open an issue or contact the maintainer at:
- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)

---

Made with ❤️ by [Your Name]

