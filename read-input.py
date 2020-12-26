# tsp_file_name from user
# close program if invalid (see except)
tsp_file_name = input("TSP file name: ")

try:
# open tsp file and read in expected values
# dependent on specific file format, ensure identical file formats
    tsp_file = open(tsp_file_name)

# read line 1 and save name as var
    tsp_line = tsp_file.readline()
    tsp_name = tsp_line.replace('NAME : ', '').replace('\n', '')

# read line 2 and save comment as var
    tsp_line = tsp_file.readline()
    tsp_comment = tsp_line.replace('COMMENT : ', '').replace('\n', '')

# read line 3 and save type as var
    tsp_line = tsp_file.readline()
    tsp_type = tsp_line.replace('TYPE : ', '').replace('\n', '')

# read line 4 and save dimension as var
    tsp_line = tsp_file.readline()
    tsp_dimension = tsp_line.replace('DIMENSION : ', '').replace('\n', '')

# read line 5 and fave edge weight type as var
    tsp_line = tsp_file.readline()
    tsp_edge_type = tsp_line.replace('EDGE_WEIGHT_TYPE : ', '').replace('\n','')

# print header values
    print('NAME: ' + tsp_name)
    print('COMMENT: ' + tsp_comment)
    print('TYPE: ' + tsp_type)
    print('DIMENSION: ' + tsp_dimension)
    print('EDGE WEIGHT TYPE: ' + tsp_edge_type)

# skip title, line 6
    tsp_line = tsp_file.readline()

# write xy coordinates into node_coord
    tsp_dimension = int(tsp_dimension)
    node_coord = []
    for x in range(tsp_dimension):
        arr = tsp_file.readline().replace('\n','').split(' ')
        node_coord += [arr]

#print node_coord 
    print("COORDINATES: " + str(node_coord))

except (IOError, ValueError, EOFError) as e:
# catch if cannot open file, invalid value, or end of file before expected
# print error
    print(e)

finally:
# close file after reading input
    tsp_file.close()

# read cost_file_name from user
# close file if invalid (see exception)
cost_file_name = input("Intercity costs file name: ")

try:
# open cost file
    cost_file = open(cost_file_name)

# write values into cost_matrix
    cost_matrix = []
    for x in range(tsp_dimension):
        arr = cost_file.readline().replace('\n', '').split(' ')
        cost_matrix += [arr]

# print cost_matrix
    print("COST MATRIX: " + str(cost_matrix))

except (IOError, ValueError, EOFError) as e:
# catch if cannot open file, invalid value, or end of file before expect
    cost_file.close()