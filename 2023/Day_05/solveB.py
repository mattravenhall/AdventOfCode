#!/usr/bin/env python3

from collections import defaultdict

seeds_pre, seeds_post = [], []

for line in open("input.txt").readlines():
    # Grab seeds of interest
    if line.startswith("seeds: "):
        values = list(map(int, line.split()[1:]))
        seeds_pre = [[values[i], values[i]+values[i+1]] for i in range(0, len(values), 2)]
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
        source_range_end = source_range_start + range_length

        seeds_holder = []

        # Process unmapped seeds
        for _ in range(len(seeds_pre)):
            seed_range = seeds_pre.pop()
            # Check if we overlap
            if (source_range_start < seed_range[1]) & (source_range_end > seed_range[0]):
                # Separate seed range parts that don't overlap
                if seed_range[0] < source_range_start:
                    seeds_holder.append([seed_range[0], source_range_start - 1])
                    seed_range[0] = source_range_start
                if seed_range[1] > source_range_end:
                    seeds_holder.append([seed_range[1], source_range_end + 1])
                    seed_range[1] = source_range_end
                seeds_post.append(
                    [
                        seed_range[0] - source_range_start + destination_range_start,
                        seed_range[1] - source_range_start + destination_range_start,
                    ]
                )
            else:
                seeds_holder.append(seed_range)

        seeds_pre = seeds_holder

# Print the lowest location number that corresponds to any of the initial seeds
print(min([pair[0] for pair in seeds_pre + seeds_post]))
