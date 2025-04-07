import subprocess
import requests
import json
import private_set_intersection.python as psi

def load_json_file(filename):
    """Load JSON data from a file and return as a dictionary."""
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def mpyc_computation(target_user, user_data, verbose=True):
    
    # start server code 
    requests.post("http://localhost:5000/match_user_mpyc", data={'target_user':target_user, 'verbose':verbose})
    
    # connect to server and run MPyC computation
    # note that currently it says -M2, it should be -M3 for 3 parties but it gets stuck in the mpyc_test file for some reason
    # leaving it as -M2 for now so it can run
    subprocess.run(
        ["python3", "mpyc_test.py", repr(user_data[0]), repr(user_data[1]), repr(verbose), "-M2", "-I0"],
        capture_output=True, text=True
    )
    

def psi_computation(user_id, data, server_data_type):
    
    array = data[0]
    threshold = data[1]
    #create new key for this user
    psi_client = psi.client.CreateWithNewKey(reveal_intersection=False)
    print(f"My key is: {psi_client.GetPrivateKeyBytes()}\n")
    # create request for other user to encode our already encoded data
    psi_request = psi_client.CreateRequest(array).SerializeToString()
    print(f"My encrypted data is:\n {psi_request}\n")

    # creating a package of data to send to the server with our request and what user we want to match with
    files = {
        'user_id': (None, user_id),
        'data': ('psi_request.bin', psi_request, 'application/protobuf')
    }
    # the servers response with our data encoded with the other users key
    psiresponse = requests.post("http://localhost:5000/match_user_psi", files=files)
    
    # getting the response out
    enc_data = psi.Response()
    enc_data.ParseFromString(psiresponse.content)
    print(f"My data response is:\n {enc_data}")

    # getting the other users data depending on the response type (gcs, raw, bloom)
    setup = requests.get(f"http://localhost:5000/{server_data_type}setup")
    
    server_data = psi.ServerSetup()
    server_data.ParseFromString(setup.content)
    print(f"The other party's encrypted data is:\n {server_data}\n")

    # finding the intersection size of the two data sets
    intersection = psi_client.GetIntersectionSize(server_data, enc_data)
    
    # checking if we are a match!
    print("The intersection size is: ", intersection)
    print(f"So on my side it is a {'Match' if intersection >= threshold else 'No Match'}\n")
    
    
    
        
def main():
    # running both methods
    print("Starting MPyC computation...")
    data = load_json_file('user_data_mpyc.json')
    array = data['0'][0]
    threshold = data['0'][1]
    print(f"My array is: {array}")
    print(f"My threshold is: {threshold}")
    mpyc_computation('0', (array, threshold))
    
    print('\n\n'+'*'*100)
    print("\n\nStarting PSI computation...\n")
    data = load_json_file('user_data_psi.json')
    array = data['0'][0]
    threshold = data['0'][1]
    print(f"My array is (sorted for visualization):\n {sorted(array)}\n")
    print(f"My threshold is: {threshold}\n")
    psi_computation('0', (array, threshold), 'raw') #running with raw can change to gcs or bloom
    
if __name__ == "__main__":
    main()