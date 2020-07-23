#try storing each shift as a number, representing coverage of nth time unit as:
# 2^n
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
    coverageByAll = 0;
    minSoloCoverage = float("inf");
    
    #for each lifeguard
    shiftCount = int(lines[0].strip());
    for i in range(0, shiftCount):
        #append ith shift to list of all shifts
        allShifts.append(map(int, lines[i+1].strip().split(" ")));
        allShifts[i] = getInteger(allShifts[i][0], allShifts[i][1]);
        print("getInteger:", map(int, lines[i+1].strip().split(" ")), allShifts[i]);
        
        #append solo coverage
        soloCoverage.append(allShifts[i] & (allShifts[i] ^ coverageByAll));
        
        #update pre-firing coverage
        coverageByAll |= allShifts[i];
        
        #update solo coverage
        for j in range(0, i):
            soloCoverage[j] = soloCoverage[j] - (soloCoverage[j] & allShifts[i]);
            
    #determine minimum coverage loss incurred by firing someone
    for i in range(0, shiftCount):
        minSoloCoverage = min(minSoloCoverage, bin(soloCoverage[i])[2:].count('1'));
    
    #return duration covered by all lifeguards, less minimum solo portion
    return bin(coverageByAll)[2:].count('1') - minSoloCoverage;

#convert start and end points to an array of bits
#nth bit = 1 iff lifeguard is on duty between time n and n+1
def getInteger(start, end):
    r = 0;
    print("getInteger: ", start, end);
    add = pow(2, start-1);
    for i in range(start, end):
        add *= 2;
        r += add;
        
    return r;

#print(fireLifeguard('input/JM.in'));
#for i in [1]:
for i in [2]:
#for i in [1,2,3,4,5,6,7,8,9,10]:
    print("i:", i);
    print(fireLifeguard('input/' + str(i) + '.in'));

