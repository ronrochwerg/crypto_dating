import matplotlib.pyplot as plt
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

def mpyc_computation(size, target_user, user_data, verbose=False):
    
    # Contact server to make sure it's ready
    response = requests.post("http://localhost:5000/match_user_mpyc", data={'size':size, 'target_user':target_user, 'verbose':verbose})

    if verbose:
        result = subprocess.run(
            ["python3", "mpyc_test.py", repr(user_data[0]), repr(user_data[1]), repr(verbose), "-M3", "-I0"],
            capture_output=True, text=True
        )
        
        print(f"Secure dot product result:\n {result.stdout.strip()}")
    else:
        result = subprocess.run(
            ["python3", "mpyc_test.py", repr(user_data[0]), repr(user_data[1]), repr(verbose), "-M3", "-I0", "--no-log"],
            capture_output=True, text=True
        )

def test_mpyc(verbose=False):
    data = load_json_file('user_data_mpyc.json')
    average_times = []

    for size, user_data in data.items():
        times = []
        for target_user in range(100):
            time.sleep(0.2)
            start_time = time.time()
            mpyc_computation(size, target_user, user_data, verbose=verbose)
            end_time = time.time()
            times.append(end_time - start_time)
        
        # Calculate the average time for this size
        average_time = sum(times) / len(times)
        average_times.append((size, average_time))
    
    # Plot the results
    sizes, avg_times = zip(*average_times)
    plt.plot(sizes, avg_times, marker='o')
    plt.xlabel('Input Size')
    plt.ylabel('Average Computation Time (s)')
    plt.title('Average Computation Time vs Input Size')
    plt.grid()
    plt.savefig('mpyc_computation_time.png')

def psi_computation(user_id, data, server_data_type):
    # Contact server to make sure it's ready
    psi_client = psi.client.CreateWithNewKey(reveal_intersection=False)
    psi_request = psi_client.CreateRequest(data).SerializeToString()
    files = {
        'user_id': (None, user_id),
        'data': ('psi_request.bin', psi_request, 'application/protobuf')
    }
    psiresponse = requests.post("http://localhost:5000/match_user_psi", files=files)
    
    enc_data = psi.Response()
    enc_data.ParseFromString(psiresponse.content)
    
    setup, server_threshhold = requests.get(f"http://localhost:5000/{server_data_type}setup")
    
    server_data = psi.ServerSetup()
    server_data.ParseFromString(setup.content)
    
    intersection = psi_client.GetIntersectionSize(server_data, enc_data)
    
    print(intersection)

def main():
    test_mpyc(verbose=True)
    # data = load_json_file('user_data_psi.json')
    # user_data = data['10'][0]
    # threshold = data['10'][1]
    # psi_computation(0, user_data, 'raw')

if __name__ == "__main__":
    # Run the main function within the asyncio event loop
    main()