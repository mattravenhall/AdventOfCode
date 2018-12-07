import numpy as np

n_workers = 5
infile = 'input.txt'
shift = 60

# Read input file, convert to edge tuples
edges = np.array([(x.split(' ')[1], x.split(' ')[7]) for x in open(infile)])

# Define features
timeTaken = lambda t: shift + ord(t) - 64
jobs = list(set(edges.flatten()))
jobs.sort()

def runJobs(jobs, edges, n_workers=n_workers):
	time = 0
	workers = {}
	freeJobs = []
	finishedJobs = []
	done = 0

	while len(finishedJobs) < len(jobs):

		# Possible jobs are those not waiting on another
		try:
			freeJobs = list(set(edges[:,0]) - set(edges[:,1]))
			freeJobs = list(set(freeJobs) - set(list(workers.keys())))
			freeJobs.sort()
		except:
			# Catch childless jobs
			freeJobs = list(set(jobs) - set(finishedJobs))

		# Assign jobs to workers from freeJobs alphabetically, if we have space
		while len(workers) < n_workers and len(jobs) > 0 and len(freeJobs) > 0:
			workers[freeJobs[0]] = timeTaken(freeJobs[0])
			freeJobs.remove(freeJobs[0])

		# Extend time to the end of next finished job/s
		lowestTime = min(workers.values())
		time += lowestTime

		# Any workers with lowest time to finishedJobs list
		finishedJobs.extend([i for i in workers if workers[i] == lowestTime])

		# Update worker times, remove those <= 0
		workers = {w: t-min(workers.values()) for w, t in workers.items() if t-min(workers.values()) >= 1}

		# Update the excluded jobs list to include current workers
		excludedJobs = set(finishedJobs) | set(workers.keys())

		# Remove edges with finished jobs as parents
		edges = np.array([list(e) for e in edges if e[0] not in finishedJobs])
	return(time)

print(runJobs(jobs, edges))