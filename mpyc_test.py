import sys
import asyncio
import ast  # To safely parse the input array
from mpyc.runtime import mpc

async def main(input_array, threshold, verbose):
    # wait for other users to connect
    await mpc.start()
    
    # setup for 3 party computation (who will be sending and recieving data)
    m = len(mpc.parties)
    t = m//2
    matchers = list(range(t+1))
    secint = mpc.SecInt() # Secure integer type
    
    # if you are a participant setting up the two variables to send 
    if mpc.pid in matchers:
        # Parse input vector
        x = ast.literal_eval(input_array)
        t = int(threshold)
    else:
        # Dummy values for non-matchers
        x = [None]
        t = None
    
    # Securely input the vector and threshold
    arrays = mpc.input([secint(xi) for xi in x], senders=matchers)
    thresholds = mpc.input(secint(t), senders=matchers)
    
    if verbose != 'False':
        # calculate the result and output 
        result = await mpc.output(mpc.sum([mpc.eq(arrays[0][i], arrays[1][i]) for i in range(len(arrays[0]))]) >= mpc.max(thresholds), receivers=matchers)
        print(f"\nMy array shares are:")
        [print(f"{arrays[i]}\n") for i in range(len(arrays))]
        print(f"My threshold shares are:\n{thresholds}\n")
        common = await mpc.output(mpc.sum([mpc.eq(arrays[0][i], arrays[1][i]) for i in range(len(arrays[0]))]))
        print(f"Number of common elements: {common}")
        print(f"The result: {'Match' if result else 'No Match'}")
        await mpc.shutdown()   
    else:
        # just calculate the result
        await mpc.run(mpc.output(mpc.sum([mpc.eq(arrays[0][i], arrays[1][i]) for i in range(len(arrays[0]))]) >= mpc.max(thresholds), receivers=matchers))
        
        await mpc.shutdown()
        

if __name__ == "__main__":
    input_array = sys.argv[1]  # First argument is the input array
    threshold = sys.argv[2]  # Second argument is the threshold
    verbose = sys.argv[3]  # Third argument is the verbosity flag
    # Run MPyC with given arguments
    mpc.run(main(input_array, threshold, verbose))