import hashlib
import time

def hash_data(data, hash_func):
    start_time = time.time()
    hashed_data = hash_func(data.encode()).hexdigest()
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000  # konwersja na milisekundy
    return hashed_data, time_taken

def main():
    data = input("Podaj dane do zahaszowania: ")

    algorithms = hashlib.algorithms_guaranteed
    print(algorithms)
    for algorithm in algorithms:
        print(f"Hashowanie za pomocą {algorithm}:")
        try:
            hash_func = getattr(hashlib, algorithm)
            print(hash_func)
            hashed_data, time_taken = hash_data(data, hash_func)
            print(f"Wynik haszowania: {hashed_data}")
            print(f"Czas haszowania: {time_taken:.6f} milisekund\n")  # Wyświetlenie czasu z dokładnością do mikrosekund
        except AttributeError:
            print(f"{algorithm} nie jest dostępną funkcją haszującą w hashlib.\n")

if __name__ == "__main__":
    main()
