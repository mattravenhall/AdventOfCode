latest = 0
states = [latest]
n = 0
sequence = [line.strip() for line in open('input.txt')]

while states.count(latest) != 2:
    latest = eval(str(latest) + sequence[n])
    states.append(latest)
    n += 1
    if n >= len(sequence):
        n = 0
print(latest)

