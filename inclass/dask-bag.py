import hashlib
import dask.bag as db

# load in puzzle 
puzzle = open("PUZZLE-EASY", "r").readlines()
p = [puz.strip() for puz in puzzle]
pset = set(p)


wordlist = ["The", "the", "of", "Of", "and", "And"]
N = 100000


tgts = range(N)

def check_hash(i):
    key = "{:04d}".format(i)
    for word in wordlist:
        hash = hashlib.md5(key.encode("utf-8") + word.encode("utf-8")).hexdigest()
        if hash in pset:
            return (hash, key, word)
    return None

# if __name__ == "__main__":
def main():
    # Create a Dask bag from the target range
    bag = db.from_sequence(tgts, npartitions=1)  # Adjust npartitions for your system
    results = bag.map(check_hash).filter(lambda x: x is not None).compute()

    # Print results
    for result in results:
        print(result)


