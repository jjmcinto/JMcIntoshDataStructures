#try storing each time unit of each shift in a set
#3
#5 9 => 32 + 64 + 128 + 256
#1 4 => 2 + 4 + 8
#3 7 => 8 + 16 + 32 + 64
from math import pow;
def fireLifeguard(strFilePath):
    
    #read data
    input = open(strFilePath, 'r');
    lines = input.readlines();
    allShifts = [];
    soloCoverage = [];
    coverageByAll = set();
    minSoloCoverage = float("inf");
    
    #for each lifeguard
    shiftCount = int(lines[0].strip());
    for i in range(0, shiftCount):
        #append ith shift to list of all shifts
        allShifts.append(map(int, lines[i+1].strip().split(" ")));
        allShifts[i] = set(range(allShifts[i][0], allShifts[i][1]));
        
        #append solo coverage
        soloCoverage.append(allShifts[i].intersection(xOrSet(allShifts[i], coverageByAll)));
        
        #update pre-firing coverage
        coverageByAll = coverageByAll.union(allShifts[i]);
        
        #update solo coverage
        for j in range(0, i):
            soloCoverage[j] = soloCoverage[j] - (soloCoverage[j].intersection(allShifts[i]));
            
    #determine minimum coverage loss incurred by firing someone
    for i in range(0, shiftCount):
        minSoloCoverage = min(minSoloCoverage, len(soloCoverage[i]));
    
    #print("soloCoverage:", soloCoverage);
    
    #return duration covered by all lifeguards, less minimum solo portion
    return len(coverageByAll) - minSoloCoverage;

#return
def xOrSet(set1, set2):
    return (set1 - set2).union(set2 - set1);

#convert start and end points to an array of bits
#nth bit = 1 iff lifeguard is on duty between time n and n+1
def getInteger(start, end):
    r = 0;
    add = pow(2, start-1);
    for i in range(start, end):
        add *= 2;
        r += add;
        
    return r;

#print(fireLifeguard('input/JM.in'));
#for i in [1]: #started at 4:26pm - ended at 4:28pm
#for i in [5]: #started at 4:30pm - crashed by 5:30pm with "killed:9"
for i in [5,6,7,8,9,10]: #started at 5:34pm
#for i in [1,2,3,4,5,6,7,8,9,10]:
    print("i:", i);
    print(fireLifeguard('input/' + str(i) + '.in'));


