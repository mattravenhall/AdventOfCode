#!/usr/bin/env python3

from collections import defaultdict

seeds_pre, seeds_post = [], []

for line in open("input.txt").readlines():
    # Grab seeds of interest
    if line.startswith("seeds: "):
        seeds_pre = list(map(int, line.split()[1:]))
        continue

    # Skip map names
    elif line.endswith("map:\n"):
        continue
 
    # Process a map once it's collected
    elif line == "\n":
        seeds_pre = seeds_pre + seeds_post
        seeds_post = []

    # Process each mapping
    else:
        destination_range_start, source_range_start, range_length = map(int, line.split())

        seeds_holder = []

        # Process unmapped seeds
        for _ in range(len(seeds_pre)):
            seed = seeds_pre.pop()
            if source_range_start <= seed <= (source_range_start+range_length):
                seeds_post.append(seed - source_range_start + destination_range_start)
            else:
                seeds_holder.append(seed)

        seeds_pre = seeds_holder

# Print the lowest location number that corresponds to any of the initial seeds
print(min(seeds_pre + seeds_post))
