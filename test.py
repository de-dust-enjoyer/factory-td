dict = {0:5, 1:2, 2:5, 3:9, 4:34}
nestedDict = {0:dict, 1:dict, 2:dict}
print(len(dict))
print(len(nestedDict))
for i in nestedDict:
    print(len(i))