import argparse
import csv
import math
import os
import random
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path


def count_inside(task):
    index, n, seed = task
    rng = random.Random(seed + index)
    inside = 0
    for _ in range(n):
        x, y = rng.random(), rng.random()
        if x*x + y*y <= 1:
            inside += 1
    return inside


def main():
    parser = argparse.ArgumentParser(description='Benchmark sequential vs parallel CPU')
    parser.add_argument('--samples', type=int, default=2000000)
    parser.add_argument('--workers', type=int, default=min(4, os.cpu_count() or 1))
    parser.add_argument('--chunks', type=int, default=16)
    parser.add_argument('--seed', type=int, default=2026)
    args = parser.parse_args()
    if min(args.samples, args.workers, args.chunks) <= 0 or args.chunks > args.samples:
        parser.error('samples/workers/chunks must be positive and chunks <= samples')
    base, remainder = divmod(args.samples, args.chunks)
    tasks = [(i, base + (i < remainder), args.seed) for i in range(args.chunks)]

    start = time.perf_counter()
    seq = sum(map(count_inside, tasks))
    sequential_time = time.perf_counter() - start

    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        parallel = sum(pool.map(count_inside, tasks))
    parallel_time = time.perf_counter() - start
    assert seq == parallel, 'Different input results!'

    pi_estimate = 4 * seq / args.samples
    speedup = sequential_time / parallel_time if parallel_time else float('inf')
    efficiency = 100 * speedup / args.workers
    print(f'Samples: {args.samples:,} | workers: {args.workers} | chunks: {args.chunks}')
    print(f'Pi estimate: {pi_estimate:.8f} | absolute error: {abs(pi_estimate-math.pi):.8f}')
    print(f'Sequential: {sequential_time:.4f}s | parallel: {parallel_time:.4f}s')
    print(f'Speedup: {speedup:.2f}x | worker efficiency: {efficiency:.2f}%')
    if speedup < 1:
        print('Parallel was slower in this run: process overhead may contribute.')
    output = Path(__file__).resolve().parent / 'output'
    output.mkdir(exist_ok=True)
    with (output / 'hasil_benchmark.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['samples','workers','chunks','pi_estimate','absolute_error','sequential_seconds','parallel_seconds','speedup','efficiency_percent'])
        writer.writerow([args.samples,args.workers,args.chunks,pi_estimate,abs(pi_estimate-math.pi),sequential_time,parallel_time,speedup,efficiency])
    print('Saved:', output / 'hasil_benchmark.csv')


if __name__ == '__main__':
    main()
