import argparse
import hashlib
import string
import timeit
import plotly.graph_objs as go
import random
from statistics import median

def hash_data(data):
    """
    Calculate hashes of the provided data using various hash algorithms available in hashlib.

    Args:
        data (str): The data to be hashed.

    Returns:
        dict: A dictionary containing pairs of hash algorithms and their corresponding hash values and execution times.
              Each key is the name of the hash algorithm (str), and its value is a list containing two elements:
              - Hashed data (str): The resulting hash value of the provided data.
              - Execution time (float): The time taken to compute the hash.
    """
    hashes = {}
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
            hashes[algorithm] = [hashed_data, execution_time]
        except AttributeError:
            hashes[algorithm] = [f"{algorithm} is not an available hash function in hashlib.", 0]
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


def aggregate_hash_data(data, num_iterations):
    """
    Aggregate hash data by calling the hash_data function a specified number of times.

    Args:
        data (str): The data to be hashed.
        num_iterations (int): The number of times to call the hash_data function.

    Returns:
        dict: A dictionary containing aggregated execution times for each hash algorithm.
              Each key is the name of the hash algorithm (str), and its value is a list of execution times (float).
    """
    aggregated_times = {}
    for _ in range(num_iterations):
        hash_results = hash_data(data)
        for algorithm, (hashed_data, execution_time) in hash_results.items():
            if algorithm not in aggregated_times:
                aggregated_times[algorithm] = []
            aggregated_times[algorithm].append(execution_time)
    return aggregated_times


def visualize_hash_performance(word_max_length=100, iterations=100):
    """
    Visualize the performance of hashing algorithms for varying data lengths.

    Args:
        word_max_length (int): The maximum length of the random data to be hashed.
        iterations (int): The number of iterations to aggregate hash performance.

    Returns:
        None
    """
    my_dict = {}
    characters = string.ascii_letters + string.digits
    for data_length in range(word_max_length):
        text = ''.join(random.choice(characters) for _ in range(data_length))
        aggregated_times = aggregate_hash_data(text, iterations)
        my_dict[data_length] = {hash_name: median(hash_times) for hash_name, hash_times in aggregated_times.items()}

    hashes = list(my_dict[1].keys())

    # Tworzenie średnich czasów dla każdego hasha
    hash_avg_times = {hash_name: [] for hash_name in hashes}
    for word_length, dict_inside in my_dict.items():
        for hash_name, hash_values in dict_inside.items():
            hash_avg_times[hash_name].append(hash_values)


    # Tworzenie wykresu
    fig = go.Figure()
    for hash_name, times in hash_avg_times.items():
        fig.add_trace(go.Scatter(x=list(my_dict.keys()), y=times, mode='lines', name=hash_name))

    fig.update_layout(
        title='Średni czas dla różnych hashy w zależności od klucza',
        xaxis=dict(title='Klucz w słowniku'),
        yaxis=dict(title='Średni czas')
    )
    fig.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate hashes of data or files and visualize the performance of hashing algorithms.")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    hash_data_parser = subparsers.add_parser('hash_data', help='Calculate hashes of provided data')
    hash_data_parser.add_argument('data', type=str, help='The data to be hashed')

    hash_file_parser = subparsers.add_parser('hash_file', help='Calculate hash of specified file')
    hash_file_parser.add_argument('file_path', type=str, help='The path to the binary file')

    visualize_parser = subparsers.add_parser('visualize', help='Visualize the performance of hashing algorithms')
    visualize_parser.add_argument('--word_max_length', type=int, default=100, help='Maximum length of random data to be hashed')
    visualize_parser.add_argument('--iterations', type=int, default=100, help='Number of iterations to aggregate hash performance')

    args = parser.parse_args()

    if args.command == 'hash_data':
        result = hash_data(args.data)
        print(result)
    elif args.command == 'hash_file':
        result = hash_file(args.file_path)
        print(result)
    elif args.command == 'visualize':
        visualize_hash_performance(word_max_length=args.word_max_length, iterations=args.iterations)