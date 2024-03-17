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


def hash_file(file_path):
    """
    Calculate the hash of the specified binary file using SHA-256 algorithm.

    Args:
        file_path (str): The path to the binary file.

    Returns:
        str: The SHA-256 hash value of the file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    try:
        with open(file_path, "rb") as file:
            file_data = file.read()
            hash_value = hashlib.sha256(file_data).hexdigest()
            return hash_value
    except FileNotFoundError:
        raise FileNotFoundError(f"The specified file '{file_path}' does not exist.")


def main():
    data = input("Podaj dane do zahaszowania: ")
    x = hash_data(data)
    print(x)

    file_path = r"C:\Users\patpi\ubuntu-23.10.1-desktop-amd64.iso"
    hashed_value = hash_file(file_path)
    print("Hash value:", hashed_value)

if __name__ == "__main__":
    main()
