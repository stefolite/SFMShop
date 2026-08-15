import multiprocessing


def worker(x):
    print(f'worker {x} started working')
    for _ in range(10**9):
        continue
    return True


if __name__ == '__main__':
    with multiprocessing.Pool() as pool:
        pool.map(worker, [1, 2])
        print('Done')
