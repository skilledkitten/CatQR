# CatQR 🐱📸

CatQR is a minimal yet powerful QR code generator written in Python. Built without relying on the `qrcode` library, it demonstrates the core principles of QR code generation from scratch.

## Features

- 🚀 Generates standard QR codes
- 🎯 Lightweight and dependency-free
- 🐾 Focused on demonstrating pure coding skills

## Installation

Clone the repository:

```bash
git clone https://github.com/skilledkitten/catqr.git
cd catqr
```

## Usage

1. Run the script:
   ```bash
   python catqr.py
   ```
2. Enter the text or URL you'd like to encode.
3. View the output, which will be a QR code image saved in the `/output` folder.

## Example

Here's an example of a generated QR code:

![Example QR Code](https://via.placeholder.com/150)

## How It Works

CatQR manually implements the principles of QR code generation:
- **Data encoding**: Converts input text into binary format.
- **Error correction**: Adds error correction data for robust QR codes.
- **Module placement**: Maps the binary data onto the QR code grid.
- **Output**: Renders the QR code as an image.

## Roadmap

- [ ] Add support for custom sizes and colors
- [ ] Implement more error correction levels
- [ ] Explore optional optimizations

## Contributing

This project is a learning exercise, but feedback and suggestions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Happy coding with CatQR! 😺
