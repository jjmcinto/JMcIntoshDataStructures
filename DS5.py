#use lists and binary search
from math import floor, ceil;
def fireLifeguard(strFilePath):
    #read data
    input = open(strFilePath, 'r');
    lines = input.readlines();
    segments = [];
    minLoneCoverage = float("inf");
    
    #if input is non-empty
    shiftCount = int(lines[0].strip());
    if shiftCount > 0:
        
        #assemble a timeline, tracking who is on solo duty at any given time
        segments = [[0, map(int, lines[1].strip().split(" "))]];
        for i in range(1, shiftCount):
            #read ith shift
            currShift = [i, map(int, lines[i+1].strip().split(" "))];
            
            #get range of indices of time segments affected
            toUpdate = getAffected(currShift, segments);
            
            #update timeline, showing solo and shared credit where appropriate
            segments = updateAffected(currShift, toUpdate, segments);
    
    #return maximum coverage possible after firing one worker
    coverageByAll, minSoloCoverage = summarizeSegments(segments, shiftCount);
    return coverageByAll - minSoloCoverage;

#binary search segments for leftmost or rightmost overlapping segment affected by currShift
def binarySearchSegments(segments, currShift, range, search):
    
    mid = 0;
    round = ceil; #search==1 => rightmost => 'ceil' function required
    iAdjust = 1 - 2 * search; #search==0 => +1; search==1 => -1
    if search == 0:
        round = floor; #search==0 => leftmost => 'floor' function required
    
    while range[0] < range[1]:
        
        #get mid-point of range
        mid = int(range[0] + round(float(range[1] - range[0])/float(2)));
        
        #if seeking leftmost and middle segment is on or right of currShift, then eliminate segments[mid+1] and up
        #if seeking rightmost and middle segment is on or left of currShift, then eliminate segments[mid-1] and down
        if iAdjust * segments[mid][1][1-search] > iAdjust * currShift[1][search]:
            range[1-search] = mid; #range: [0, 0]
        else: #eliminate the other half, as determined by parameter 'search'
            range[search] = mid + iAdjust;
            
    return range[search];
    
#employs binary search to find all time segments that overlap currShift
#returns list of integers, containing bounds of affected indices inclusive ([first, last])
def getAffected(currShift, segments):
    lenSegments = len(segments);
    r = [0, lenSegments-1];
    left = 0;
    right = lenSegments-1;
    mid = 0;
    
    #search for leftmost segment overlapped by currShift
    left = binarySearchSegments(segments, currShift, [left, right], 0);
    
    #if segments[left] is overlapped
    if segmentsOverlap(segments[left][1], currShift[1]):
        
        r[0] = left; #record leftmost segment overlapped by currShift
        right = binarySearchSegments(segments, currShift, [left, right], 1); #search for rightmost (as it must exist)
        r[1] = right; #record rightmost segment overlapped by currShift
        
    else: #nothing overlaps with currShift
        r[0] = -1; #indicate no segments are affected
        
        #indicate where to insert currShift in segments
        if currShift[1][1] < segments[left][1][1]:
            r[1] = left;
        else:
            r[1] = left + 1;
    
    #return pointers to affected segments or pointer to insertion position
    return r;
    
def segmentsOverlap(s1, s2):
    #return true iff
    #   left of s1 is in s2
    #   right of s1 is in s2
    #   s1 contains s2
    return s1[0] >= s2[0] and s1[0] < s2[1] or \
           s1[1] > s2[0] and s1[1] <= s2[1] or \
           s1[0] < s2[0] and s1[1] > s2[1];
    
#updates 'segments' at indices between those in 'toUpdate', inclusive
def updateAffected(currShift, toUpdate, segments):
    
    #if no overlap
    if toUpdate[0] == -1: #insert directly
        segments.insert(toUpdate[1], currShift);
        
    #if currShift contained by segments[toUpdate[0]] (and hence, affects only that segment)
    elif segments[toUpdate[0]][1][0] <= currShift[1][0] and currShift[1][1] <= segments[toUpdate[0]][1][1]:
        segments, toUpdate = applyMidShiftSegment(segments, currShift, toUpdate);
        
    else: #currShift overlaps segments[toUpdate[0]] but is not contained by it
    
        #handle first overlapping segment
        segments, i, toUpdate = handlePartlyCoveredFirstSegment(segments, currShift, toUpdate);
        
        #handle central segments
        while i <= toUpdate[1]:
            
            #if ith segment completely covered
            if segments[i][1][1] <= currShift[1][1]: #update the credit to 'shared'
                segments, i, toUpdate = handleCompletelyCoveredMidShiftSegment(segments, currShift, i, toUpdate);
                
            else: #not completely covered => last affected segment
                segments, i, toUpdate = handlePartlyCoveredLastSegment(segments, currShift, i, toUpdate);
            
            #move to next affected segment
            i += 1;
    
    #return updated list of segments
    return segments;

def handlePartlyCoveredLastSegment(segments, currShift, index, toUpdate):
    
    #if previous segment has shared credit
    if index > 0 and segments[index-1][0] == -1: #extend previous segment to end of currShift
        segments[index-1][1][1] = currShift[1][1];
    else: #new shared-credit segment
        segments.insert(index, [-1, [segments[index][1][0], currShift[1][1]]]);
        index += 1;
    segments[index][1][0] = currShift[1][1];
    
    return segments, index, toUpdate;

#update segments for the case where a segment is completely covered by currShift
def handleCompletelyCoveredMidShiftSegment(segments, currShift, index, toUpdate):
    
    #if previous segment has shared credit
    if index > 0 and segments[index-1][0] == -1:
        #extend previous segment over ith
        segments[index-1][1][1] = segments[index][1][1];
                
        #delete (index)th segment
        segments.pop(index);
        toUpdate[1] -= 1;
        index -= 1;
    else: #only share credit on ith segment
        segments[index][0] = -1;

    #if currShift goes past end of (index)th segment and ith is last overlapping or there is a gap between (index)th and (index+1)th
    if segments[index][1][1] < currShift[1][1] and (index==toUpdate[1] or (index < len(segments)-1 and segments[index][1][1] < segments[index+1][1][0])):
        
        #insert new segment
        segments.insert(index+1, [currShift[0], [segments[index][1][1], (segments[index+1][1][0] if index<toUpdate[1] else currShift[1][1])]]);
        index += 1;
        toUpdate[1] += 1;
    
    return segments, index, toUpdate;

#handle any portion of timeline left of the first segment completely covered by currShift
def handlePartlyCoveredFirstSegment(segments, currShift, toUpdate):
    
    #initialize counter
    index = toUpdate[0];
    
    #if there is left edge spillover
    if currShift[1][0] < segments[index][1][0]:
        #insert segment for left edge spillover
        segments.insert(toUpdate[0], [currShift[0],[currShift[1][0], segments[index][1][0]]]);
        index += 1;
        toUpdate[1] += 1; #the range to update just grew by one
        
    #if currShift starts within the first shift is affects
    elif segments[index][1][0] < currShift[1][0]:
        segments.insert(index+1, [-1, [currShift[1][0], segments[index][1][1]]]);
        segments[index][1][1] = currShift[1][0];
        index += 1;
        toUpdate[1] += 1; #the range to update just grew by one
    
    #else, currShift starts at the same point as the first shift, which is a case the loop can handle directly
    
    return segments, index, toUpdate;

#handle segment completely covered by currShift
def applyMidShiftSegment(segments, currShift, toUpdate):
    #if credit not already shared
    if segments[toUpdate[0]][0] > -1:
        if segments[toUpdate[0]][1][0] < currShift[1][0]: #where applicable, credit left side of segments[toUpdate[0]]
            segments.insert(toUpdate[0], [segments[toUpdate[0]][0],[segments[toUpdate[0]][1][0], currShift[1][0]]]);
            toUpdate[0] += 1;
            toUpdate[1] += 1;
        segments.insert(toUpdate[0], [-1,[currShift[1][0], currShift[1][1]]]); #insert overlapping section
        if currShift[1][1] < segments[toUpdate[0]+1][1][1]: #where applicable, credit right side of segments[toUpdate[0]]
            segments[toUpdate[0]+1][1][0] = currShift[1][1];
        else: #nothing on right side; remove right side of segments[toUpdate[0]]
            segments.pop(toUpdate[0]+1);
    
    return segments, toUpdate;

#adds up time covered by all workers before firing
#finds coverage by worker with least solo coverage time
def summarizeSegments(segments, shiftCount):

    #initialize all solo coverage segments to zero
    d = {};
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
        coverageByAll += d[i];

    #return
    return coverageByAll, minSoloCoverage;
    
#for each input file
for i in range(1,11):
    #print(i, fireLifeguard('input/' + str(i) + '.in'));
    #record corresponding output
    f = open("output/" + str(i) + ".out", "w");
    f.write(str(fireLifeguard('input/' + str(i) + '.in')));
    f.close();
