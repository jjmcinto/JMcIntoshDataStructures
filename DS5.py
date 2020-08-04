#use lists and binary search
#3
#5 9
#1 4
#3 7
from math import floor, ceil;
def fireLifeguard(strFilePath):
    #read data
    input = open(strFilePath, 'r');
    lines = input.readlines();
    segments = [];
    minLoneCoverage = float("inf");
    
    shiftCount = int(lines[0].strip());
    if shiftCount > 0:
        segments = [[0, map(int, lines[1].strip().split(" "))]];
        #print("segments:", segments);
        for i in range(1, shiftCount):
            #read ith shift
            currShift = [i, map(int, lines[i+1].strip().split(" "))];
            
            #get range of indices of time segments affected
            toUpdate = getAffected(currShift, segments);
            #print(currShift, "affects", toUpdate);
            
            #update segments acordingly
            segments = updateAffected(currShift, toUpdate, segments);
            #print("updated segments:", segments);
        #print("segments:", segments);
            
    coverageByAll, minSoloCoverage = summarizeSegments(segments, shiftCount);
    return coverageByAll - minSoloCoverage;

#employs binary search to find all time segments that overlap currShift
#returns list of integers, containing bounds of affected indices [first, last+1]
def getAffected(currShift, segments): #[1, [3,5]], [[0,[1,3]]]
    lenSegments = len(segments); #1
    r = [0, lenSegments-1];
    left = 0;
    right = lenSegments-1; #0
    mid = 0;
    
    #search for leftmost segment overlapped by currShift
    while left < right:
        mid = int(floor(left + (right - left)/2));
        #if segments[mid] is on or right of currShift
        if segments[mid][1][1] > currShift[1][0]: #then segments[mid+1] and up are not the leftmost
            right = mid;
        #if segments[mid] is left of currShift (not on or right)
        else: #segments[mid][1][1] <= currShift[1][0]
            left = mid+1;
    
    #if segments[left] (note that left==right) is overlapped
    if segmentsOverlap(segments[left][1], currShift[1]):
        r[0] = left;
    else: #nothing overlaps with currShift
        r[0] = -1; #indicate no segments are affected
        
        #indicate where to insert currShift
        if currShift[1][1] < segments[left][1][1]:
            r[1] = left;
        else:
            r[1] = left + 1;
    
    #if leftmost segment found
    if r[0] > -1: #search for rightmost (as it must exist)
        left = 0;
        right = lenSegments - 1;
        
        #search for rightmost segment overlapped by currShift
        while left < right:
            mid = left + int(ceil(float(right - left)/2));
            #if segments[mid] is on or left of currShift
            if segments[mid][1][0] < currShift[1][1]: #then segments[mid-1] and down are not the rightmost
                left = mid;
            #if segments[mid] is right of currShift (not on or left)
            else: #segments[mid][1][0] >= currShift[1][1]
                right = mid-1;
        
        #if segments[right] (note that left==right) is overlapped
        if segmentsOverlap(segments[right][1], currShift[1]):
            r[1] = right;
        elif segmentsOverlap(segments[left][1], currShift[1]):
            r[1] = left;
            right = left;
        else: #nothing overlaps with currShift
            r[0] = -1; #indicate no segments are affected
            
            #indicate where to insert currShift
            if currShift[1][1] < segments[right][1][1]:
                r[1] = right;
            else:
                r[1] = right + 1;
        
    return r;
    
def segmentsOverlap(s1, s2):
    #return true iff
    #   left of s1 is in s2
    #   right of s1 is in s2
    #   s1 contains s2
    return s1[0] >= s2[0] and s1[0] < s2[1] or \
           s1[1] > s2[0] and s1[1] <= s2[1] or \
           s1[0] < s2[0] and s1[1] > s2[1];
    
#3
#5 9
#1 4
#3 7
#updates 'segments' at indices between those in 'toUpdate'
def updateAffected(currShift, toUpdate, segments):
    #indices at ends may only partly overlap
    #indices in middle are duplicates and have contributor ID updated to '-1'
    #if adjacent segments have contributor ID of '-1', then combine
    
    #if no overlap
    if toUpdate[0] == -1:
        segments.insert(toUpdate[1], currShift);
        
    #currShift contained by segments[toUpdate[0]]
    elif segments[toUpdate[0]][1][0] <= currShift[1][0] and currShift[1][1] <= segments[toUpdate[0]][1][1]:
        if segments[toUpdate[0]][1][0] < currShift[1][0]: #left side
            segments.insert(0, [segments[toUpdate[0]][0],[segments[toUpdate[0]][1][0], currShift[1][0]]]);
        segments.insert(1, [-1,[currShift[1][0], currShift[1][1]]]); #overlap
        if currShift[1][1] < segments[toUpdate[0]][1][1]: #right side
            segments.insert(2, [segments[toUpdate[0]][0],[currShift[1][1], segments[toUpdate[0]][1][1]]]);
    
    else:
        #initialize counter
        i = toUpdate[0];
        
        #handle first overlapping segment
        
        #currShift straddles both sides of segments[toUpdate[0]]
        #currShift straddles (possibly equals) left edge of segments[toUpdate[0]]
        #currShift straddles (possibly equals) right edge of segments[toUpdate[0]]
        
        #if there is left edge spillover
        if currShift[1][0] < segments[i][1][0]:
            #insert segment for left edge spillover
            segments.insert(toUpdate[0], [currShift[0],[currShift[1][0], segments[i][1][0]]]);
            i += 1;
            toUpdate[1] += 1; #the range to update just grew by one
            
        #if currShift starts in the middle of the first shift is affects
        elif segments[i][1][0] < currShift[1][0]:
            segments.insert(i+1, [-1, [currShift[1][0], segments[i][1][1]]]);
            segments[i][1][1] = currShift[1][0];
            i += 1;
            toUpdate[1] += 1; #the range to update just grew by one
        
        #handle central segments
        while i <= toUpdate[1]:
            
            #if ith segment completely covered
            if segments[i][1][1] <= currShift[1][1]: #update the credit to 'shared'
                #if previous segment has shared credit
                if i > 0 and segments[i-1][0] == -1:
                    #extend previous segment over ith
                    segments[i-1][1][1] = segments[i][1][1];
                            
                    #delete ith segment
                    segments.pop(i);
                    toUpdate[1] -= 1;
                    i -= 1;
                else: #only share credit on ith segment
                    segments[i][0] = -1;
        
                #if currShift goes past end of ith segment and ith is last overlapping or there is a gap between ith and (i+1)th
                if segments[i][1][1] < currShift[1][1] and (i==toUpdate[1] or (i < len(segments)-1 and segments[i][1][1] < segments[i+1][1][0])):
                    
                    #insert new segment
                    segments.insert(i+1, [currShift[0], [segments[i][1][1], (segments[i+1][1][0] if i<toUpdate[1] else currShift[1][1])]]);
                    i += 1;
                    toUpdate[1] += 1;
                
            else: #not completely covered => last affected segment
                
                #if previous segment has shared credit
                if i > 0 and segments[i-1][0] == -1: #extend previous segment to end of currShift
                    segments[i-1][1][1] = currShift[1][1];
                else: #new shared-credit segment
                    segments.insert(i, [-1, [segments[i][1][0], currShift[1][1]]]);
                    i += 1;
                segments[i][1][0] = currShift[1][1];
            
            i += 1;
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
    # {-1:3; 0:2; 1:2; 2:1}
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



for i in range(1, 7):
    print(fireLifeguard('input/JM' + str(i) + '.in'));
#for i in [5]:
#for i in [1,2,3,4,5,6,7,8,9,10]:
#    print(str(i) + ":", fireLifeguard('input/' + str(i) + '.in'));
