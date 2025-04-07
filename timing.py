import matplotlib.pyplot as plt
import subprocess
import requests
import json
import time
import private_set_intersection.python as psi
from demo_data import create_data

def load_json_file(filename):
    """Load JSON data from a file and return as a dictionary."""
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def mpyc_computation(target_user, user_data, verbose=False):
    
    # start server code 
    requests.post("http://localhost:5000/match_user_mpyc", data={'target_user':target_user, 'verbose':verbose})

    # connect to server and run MPyC computation
    # note that currently it says -M2, it should be -M3 for 3 parties but it gets stuck in the mpyc_test file for some reason
    # leaving it as -M2 for now so it can run
    subprocess.run(
        ["python3", "mpyc_test.py", repr(user_data[0]), repr(user_data[1]), repr(verbose), "-M2", "-I0", "--no-log"],
        capture_output=True, text=True
    )

def test_mpyc(verbose=False):
    # time and run the mpyc code
    data = load_json_file('user_data_mpyc.json')
    start_time = time.time()
    mpyc_computation('0', data['0'], verbose=verbose)
    end_time = time.time()
    return end_time - start_time
    
def psi_computation(server_data_type):
    # run the psi code
    data = load_json_file('user_data_psi.json')
    start_time = time.time()
    array = data['0'][0]
    threshold = data['0'][1]
    #create new key for this user
    psi_client = psi.client.CreateWithNewKey(reveal_intersection=False)

    # create request for other user to encode our already encoded data
    psi_request = psi_client.CreateRequest(array).SerializeToString()

    # creating a package of data to send to the server with our request and what user we want to match with
    files = {
        'user_id': (None, '0'),
        'data': ('psi_request.bin', psi_request, 'application/protobuf')
    }
    # the servers response with our data encoded with the other users key
    psiresponse = requests.post("http://localhost:5000/match_user_psi", files=files)
    
    # getting the response out
    enc_data = psi.Response()
    enc_data.ParseFromString(psiresponse.content)

    # getting the other users data depending on the response type (gcs, raw, bloom)
    setup = requests.get(f"http://localhost:5000/{server_data_type}setup")
    
    server_data = psi.ServerSetup()
    server_data.ParseFromString(setup.content)

    # finding the intersection size of the two data sets
    intersection = psi_client.GetIntersectionSize(server_data, enc_data)
    
    # checking if we are a match! (does not matter for timing purposes)
    is_match = intersection >= threshold
    
    end_time = time.time()
    return end_time - start_time
    


def plot_times(data, method):
    # for plotting times
    sizes, avg_times = zip(*data)
    plt.plot(sizes, avg_times, marker='o', label=method)
    plt.xlabel('Input Size')
    plt.ylabel('Average Computation Time (s)')
    plt.title(f'Average Computation Time vs Input Size')
    plt.grid()
    

def main():
    # run the code on different lengths of data and average the times
    lengths = [100, 500, 1000, 5000, 10000]
    mpyc_times = []
    psi_gcs_times = []
    psi_raw_times = []
    psi_bloom_times = []
    
    avg_mpyc_times = []
    avg_psi_gcs_times = []
    avg_psi_raw_times = []
    avg_psi_bloom_times = []
    
    for length in lengths:
        for i in range(20):
            # randomly create the data each time
            print(f"Iteration {i+1} for length {length}")
            create_data(randomized=True, length=length)

            # run the methods
            mpyc_times.append(test_mpyc(verbose=False))
            psi_gcs_times.append(psi_computation('gcs'))
            psi_raw_times.append(psi_computation('raw'))
            psi_bloom_times.append(psi_computation('bloom'))
        
        # average the times for each method
        avg_mpyc_times.append((length, sum(mpyc_times) / len(mpyc_times)))
        avg_psi_gcs_times.append((length, sum(psi_gcs_times) / len(psi_gcs_times)))
        avg_psi_raw_times.append((length, sum(psi_raw_times) / len(psi_raw_times)))
        avg_psi_bloom_times.append((length, sum(psi_bloom_times) / len(psi_bloom_times)))
    
    # graph
    plot_times(avg_mpyc_times, 'MPyC')
    plot_times(avg_psi_gcs_times, 'PSI GCS')
    plot_times(avg_psi_raw_times, 'PSI Raw')
    plot_times(avg_psi_bloom_times, 'PSI Bloom')
    plt.legend()
    plt.savefig(f'computation_time.png')


if __name__ == "__main__":
    # Run the main function within the asyncio event loop
    main()