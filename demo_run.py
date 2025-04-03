import subprocess
import requests
import asyncio
import json
import time
import private_set_intersection.python as psi

def load_json_file(filename):
    """Load JSON data from a file and return as a dictionary."""
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def mpyc_computation(size, target_user, user_data, verbose=True):
    
    # Contact server to make sure it's ready
    response = requests.post("http://localhost:5000/match_user_mpyc", data={'size':size, 'target_user':target_user, 'verbose':verbose})

    result = subprocess.run(
        ["python3", "mpyc_test.py", repr(user_data[0]), repr(user_data[1]), repr(verbose), "-M2", "-I0"],
        capture_output=True, text=True
    )
    
    print(f"Secure dot product result:\n {result.stdout.strip()}")
    

def psi_computation(user_id, data, server_data_type):
    # Contact server to make sure it's ready
    array = data[0]
    threshold = data[1]
    psi_client = psi.client.CreateWithNewKey(reveal_intersection=False)
    print(f"My key is: {psi_client.GetPrivateKeyBytes()}\n")
    psi_request = psi_client.CreateRequest(array).SerializeToString()
    print(f"My encrypted data is:\n {psi_request}\n")
    files = {
        'user_id': (None, user_id),
        'data': ('psi_request.bin', psi_request, 'application/protobuf')
    }
    psiresponse = requests.post("http://localhost:5000/match_user_psi", files=files)
    
    enc_data = psi.Response()
    enc_data.ParseFromString(psiresponse.content)
    print(f"My data response is:\n {enc_data}")
    
    setup = requests.get(f"http://localhost:5000/{server_data_type}setup")
    
    server_data = psi.ServerSetup()
    server_data.ParseFromString(setup.content)
    print(f"The other party's encrypted data is:\n {server_data}\n")
    
    intersection = psi_client.GetIntersectionSize(server_data, enc_data)
    
    print("The intersection size is: ", intersection)
    print(f"So on my side it is a {'Match' if intersection >= threshold else 'No Match'}\n")
        
def main():
    print("Starting MPyC computation...")
    data = load_json_file('user_data_mpyc.json')
    array = data['0'][0]
    threshold = data['0'][1]
    print(f"My array is: {array}")
    print(f"My threshold is: {threshold}")
    mpyc_computation('0', '0', (array, threshold))
    
    print('\n\n*'*150)
    print("\n\nStarting PSI computation...\n")
    data = load_json_file('user_data_psi.json')
    array = data['0'][0]
    threshold = data['0'][1]
    print(f"My array is (sorted for visualization):\n {sorted(array)}\n")
    print(f"My threshold is: {threshold}\n")
    psi_computation('0', (array, threshold), 'raw')
    
if __name__ == "__main__":
    main()