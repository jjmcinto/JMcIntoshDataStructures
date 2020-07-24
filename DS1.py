#use lists - way too slow
#3
#5 9
#1 4
#3 7
def fireLifeguard(strFilePath):
    #read data
    input = open(strFilePath, 'r');
    lines = input.readlines();
    allShifts = [];
    loneShifts = [];
    coverageByAll = 0;
    boolCoverageLossPossible = True;
    minLoneCoverage = float("inf");
    
    shiftCount = int(lines[0].strip());
    for i in range(0, shiftCount):
        #append ith shift to list of all shifts and solo segments
        allShifts.append(map(int, lines[i+1].strip().split(" ")));
        loneShifts.append([allShifts[i]]);
        
        #determine unique portion(s) of ith shift
        for j in range(0, i):
            loneShifts[i], loneShifts[j] = \
                getUniquePortionOfFirstPeriodList(loneShifts[i], loneShifts[j]), \
                getUniquePortionOfFirstPeriodList(loneShifts[j], loneShifts[i]);
        
	#print(i, loneShifts);
	
        #update minimum solo contribution; add solo coverage to coverageByAll
        currLoneCoverage = getCoverage(loneShifts[i]);
        minLoneCoverage = min(minLoneCoverage, currLoneCoverage);
	coverageByAll += currLoneCoverage;
        
    #print(allShifts);
    return coverageByAll - minLoneCoverage;
    
def getCoverage(periodList):
    
    #given a list of periods, return duration covered by all periods
    #print("getCoverage: ", [p[1]-p[0] for p in periodList])
    return sum([p[1]-p[0] for p in periodList])

def getUniquePortionOfFirstPeriodList(list1, list2):
    
    #prune list1 down to periods it covers that are not also covered by list2
    r = [];
    for p1 in list1:
        for p2 in list2:
            r += getUniquePortionOfFirst(p1, p2);
    
    return r;
    
def getUniquePortionOfFirst(in1, in2):
    
    prune = in1;
    compare = in2;
    r = [];
    #print("prune, compare", prune, compare);    
    #given two contiguous time segments, 'prune' and 'compare',
    #return segments of 'prune' that are not covered by 'compare'
    
    #if prune covers left end of compare
    if prune[0] <= compare[0] and compare[0] < prune[1]: #prune from left
        #if some of prune is to the left of compare
        if prune[0] < compare[0]: #keep that portion
            r.append([prune[0], compare[0]]);
        #if some of prune is to the right of compare
        if compare[1] < prune[1]: #keep that portion
            r.append([compare[1], prune[1]]);
    
    #if prune covers right end of compare
    elif prune[0] < compare[1] and compare[1] <= prune[1]: #prune from right
        #if some of prune is to the right of compare
        if compare[1] < prune[1]: #keep that portion
            r.append([compare[1], prune[1]]);
    
    #if prune and compare are completely disjoint
    elif not (compare[0] < prune[0] and prune[1] < compare[1]):
	r = [prune];
    
    #print('r', r);
    return r;

#print(fireLifeguard('input/JM.in'));            
for i in [5,6,7,8,9,10]:
#    print(fireLifeguard('input/' + str(i) + '.in'));
    print("i:", i);
    r = fireLifeguard('input/' + str(i) + '.in');
    f = open("output/ubuntu" + str(i) + ".out", "w");
    f.write(str(r));
    f.close();
    print("r:", r);
