import random

def generate_pipe_address():
    # Fixed base address
    base_address = 0xF0F0F0F0
    
    # Generate a random 1-byte address (0x00 to 0xFF)
    unique_byte = random.randint(0x00, 0xFF)
    
    # Combine the base address and the unique byte to form the full address
    pipe_address = (base_address << 8) | unique_byte
    
    # Format the address as a hexadecimal string with 'LL' suffix
    pipe_address_str = f"0x{pipe_address:012X}LL"
    
    return pipe_address_str
