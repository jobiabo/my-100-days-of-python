def passing_scores(scores):
    passed = []
    # for index in range(len(scores)-1):
        # if scores[index] > 50:
        #     passed.append(scores[index])

    i = 0
    while i < len(scores):
        print(scores[i])
        if scores[i] >= 50:
            passed.append(scores[i])
        elif scores == []:
            return []
        
        i=i+1
        
    return passed

# print(passing_scores([]))
# print(passing_scores([50]))
# print(passing_scores([80, 90, 100, 78]))

assert passing_scores([50]) == [50]
assert passing_scores([80]) == [80]
assert passing_scores([]) == []

