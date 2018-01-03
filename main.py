#!/usr/bin/python
import string
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


class Graph():

	def __init__(self, vertices):
		self.V = vertices
		self.color_global = [0] * self.V
		self.indp = [0 for row in range(vertices)]
		self.graph = [[0 for column in range(vertices)]\
							for row in range(vertices)]

	# A utility function to check if the current color assignment is safe for vertex v
	# This is done by comparing the potential (to be assigned) colour for vertex v with
	# already assigned colours to all its neighbours	
	def isSafe(self, v, colour, c):
		for i in range(self.V):
			if self.graph[v][i] == 1 and colour[i] == c:
				return False
		return True
	
	# A recursive utility function to solve 'm' coloring problem
	# Try all colours one by one for each vertex and check if assignment of that colour to
	# the vertex is Safe. Assign whenever safe colour is found and then move to next vertex
	# colour[0] gets -1 whenever algorithm is not able to colour graph in 'm' colours  	
	def graphColourUtil(self, m, colour, v):
		if v == self.V:
			return True

		for c in range(1, m+1):
			if self.isSafe(v, colour, c) == True:
				colour[v] = c
				if self.graphColourUtil(m, colour, v+1) == True:
					return True
				colour[v] = -1
	
	# Begins the colouring operation for graph and returns true whenever colouring is possible  
	def graphColouring(self, m,var_list):
		colour = [0] * self.V
		if self.graphColourUtil(m, colour, 0) == False:
			return False

		isZero = [0 for row in range(self.V)]
		sum = [0 for row in range(self.V)]	
		if colour[0] == -1:
			return False
		else:
			print ""
			print "Following are the assigned colours and independent nodes:"

			# Find maximum number of colours used 
			colour_max = 0
			self.color_global = colour
			for i in range(self.V):
				if colour_max < colour[i]:
					colour_max = colour[i]
					
			for i in range(self.V):
				if self.indp[i] == 1:
					print var_list[i]," node is independent"
					self.color_global[i] = 0
				else:
					print "Colour of ",var_list[i]," node is ",colour[i]
			print ""			
			print "Total number of registers used : ",colour_max
			return True
	
	# Finds the vertex of maximum degree in the graph and removes it  	
	def reduceGraph(self):
		sum = [0 for row in range(self.V)]
		max_sum = 0
		indx = 0
		for i in range(self.V):
			for j in range(self.V):
				sum[i] = sum[i] + self.graph[i][j]
		#print sum	
		for i in range(self.V):
			if max_sum <= sum[i]:
				max_sum = sum[i]
				indx = i
		
		self.indp[indx] = 1;	
		if max_sum == 0:
			raw_input("Error")
		for i in range(self.V):
			self.graph[i][indx] = 0
			self.graph[indx][i] = 0
		return True	
				

				
# Used to find a list of variables for a given set of tuples, which may contain unordered multiple instances of the same
def variable_list(tuples):
    var_list = []
    for i in range(0,len(tuples)):
        for j in range(0,len(tuples[i])):
            if (not tuples[i][j] in var_list):
                var_list.append(tuples[i][j])		#This appends a variable if it not present in the list
    print "Variable list for given code :",var_list
    return var_list    


# This function takes a list of tuples, and the corresponding variable list, and finds out the Adjacency matrix for the formed RIG 		
def adj(var_list, tuples):

    adj_mat = [[0 for x in range(0,len(var_list))] for y in range(0,len(var_list))]	#Initialization of Ajdacency matrix 
    for i in range(0,len(tuples)):
        for j in range(0,len(tuples[i])):	#Loop for a variable in a tuple
            for k in range(0,len(tuples[i])):	#Loop for the second variable in the tuple, between which we are introducing an edge
                #print var_list.index(tuples[i][j])
                adj_mat[var_list.index(tuples[i][j])][var_list.index(tuples[i][k])]=1	#For variables appearing together in a tuple, introduces an edge in the graph 

    for i in range(0,len(var_list)):
        adj_mat[i][i]=0		#Diagonal entries removed, since we dont want self loops in our graphs 
    print "Adjacency Matrix of RIG :",adj_mat
    return adj_mat

#for a path in dataflow finds the tuples of live variables at different points of time
def with_while_rig(tuples):
	out = []
	temp = []
	temp2 = []
	for i in range(len(tuples)):
		for start_check in range(i+1,len(tuples)):
			# if output variable is reassigned before using it
			if (tuples[i][0] == tuples[start_check][0]):
				break
			else:
				# outputs are being stored incase if they are being used in next instructions 
				if (tuples[i][0]!= tuples[start_check][0] and (tuples[i][0] in tuples[start_check])):
					if (not tuples[i][0] in temp):
						temp.append(tuples[i][0])
						break
						
		#test cases for live variables
		# input variable in one instruction will be decided as live.  
		# 1. If input variable is used without redefining it.
		# 2. If input variable is used in some next instruction, then removed from live variable list.
		# 3. In while loops last outputs are being used in the earlier statements. 
		for j in range(1,len(tuples[i])):
			if (not tuples[i][j] in temp):
				temp.append(tuples[i][j])
			for check_i in range(i+1,len(tuples)):
				for check_j in range(1,len(tuples[check_i])):
					temp2.append(tuples[check_i][check_j])
			for start_check in range(i+1,len(tuples)):
				if ((tuples[i][j] == tuples[start_check][0] and (tuples[i][0] in tuples[start_check])) or (not tuples[i][j] in temp2)):
					temp.remove(tuples[i][j])
					break
			temp2 =[]
		# either we use the last variable or not anyway it will be a live variable
		if (i == len(tuples)-1 and not (tuples[i][0] in temp)):
			temp.append(tuples[i][0])
		#print temp,"after i", i+1
		out.append(temp[:])
	return out	

##########################################################################################################################################
#reading from a code file
f = open('input3.txt','r')
#f = open('Test3.txt','r')

# reading file line by line and omitting while, if-else conditional lines.
# gives only tuples of variables from the file
# removes symbols, numerical values
# only alphabets can be used to form a variable. 
inp = []
message = "start"
while (message[0] != "return"):
	message = f.readline()
	if ("while" in message):
		message = f.readline()
	if ("if" in message):
		message = f.readline()
	if ("else" in message):
		message = f.readline()
	if ("end while" in message):
		message = f.readline()
	if ("end if" in message):
		message = f.readline()
	message = message.translate(string.maketrans('', ''), '=+-*/;_'+ string.digits)
	message = message.split()
	inp.append(message)
	#print message
del inp[-1]
#print inp
f.close()

var = with_while_rig(inp)
var_list = variable_list(var)

g = Graph(len(var_list))
g.graph = adj(var_list,var)

# decides spilling in RIG
number_of_registers = 5
done = 0;
while done == 0: 
	if g.graphColouring(number_of_registers,var_list):
		done = 1;
	else:
		#print "Reducing Graph" 
		g.reduceGraph()
#raw_input("Finished")
print ""
print "Finished Register Allocation using Graph Coloring\n"

colors = g.color_global
labels = {}
graphmatrx = np.asarray(g.graph)
G = nx.from_numpy_matrix(graphmatrx)
for i in range(len(g.graph)):
	labels[i] = var_list[i] 

# networkx library is used for building a graph.
nx.draw(G,labels=labels, with_labels=True,node_size=650,node_color = colors)
plt.show()
