import hashlib
import timeit

def hash_data(data):
    """
    Calculate hashes of the provided data using various hash algorithms available in hashlib_algorithms_available.

    Args:
        data (str): The data to be hashed.

    Returns:
        list: A list containing pairs of hash values and their corresponding execution times.
              Each pair is represented as [hashed_data (str), execution_time (float)].

    Example:
        >>> hash_data("Hello, world!")
        [['2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824', 1.698142359],
         ['6dcd4ce23d88e2ee9568ba546c007c63d9131c1b250b8f5f2e4dc4c5c30f89dc', 1.349122872],
         ['f7ff9e8b7bb2e09b70935a5d785e0cc5d9d0abf0c54a7a0b2bdc59026a00781', 1.315445931],
         ...
         ['sha3_384 is not an available hash function in hashlib.', 0],
         ...]
    """
    hashes = []
    for algorithm in hashlib.algorithms_available:
        if algorithm.startswith('shake_'):  # There's no way to give the desired length in the placeholder
            continue
        try:
            hash_func = getattr(hashlib, algorithm)
            start_time = timeit.default_timer()
            hash_func().update(data.encode())
            hashed_data = hash_func(data.encode()).hexdigest()
            end_time = timeit.default_timer()
            execution_time = end_time - start_time
            hashes.append([hashed_data, execution_time])
        except AttributeError:
            hashes.append([f"{algorithm} is not an available hash function in hashlib.", 0])
    return hashes

def main():
    data = input("Podaj dane do zahaszowania: ")
    x = hash_data(data)
    print(x)

if __name__ == "__main__":
    main()
