# String containing the list of lists
string = "[['B', 'N', 'H', 'N', 'T', 'N', 'N', 'N', 'H', 'N', 'N', 'H', 'H', 'T', 'H', 'H', 'N', 'N', 'T', 'T', 'N', 'N', 'N', 'H', 'T', 'N', 'T', 'T', 'N', 'N', 'N', 'H', 'T', 'N', 'N', 'H', 'N', 'N', 'H', 'H', 'N', 'H', 'H', 'N', 'H', 'N', 'H', 'N', 'N', 'T'], ['B', 'H', 'H', 'N', 'B', 'H', 'N', 'T', 'T', 'H', 'N', 'H', 'N', 'B', 'N', 'N', 'B', 'N', 'N', 'N', 'N', 'B', 'T', 'H', 'N', 'N', 'T', 'N', 'N', 'T', 'B', 'N', 'T', 'T', 'N', 'N', 'N', 'B', 'N', 'N', 'T', 'H', 'N', 'N', 'T', 'N', 'N', 'N', 'H', 'N"

# Split the string on the outer square brackets
string_list = string.split('[')

# Use the map() method to apply the list() function to each element in the string_list,
# which converts the string representation of a list into a list of strings
list_of_lists = list(map(list, string_list))

# Print the 2D list
print(list_of_lists)
