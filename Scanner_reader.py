import usb.core
import usb.util
import time

# Constants for the USB device's Vendor ID and Product ID
VENDOR_ID = 0x34EB
PRODUCT_ID = 0x1502

# HID keyboard code to ASCII translation tables
HID_KEYCODES = {
    4: ('a', 'A'), 5: ('b', 'B'), 6: ('c', 'C'), 7: ('d', 'D'), 8: ('e', 'E'), 9: ('f', 'F'), 10: ('g', 'G'), 11: ('h', 'H'), 12: ('i', 'I'), 13: ('j', 'J'),
    14: ('k', 'K'), 15: ('l', 'L'), 16: ('m', 'M'), 17: ('n', 'N'), 18: ('o', 'O'), 19: ('p', 'P'), 20: ('q', 'Q'), 21: ('r', 'R'), 22: ('s', 'S'), 23: ('t', 'T'),
    24: ('u', 'U'), 25: ('v', 'V'), 26: ('w', 'W'), 27: ('x', 'X'), 28: ('y', 'Y'), 29: ('z', 'Z'), 30: ('1', '!'), 31: ('2', '@'), 32: ('3', '#'), 33: ('4', '$'),
    34: ('5', '%'), 35: ('6', '^'), 36: ('7', '&'), 37: ('8', '*'), 38: ('9', '('), 39: ('0', ')'), 40: ('\n', '\n'), 41: ('\x1b', '\x1b'), 42: ('\b', '\b'), 43: ('\t', '\t'),
    44: (' ', ' '), 45: ('-', '_'), 46: ('=', '+'), 47: ('[', '{'), 48: (']', '}'), 49: ('\\', '|'), 51: (';', ':'), 52: ("'", '"'), 53: ('', '~'), 54: (',', '<'), 55: ('.', '>'), 56: ('/', '?')
}

# File path for saving data
FILE_PATH = 'path_to_your_file.txt'  # Replace with your file path

while True:
    # Find the USB device
    dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

    if dev is None:
        raise ValueError('Device not found')

    # Set the configuration of the device
    dev.set_configuration()

    # Get the active configuration
    cfg = dev.get_active_configuration()

    # Get the first interface
    intf = cfg[(0, 0)]

    # Find the endpoint for data reception
    ENDPOINT_ADDRESS = 0x81  # Example endpoint address

    ep = usb.util.find_descriptor(
        intf,
        custom_match=lambda e: e.bEndpointAddress == ENDPOINT_ADDRESS
    )

    if ep is None:
        raise ValueError(f"Endpoint {hex(ENDPOINT_ADDRESS)} not found.")

    # Function to decode HID data to readable characters
    def decode_hid_data(data):
        shift_pressed = data[0] & 0b00100010  # Check if either shift key is pressed
        chars = []
        for byte in data[2:]:
            if byte > 0:
                char_pair = HID_KEYCODES.get(byte, ('', ''))
                chars.append(char_pair[1] if shift_pressed else char_pair[0])
        return ''.join(chars)

    data_buffer = []  # Array to store received data
    data_received = False  # Flag to check if data was received

    try:
        while True:
            try:
                data = dev.read(ep.bEndpointAddress, ep.wMaxPacketSize)
                # Convert the byte array to readable characters
                readable_data = decode_hid_data(data)
                if readable_data:
                    data_buffer.append(readable_data.replace(' ', ''))
                    print('Data received:', readable_data)
                    data_received = True  # Set flag that data was received
            except usb.core.USBError as e:
                if data_received:
                    # Exit the loop if an error occurs after data was received
                    print("Data read, restarting program.")
                    break
                else:
                    print("No data")
    except KeyboardInterrupt:
        print("Program terminated.")
        break
    finally:
        # Print the collected data to the console
        if data_buffer:
            all_data = ''.join(data_buffer)
            print("Collected data:", all_data)

            # Clear the file content and save the new data
            with open(FILE_PATH, 'w') as file:
                file.write(all_data + '\n')

        # Clean up
        usb.util.dispose_resources(dev)
        
    # Short delay before restarting (increase if needed)
    time.sleep(1)