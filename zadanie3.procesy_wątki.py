# pierwsza część dotycząca wątków
import os
import shutil
from threading import Thread

def sort_files_by_extension(source_folder):
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            source_path = os.path.join(root, file)
            extension = os.path.splitext(file)[1][1:]
            destination_folder = os.path.join(source_folder, extension)
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)
            shutil.move(source_path, destination_folder)

def parallel_sort(source_folder, num_threads):
    threads = []
    for _ in range(num_threads):
        thread = Thread(target=sort_files_by_extension, args=(source_folder,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

source_folder = "Bałagan"
num_threads = 4 
parallel_sort(source_folder, num_threads)


# druga część dotycząca procesów
import time
import multiprocessing

def factorize_sync(numbers):
    results = []
    for num in numbers:
        factors = [i for i in range(1, num+1) if num % i == 0]
        results.append(factors)
    return results

def factorize_parallel(numbers):
    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_processes)
    results = pool.map(factorize_sync, [numbers])
    pool.close()
    pool.join()
    return results


start_time_sync = time.time()
numbers = [9999999, 8888888, 7777777, 6666666, 5555555]  
results_sync = factorize_sync(numbers)
end_time_sync = time.time()
print("Synchronous execution time:", end_time_sync - start_time_sync)
print("Synchronous results:", results_sync)


start_time_parallel = time.time()
results_parallel = factorize_parallel(numbers)
end_time_parallel = time.time()
print("Parallel execution time:", end_time_parallel - start_time_parallel)
print("Parallel results:", results_parallel)