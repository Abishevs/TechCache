from barcode import Code128
from barcode.writer import SVGWriter

def generate_barcode(sku, output_path):
    with open(f'{output_path}.svg', "wb") as f:
        Code128(sku, writer=SVGWriter()).write(f)

# Example usage
generate_barcode('ARD-UNO', 'arduino_uno_barcode')
