import hashlib
from concurrent.futures import ProcessPoolExecutor

# Sample variables for demonstration
wordlist = ["the"]
N = 1000000000
tgts = range(N)  # Adjust range based on your requirements
pset = set()  # Replace with your actual hash set



def check_hash(i):
    key = "{:09d}".format(i)
    for word in wordlist:
        hash = hashlib.md5(key.encode("utf-8") + word.encode("utf-8")).hexdigest()
        if hash in pset:
            return (hash, key, word)
    return None

# Parallel execution
if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        results = executor.map(check_hash, tgts)
        
        # Process results
        for result in results:
            if result:
                print(result)

