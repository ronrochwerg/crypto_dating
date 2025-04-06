import json
import random

def get_binary_list():
    user_input = input("Enter a binary list (e.g., [0, 1, 1, 0]) or an integer: ")
    try:
        # Attempt to interpret the input as a list
        binary_list = eval(user_input)
        if isinstance(binary_list, list) and all(x in [0, 1] for x in binary_list):
            return binary_list
        else:
            raise ValueError
    except:
        # If not a list, treat input as an integer
        try:
            length = int(user_input)
            return [random.choice([0, 1]) for _ in range(length)]
        except ValueError:
            print("Invalid input. Please enter a binary list or an integer.")
            return get_binary_list()

def get_threshold():
    while True:
        try:
            threshold = int(input("Enter a threshold value: "))
            return threshold
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_string_list():
    user_input = input("Enter a list of strings (e.g., ['pigeon', 'session key']) or an integer: ")
    try:
        # Attempt to interpret the input as a list
        string_list = eval(user_input)
        if isinstance(string_list, list) and all(isinstance(x, str) for x in string_list):
            return string_list
        else:
            raise ValueError
    except:
        # If not a list, treat input as an integer
        try:
            length = int(user_input)
            return [f"interest-{random.randint(0, length * 2)}" for _ in range(length)]
        except ValueError:
            print("Invalid input. Please enter a list of strings or an integer.")
            return get_string_list()

def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    random.seed(0)
    # Process for user_data_mpyc.json
    binary_list = get_binary_list()
    threshold = get_threshold()
    user_data_mpyc = {'0': (binary_list, threshold)}
    save_json(user_data_mpyc, 'user_data_mpyc.json')

    binary_list = get_binary_list()
    threshold = get_threshold()
    user_data_mpyc = {'0': (binary_list, threshold)}
    # Process for server_data_mpyc.json
    server_data_mpyc = {'0': user_data_mpyc}
    save_json(server_data_mpyc, 'server_data_mpyc.json')

    # Process for user_data_psi.json
    string_list = get_string_list()
    threshold = get_threshold()
    user_data_psi = {'0': (string_list, threshold)}
    save_json(user_data_psi, 'user_data_psi.json')

    string_list = get_string_list()
    threshold = get_threshold()
    user_data_psi = {'0': (string_list, threshold)}
    # Process for server_data_psi.json
    save_json(user_data_psi, 'server_data_psi.json')

if __name__ == "__main__":
    main()
