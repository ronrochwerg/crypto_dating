from flask import Flask, request
import subprocess
import threading
import time
import json
import private_set_intersection.python as psi

app = Flask(__name__)

def load_json_file(filename):
    """Load JSON data from a file and return as a dictionary."""
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

@app.route('/match_user_mpyc', methods=['POST'])
def compute():
    """Runs the secure computation as Party 0 and returns the result."""
    size = request.form.get('size')
    target_user = request.form.get('target_user')
    verbose = request.form.get('verbose')

    def mpyc_task(size, target_user, verbose):
        # time.sleep(1)
        print(f"Running MPyC computation for size {size} and target user {target_user}")
        if target_user is not None:
            time.sleep(0.1)
            data = load_json_file('server_data_mpyc.json')
            target_user_data = data[size][target_user]
            
            
            if verbose != "False":
                array = target_user_data[0]
                threshold = target_user_data[1]
                print(f"My array is: {array}")
                print(f"My threshold is: {threshold}")
                result = subprocess.run(
                ["python3", "mpyc_test.py", repr(target_user_data[0]), repr(target_user_data[1]), repr(verbose), "-M2", "-I1"],
                capture_output=True, text=True
                )
                print(f"Secure dot product result:\n {result.stdout.strip()}")
            else:
                result = subprocess.run(
                ["python3", "mpyc_test.py", repr(target_user_data[0]), repr(target_user_data[1]), repr(verbose), "-M3", "-I1", "--no-log"],
                capture_output=True, text=True
                )
        else:
            if verbose != "False":
                result = subprocess.run(
                ["python3", "mpyc_test.py", repr(None), repr(None), repr(verbose), "-M3", "-I2"],
                capture_output=True, text=True
                )
                print(f"Secure dot product result:\n {result.stdout.strip()}")
            else:
                result = subprocess.run(
                ["python3", "mpyc_test.py", repr(None), repr(None), repr(verbose), "-M3", "-I2", "--no-log"],
                capture_output=True, text=True
                )
        
    thread1 = threading.Thread(target=mpyc_task, args=(size, target_user, verbose))
    # thread2 = threading.Thread(target=mpyc_task, args=(None, None, verbose))
    thread1.start()
    # thread2.start()
    return {"message": "Accepted"}, 202

# Setup psi class to hold server key created at every match
class psikey(object):
    def __init__(self):
        self.key = None
        self.user_id = None

    def set_user_id(self, user_id):
        self.user_id = user_id
        return self.user_id
    
    def get_user_id(self):
        return self.user_id
    
    def set_key(self, newkey):
        self.key = newkey
        return self.key

    def get_key(self):
        return self.key

pkey = psikey()    
fpr = 0.01
num_client_inputs = 100
# In response to POST to /match, generate new key and encrypt payload elements and return

@app.route('/match_user_psi', methods=['POST'])
def match():
    user_id = request.form.get('user_id')
    pkey.set_user_id(user_id)
    s =  pkey.set_key(psi.server.CreateWithNewKey(reveal_intersection=False))
    
    data = request.files.get('data').read()
    psirequest = psi.Request()
    psirequest.ParseFromString(data)
    return s.ProcessRequest(psirequest).SerializeToString()

# Return the setup using current key. This means re-encrypting whole data set at every ask and returning either raw or compressed (gcs or bloom) to client.

@app.route('/gcssetup', methods=['GET'])
def gcssetup():
    s = pkey.get_key()
    user_id = pkey.get_user_id()
    data = load_json_file('server_data_psi.json')
    user_data = data[user_id][0]
    return s.CreateSetupMessage(fpr, num_client_inputs, user_data, psi.DataStructure.GCS).SerializeToString()

@app.route('/rawsetup', methods=['GET'])
def rawsetup():
    s = pkey.get_key()
    user_id = pkey.get_user_id()
    data = load_json_file('server_data_psi.json')
    user_data = data[user_id][0]
    return s.CreateSetupMessage(fpr, num_client_inputs, user_data, psi.DataStructure.RAW).SerializeToString()

@app.route('/bloomsetup', methods=['GET'])
def bloomsetup():
    s = pkey.get_key()
    user_id = pkey.get_user_id()
    data = load_json_file('server_data_psi.json')
    user_data = data[user_id][0]
    return s.CreateSetupMessage(fpr, num_client_inputs, user_data, psi.DataStructure.BLOOM_FILTER).SerializeToString()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)