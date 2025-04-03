import json
import random

def generate_data_mpyc(length):
    """Generate a random binary array of the given length."""
    bin_array = [random.randint(0, 1) for _ in range(length)]
    threshold = random.randint(0, length//2)
    return (bin_array, threshold)

def create_user_data_mpyc():
    """Create a dictionary with keys as integers and values as random binary arrays of corresponding lengths."""
    return {size: generate_data_mpyc(size) for size in range(10, 101, 10)}

def create_server_data_mpyc():
    """Create a dictionary with keys as integers and values as dictionaries containing 100 binary arrays each."""
    nested_dict = {}
    for size in range(10, 101, 10):
        nested_dict[size] = {i: generate_data_mpyc(size) for i in range(100)}
    return nested_dict

def write_json_file(filename, data):
    """Write the given data to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def generate_data_psi(length):
    interests = random.sample(range(200), length)
    threshold = random.randint(0, length//2)
    return (['Interest-' + str(i) for i in interests], threshold)

def create_user_data_psi():
    """Create a dictionary with keys as integers and values as random interests of corresponding lengths."""
    return {size: generate_data_psi(size) for size in range(10, 101, 10)}

def create_server_data_psi():
    return {i: generate_data_psi(((i//10) + 1) * 10) for i in range(100)}

def main():
    random.seed(0)
    # Generate MPyC data
    user_data_mpyc = create_user_data_mpyc()
    server_data_mpyc = create_server_data_mpyc()
    
    # Write MPyC data to JSON files
    write_json_file('user_data_mpyc.json', user_data_mpyc)
    write_json_file('server_data_mpyc.json', server_data_mpyc)
    
    # Generate PSI data
    user_data_psi = create_user_data_psi()
    server_data_psi = create_server_data_psi()
    
    # Write PSI data to JSON files
    write_json_file('user_data_psi.json', user_data_psi)
    write_json_file('server_data_psi.json', server_data_psi)

if __name__ == '__main__':
    main()