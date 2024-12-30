import numpy as np
import time
import functools

# Define the error correction level H (30%)
ERROR_CORRECTION_H = 'H'

# Encoding mode indicator for byte mode
MODE_INDICATOR = '0100'

# Galois Field (GF(256)) tables
GF256_EXP = [0] * 512
GF256_LOG = [0] * 256

# Initialize the Galois Field tables
def init_gf256():
    x = 1
    for i in range(255):
        GF256_EXP[i] = x
        GF256_LOG[x] = i
        x <<= 1
        if x & 0x100:
            x ^= 0x11d
    for i in range(255, 512):
        GF256_EXP[i] = GF256_EXP[i - 255]

init_gf256()

def gf256_add(x, y):
    return x ^ y

def gf256_sub(x, y):
    return x ^ y

def gf256_mul(x, y):
    if x == 0 or y == 0:
        return 0
    return GF256_EXP[GF256_LOG[x] + GF256_LOG[y]]

def gf256_div(x, y):
    if y == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    if x == 0:
        return 0
    return GF256_EXP[(GF256_LOG[x] + 255 - GF256_LOG[y]) % 255]

def gf256_poly_mul(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for j in range(len(q)):
        for i in range(len(p)):
            r[i + j] ^= gf256_mul(p[i], q[j])
    return r

def gf256_poly_div(dividend, divisor):
    result = list(dividend)
    for i in range(len(dividend) - len(divisor) + 1):
        coef = result[i]
        if coef != 0:
            for j in range(1, len(divisor)):
                if divisor[j] != 0:
                    result[i + j] ^= gf256_mul(divisor[j], coef)
    separator = -(len(divisor) - 1)
    return result[:separator], result[separator:]

def rs_generator_poly(nsym):
    g = [1]
    for i in range(nsym):
        g = gf256_poly_mul(g, [1, GF256_EXP[i]])
    return g

def rs_encode_msg(msg_in, nsym):
    if len(msg_in) + nsym > 255:
        raise ValueError("Message too long")
    gen = rs_generator_poly(nsym)
    msg_out = list(msg_in) + [0] * nsym
    _, remainder = gf256_poly_div(msg_out, gen)
    return msg_in + remainder

def encode_data(data):
    """Encode the input data into binary format using byte mode."""
    # Convert each character to its ASCII value and then to an 8-bit binary string
    bits = ''.join(format(ord(char), '08b') for char in data)
    
    # Add mode indicator and character count
    length = len(data)
    length_bits = format(length, '08b')  # Version 1 can handle up to 25 characters in byte mode
    return MODE_INDICATOR + length_bits + bits

def add_error_correction(data_bits):
    """Add error correction to the encoded data using Reed-Solomon encoding."""
    # Convert bits to byte array
    data_bytes = [int(data_bits[i:i+8], 2) for i in range(0, len(data_bits), 8)]
    
    # Determine the number of error correction codewords
    version = 1  # Simplified to use version 1
    nsym = 7  # Number of error correction codewords for version 1-H
    
    # Generate error correction codewords
    encoded_data = rs_encode_msg(data_bytes, nsym)
    
    # Convert back to bits
    encoded_bits = ''.join(format(byte, '08b') for byte in encoded_data)
    return encoded_bits

def create_qr_matrix(version, bits):
    """Create the QR code matrix for the given version and bits."""
    # Determine the size of the QR code matrix
    size = 4 * version + 17
    matrix = np.zeros((size, size), dtype=int)

    # Add finder patterns
    def add_finder_pattern(r, c):
        pattern = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1],
        ]
        for dr in range(7):
            for dc in range(7):
                matrix[r + dr][c + dc] = pattern[dr][dc]
    
    add_finder_pattern(0, 0)
    add_finder_pattern(0, size - 7)
    add_finder_pattern(size - 7, 0)

    # Add alignment pattern for version 1 (centered at position 18 for version 1)
    def add_alignment_pattern(r, c):
        pattern = [
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1],
        ]
        for dr in range(5):
            for dc in range(5):
                matrix[r + dr][c + dc] = pattern[dr][dc]
    
    if version > 1:
        add_alignment_pattern(size // 2 - 2, size // 2 - 2)

    # For simplicity, we'll just fill the matrix with the bits sequentially
    bit_index = 0
    for r in range(size):
        for c in range(size):
            if bit_index < len(bits) and matrix[r][c] == 0:
                matrix[r][c] = int(bits[bit_index])
                bit_index += 1

    return matrix

def print_qr_matrix_flow(matrix):
    """Print the QR code matrix row by row with a delay to create a flowing effect."""
    for row in matrix:
        line = ''.join('██' if cell else '  ' for cell in row)
        print(line)
        time.sleep(0.1)  # Adjust the delay as desired

def qr_code_generator(data):
    """Generate a QR code from the input data."""
    # Step 1: Encode the data
    encoded_data = encode_data(data)

    # Step 2: Add error correction
    data_with_error_correction = add_error_correction(encoded_data)

    # Step 3: Determine the QR code version (simplified)
    version = 1  # For simplicity, we use version 1

    # Step 4: Create the QR code matrix
    qr_matrix = create_qr_matrix(version, data_with_error_correction)

    # Step 5: Print the QR code matrix with a flowing effect
    print_qr_matrix_flow(qr_matrix)

# Example usage
data = "HELLO WORLD"
qr_code_generator(data)