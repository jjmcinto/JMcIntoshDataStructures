#use lists and binary search
#3
#5 9
#1 4
#3 7
def fireLifeguard(strFilePath):
    #read data
    input = open(strFilePath, 'r');
    lines = input.readlines();
    segments = [];
    minLoneCoverage = float("inf");
    
    shiftCount = int(lines[0].strip());
    if shiftCount > 0:
        segments = [0, map(int, lines[1].strip().split(" "))];
        for i in range(1, shiftCount):
            #read ith shift
            currShift = [i, map(int, lines[i+1].strip().split(" "))];
            
            #get range of indices of time segments affected
            toUpdate = getAffected(currShift, segments);
            
            #update segments acordingly
            segments = updateAffected(currShift, toUpdate, segments);
            
    coverageByAll, minSoloCoverage = summarizeSegments(segments, shiftCount);
    return coverageByAll - minSoloCoverage;

#employs binary search to find all time segments that overlap currShift
#returns list of integers, containing affected indices [first and last+1]
def getAffected(currShift, segments):
    lenSegments = len(segments);
    r = [0, lenSegments-1];
    left = 0;
    right = lenSegments-1;
    mid = 0;
    
    #if some segments end before currShift starts
    if segments[0][1] < currShift[0]: #find segment just left of currShift
        while right > left+1:
            mid = left + (right - left)/2;
            #if segments[mid] is on or right of currShift
            if segments[mid][1] > currShift[0]:
                right = mid;
            #if segments[mid+1] is not on or right of currShift
            elif segments[mid+1][1] < currShift[0]:
                left = mid;
            else: #segments[mid] is left of currShift and segments[mid+1][1] is on or right of currShift
                left = mid;
                right = mid+1;
        r[0] = right;
    
    left = 0;
    right = lenSegments - 1;
    #if some segments begin after currShift ends
    if segments[right][0] > currShift[1]: #find segment just right of currShift
        while right > left+1:
            mid = left + (right - left)/2;
            #if segments[mid] is on or left of currShift
            if segments[mid][0] < currShift[1]:
                left = mid;
            #if segments[mid-1] is not on or left of currShift
            elif segments[mid-1][0] > currShift[1]:
                right = mid;
            else: #segments[mid] is right of currShift and segments[mid-1][0] is on or left of currShift
                left = mid;
                right = mid+1;
        r[1] = left;
    
    return r;
    
#updates 'segments' at indices between those in 'toUpdate'
def updateAffected(currShift, toUpdate, segments):
    #indices at ends may only partly overlap
    #indices in middle are duplicates and have contributor ID updated to '-1'
    #if adjacent segments have contributor ID of '-1', then combine
    
    #handle edge segments
    
    #handle central segments
    for i in range(toUpdate[0]+1, toUpdate[1]-1)
        
        
    return segments;

#maps each worker ID to sum of solo work time
#also adds up time covered by all workers before firing
def summarizeSegments(segments, shiftCount):
    d = {};
    #initialize all solo coverage segments to zero
    for i in range(-1, shiftCount):
        d[i] = 0;
    
    #get solo totals for each lifeguard (and redundant coverage)
    for s in segments:
        d[s[0]] += s[1][1] - s[1][0];
    
    #find:
    #   amount of time covered by all lifeguards currently employed
    #   minimum amount of coverage we can lose by firing one lifeguard
    coverageByAll = d[-1];
    minSoloCoverage = float("inf");
    for i in range(0, shiftCount):
        minSoloCoverage = min(minSoloCoverage, d[i]);
        coverageByAll += d[key];
    
    #return
    return coverageByAll, minSoloCoverage;

#print(fireLifeguard('input/JM.in'));
for i in [1,2,3,4,5,6,7,8,9,10]:
    print(fireLifeguard('input/' + str(i) + '.in'));
