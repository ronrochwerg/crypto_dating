# import mpyc
# from mpyc.runtime import mpc

# async def main():
#     # Initialize the MPyC runtime
#     await mpc.start()

#     # Define the secure binary field (GF(2))
#     secbool = mpc.SecInt()

#     # Each party inputs their binary vector
#     if mpc.pid == 0:
#         x = [1, 1, 1, 1]  # Party 0's binary vector
#     else:
#         x = [1, 1, 1, 1]

#     arrays = mpc.input([secbool(xi) for xi in x])

#     # Reveal the result to all parties
#     result = await mpc.output(mpc.in_prod(arrays[0], arrays[1]))
#     if mpc.pid == 0:
#         print(f"Secure dot product result: {result}")

#     # Stop the MPyC runtime
#     await mpc.shutdown()
# if __name__ == "__main__":

#     # Run the main function within the MPyC event loop
#     mpc.run(main())

# import requests
# import asyncio
# from mpyc.runtime import mpc

# # Send request to server
# response = requests.get("http://localhost:5000/compute")

# # If the server is ready, run MPyC as Party 1
# if response.status_code == 200:
#     print("Server is ready. Running MPyC computation...")
# else:
#     print("Error: Server is not ready.")
#     exit()

# async def main():
#     """Secure computation for Party 1."""
#     await mpc.start()

#     secbool = mpc.SecInt()

#     # Party 1 inputs this vector
#     x = [0, 1, 1, 1]  

#     # Securely input the vector
#     arrays = mpc.input([secbool(xi) for xi in x])
#     arrays = await mpc.gather(arrays)
#     print(arrays)
#     print(mpc.pid)
#     print(await mpc.output(arrays))
#     # Compute secure dot product
#     result = await mpc.output(mpc.in_prod(arrays[0], arrays[1]))

#     await mpc.shutdown()
#     print(f"Secure dot product result: {result}")

# mpc.run(main())

import sys
import asyncio
import ast  # To safely parse the input array
from mpyc.runtime import mpc

async def main(input_array, threshold, verbose):
    """Run the secure dot product computation with the given input array."""
    await mpc.start()
    secint = mpc.SecInt()

    # Parse input vector
    x = ast.literal_eval(input_array)
    t = int(threshold)
    
    # Securely input the vector
    arrays = mpc.input([secint(xi) for xi in x])
    thresholds = mpc.input(secint(t))

    # Compute secure dot product
    result = await mpc.output(mpc.in_prod(arrays[0], arrays[1]) >= mpc.max(thresholds))
    
    await mpc.shutdown()
    if verbose != 'False':
        dot_product = await mpc.output(mpc.in_prod(arrays[0], arrays[1]))
        plaintex_thresholds = await mpc.output(thresholds)

        # Print result so the caller can capture it
        print(plaintex_thresholds)
        print(dot_product)
        print(result)

if __name__ == "__main__":

    input_array = sys.argv[1]  # First argument is the input array
    threshold = sys.argv[2]  # Second argument is the threshold
    verbose = sys.argv[3]  # Third argument is the verbosity flag
    # Run MPyC with given arguments
    mpc.run(main(input_array, threshold, verbose))