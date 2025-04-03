import requests
import private_set_intersection.python as psi
from pandas import read_csv

import random
import private_set_intersection.python as psi

# Generate random names
def generate_names(num):
    return [f"Name{random.randint(1, 100)}" for _ in range(num)]

# Client and server datasets
client_data = generate_names(5)
server_data = client_data[:3] + generate_names(5)  # Ensuring an intersection

# 1. Server Initialization
server = psi.server.CreateWithNewKey(reveal_intersection=True)

# 2. Server Setup Phase
num_client_inputs = len(client_data)
setup_message = server.CreateSetupMessage(fpr=0.3, num_client_inputs=100, inputs=server_data, ds=psi.DataStructure.GCS)

# 3. Client Initialization
client = psi.client.CreateWithNewKey(reveal_intersection=True)

# 4. Client Creates Request
request = client.CreateRequest(client_data)

# 5. Server Processes the Request
response = server.ProcessRequest(request)

# 6. Client Computes Intersection
intersection_indices = client.GetIntersection(setup_message, response)
print("Intersection Indices:", intersection_indices)
intersection = [client_data[i] for i in intersection_indices]
print("Client Data:", client_data)
print("Server Data:", server_data)
print("Intersection:", intersection)

