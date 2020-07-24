#use dictionaries
# - fast enough for first four inputs
# - ran for two hours and crashed on 5.in:
#Traceback (most recent call last):
#  File "DS2.py", line 48, in <module>
#    print(fireLifeguard('input/' + str(i) + '.in'));
#  File "DS2.py", line 34, in fireLifeguard
#    soloCoverage[dShifts[j]] -= 1;
#IndexError: list index out of range
#1.in: 7
#2.in: 3954114
#3.in: 40284653
#4.in: 41030168

#3
#5 9
#1 4
#3 7
def fireLifeguard(strFilePath):
    #read data
    input = open(strFilePath, 'r');
    lines = input.readlines();
    allShifts = [];
    soloCoverage = [];
    dShifts = {};
    coverageByAll = 0;
    boolCoverageLossPossible = True;
    minLoneCoverage = float("inf");
    
    #for each lifeguard
    shiftCount = int(lines[0].strip());
    for i in range(0, shiftCount):
        #append ith shift to list of all shifts
        allShifts.append(map(int, lines[i+1].strip().split(" ")));
        
        #initialize solo coverage for ith worker
        soloCoverage.append(allShifts[i][1] - allShifts[i][0]);
        
        #for each unit of time covered by ith shift
        for j in range(allShifts[i][0], allShifts[i][1]):
            #if unit of time not yet covered
            if j not in dShifts: #map time to i
                dShifts[j] = i;
            else: #overlap detected
                #if first overlap at this point
                if dShifts[j] > -1:
                    #reduce solo coverage for first worker to cover this unit of time
                    soloCoverage[dShifts[j]] -= 1;
                    
                    #remove mapping; only indicate this unit of time is covered
                    dShifts[j] = -1;
                    
                #reduce solo coverage for ith worker
                soloCoverage[i] -= 1;
    
    #return duration covered by all lifeguards, less minimum solo portion
    return len(dShifts.keys()) - min(soloCoverage);

#print(fireLifeguard('input/JM.in'));
#for i in [1, 2, 3, 4]:
for i in [1,5,6,7,8,9,10]:
#for i in [1,2,3,4,5,6,7,8,9,10]:
    print("i:", i);
    r = fireLifeguard('input/' + str(i) + '.in');
    f = open("output/ubuntu" + str(i) + ".out", "w");
    f.write(str(r));
    f.close();
    print("r:", r);
