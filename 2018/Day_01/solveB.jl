latest = 0
states = [latest]
n = 1
sequence = [line for line in readlines(open("input.txt"))]

while count(x->x==latest, states) != 2
	global latest = eval(Meta.parse(string(latest,sequence[n])))
	append!(states, latest)
	global n += 1
	if n > length(sequence)
		global n = 1
	end
end

println(latest)
