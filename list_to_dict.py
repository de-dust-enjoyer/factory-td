def nestedlist_to_nesteddict(list:list):
	counter1 = 0
	counter2 = 0
	big_dict = {}
	smol_dict = {}
	for row in list:
		counter2 = 0
		smol_dict = {}
		for element in row:
			smol_dict[counter2] = element
			counter2 += 1
		big_dict[counter1] = smol_dict
		counter1 += 1
	return big_dict

