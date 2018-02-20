def maxdiff(values):
    md = abs(values[1] - values[0])
    for i in range(2, len(values)):
        md = max(md, abs(values[i] - values[i-1]))
    return md

def maxseq(instring):
    i = 0
    seq=[]
    while i < len(instring):
        j = 1
        while i + j < len(instring) and instring[i] == instring[i + j]:
            j += 1
        seq.append(j)
        i += 1
    return max(seq)
