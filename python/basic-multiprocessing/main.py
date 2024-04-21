import sys, time
sys.path.append("../../")
import multiprocessing as mp
from python.common import OUTPUT_PATH, MEASUREMENTS_PATH, Timer

def process_city_data(city_data, shared_map):
    """
    Processes city data and updates shared memory map.
    """
    for line in city_data:
        city_name, measurement = line.strip().split(";")
        measurement = int(measurement)
        with shared_map.get_lock():  # Acquire lock before modifying shared data
            if city_name in shared_map:
                data = shared_map[city_name]
                data["min"] = min(data["min"], measurement)
                data["max"] = max(data["max"], measurement)
                data["total"] += measurement
                data["count"] += 1
            else:
                shared_map[city_name] = {
                    "min": measurement,
                    "max": measurement,
                    "total": measurement,
                    "count": 1,
                }

def solution_parallel(path: str) -> str:
    """
    Processes city data in parallel using multiprocessing and shared memory.
    """
    with open(path, 'r') as f:
        data = f.readlines()

    # Create shared memory map for city data
    manager = mp.Manager()
    shared_map = manager.dict()

    # Determine number of processes based on CPU count
    num_processes = mp.cpu_count()

    # Split data into chunks for each process
    chunk_size = len(data) // num_processes
    data_chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    # Create processes and start processing
    processes = []
    for chunk in data_chunks:
        p = mp.Process(target=process_city_data, args=(chunk, shared_map))
        processes.append(p)
        p.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()

    # Build output string from shared map
    sorted_map = dict(sorted(shared_map.items()))
    bucket = ""
    for city_name, status in sorted_map.items():
        avg = int(status["total"] / status["count"])
        line = "{}={};{};{}({}/{})\n".format(city_name, status["min"],                       
                       status["max"], avg, status["total"], status["count"])
        bucket += line

    return bucket

def main():
    with open(OUTPUT_PATH, 'r') as f:
        expect_output = f.read()
    timer = Timer()
    got = solution_parallel(MEASUREMENTS_PATH)
    print(f"Elapsed: {timer.elapsed_as_milliseconds()}ms")
    assert expect_output == got

if __name__ == "__main__":
    main()