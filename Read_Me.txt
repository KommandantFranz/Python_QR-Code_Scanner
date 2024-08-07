# USB Barcode Scanner Reader

This Python script reads data from a USB barcode scanner, decodes the HID key codes into readable characters, prints the data to the console, and saves it to a text file. The program automatically restarts after completing a data read cycle.

## Usage

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/usb-barcode-scanner-reader.git
    cd usb-barcode-scanner-reader
    ```

2. **Install dependencies**:
    Ensure you have `pyusb` installed:
    ```bash
    pip install pyusb
    ```

3. **Configure the script**:
    - Open `scanner_reader.py` in a text editor.
    - Replace `VENDOR_ID` and `PRODUCT_ID` with your USB device's vendor and product IDs.
    - Update the `FILE_PATH` with the desired path to save the data.

4. **Run the script**:
    ```bash
    python scanner_reader.py
    ```

## Notes

- The script will continuously read data from the barcode scanner and restart after completing each read cycle.
- Collected data is printed to the console and saved to the specified file, overwriting any existing content.

## License

This project is licensed under the AGPL License.
