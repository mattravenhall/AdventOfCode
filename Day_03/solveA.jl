x = [line for line in readlines(open("example.txt"))]

function processID(line)
	return(split(replace(replace(strip(split(line, '@')[2]), ": " => ","), "x" => ","), ','))
end

Xgaps = []
Ygaps = []
Xwidths = []
Ywidths = []

for line in readlines(open("example.txt"))
	Xgap, Ygap, Xwidth, Ywidth = processID(line)
	append!(Xgaps, parse(Int, Xgap))
	append!(Ygaps, parse(Int, Ygap))
	append!(Xwidths, parse(Int, Xwidth))
	append!(Ywidths, parse(Int, Ywidth))
end

maxX = 1000
maxY = 1000

fabric = [[0 for y in range(1, length=maxX)] for x in range(1, length=maxY)]

for i in range(1, length=length(Xgaps))
	for x in range(Xgaps[i], length=Xgaps[i]+Xwidths[i])
		for y in range(Ygaps[i], length=Ygaps[i]+Ywidths[i])
			fabric[x][y] += 1
		end
	end
end

print(sum([sum([square >= 2 for square in line]) for line in fabric]), '\n')
