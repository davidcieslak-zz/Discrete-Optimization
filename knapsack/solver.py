#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight', 'density'])

def Okay_Jay(items, precomp, k, j):
	#because the index of the item list and the solution matrix are offset by one
	if j == 0:
		return 0
	elif items[j-1].weight <= k:
		if k in precomp and j-1 in precomp[k]:
			a = precomp[k][j-1]
		else:
			a = Okay_Jay(items, precomp, k, j-1)
		if k-items[j-1].weight in precomp and j-1 in precomp[k-items[j-1].weight]:
			b = items[j-1].value + precomp[k-items[j-1].weight][j-1]
		else:
			b = items[j-1].value + Okay_Jay(items, precomp, k-items[j-1].weight, j-1)
		if a > b:
			return a
		else:
			return b
	else:
		if k in precomp and j-1 in precomp[k]:
			return precomp[k][j-1]
		else:
			return Okay_Jay(items, precomp, k, j-1)

def dynamic_programming_solver(items, item_count, capacity):
    computed_vals_lookup = {}
    for item_index in xrange(0, item_count + 1):
	    computed_vals_lookup[item_index] = {}
	    for c in xrange(0, capacity + 1):
		a = Okay_Jay(items, computed_vals_lookup, c, item_index)
		computed_vals_lookup[item_index][c] = a

    last_value = computed_vals_lookup[item_count][capacity]
    last_index = item_count
    capacity_remaining = capacity
    value = 0
    weight = 0
    taken = [0]*len(items)
    for item_index in xrange(item_count, 0, -1):
	if computed_vals_lookup[item_index][capacity_remaining] != computed_vals_lookup[item_index-1][capacity_remaining]:
		taken[items[item_index-1].index] = 1
		value += items[item_index-1].value
		weight += items[item_index-1].weight
		capacity_remaining = capacity_remaining - items[item_index-1].weight
    # prepare the solution in the specified output format
    output_data = '%s 0\n' % value
    output_data += ' '.join(map(str, taken))
    return output_data

"""
class Node():
    best_value = 0
    best_takens = []
    capacity = 0
    items_sorted = []

    def __init__(self, value, capacity, takens, previous_estimate):
    	self.value = value
	self.capacity = capacity
	if previous_estimate != -1:
		self.estimate = previous_estimate
	else:
		self.estimate = get_best_estimate(Node.items_sorted, Node.capacity, takens)
	self.takens = takens
	self.index = len(self.takens)

    def get_left_child(self):
	item = Node.items_sorted[self.index]
	return Node(self.value + item.value, self.capacity - item.weight, self.takens + [0], self.estimate)

    def get_right_child(self):
	item = Node.items_sorted[self.index]
	return Node(self.value, self.capacity, self.takens + [1], -1)

    def is_leaf(self):
	return self.index == len(Node.items_sorted)

def get_best_estimate(items_sorted, capacity, takens):
    value = 0
    weight = 0
    for index in xrange(0, len(items_sorted)):
        if index < len(takens) and takens[index] == 1:
		#skip because item is already taken
        	continue
	item = items_sorted[index]
	#do an optimistic assessment by taking the remaining capacity and prorating the item's value density
	if weight + item.weight > capacity:
		value += (item.value * ((capacity - weight) * 1.0) / item.weight)
	else:
		value += item.value
		weight += item.weight
    return value

def branch_and_bound_solver(items, item_count, capacity):
    Node.best_value = 0
    Node.best_takens = []
    Node.capacity = capacity
    #Node.items_sorted = sorted(items, key = lambda x: x.value, reverse = True)
    Node.items_sorted = sorted(items, key = lambda x: x.value/x.weight, reverse = True)

    root = Node(0, capacity, [], -1)
    stack = [root.get_right_child(), root.get_left_child()]
    while stack:
	node = max(stack, key = lambda x: x.value)
	stack.remove(node)

	if node.capacity < 0 or node.estimate < Node.best_value: continue

	if node.is_leaf() and node.value > Node.best_value:
		Node.best_value = node.value
		Node.best_takens = node.takens
		continue

	if not node.is_leaf():
		stack.append(node.get_left_child())
		stack.append(node.get_right_child())

    taken = [0]*len(items)
    value = 0
    for index in xrange(0, len(Node.best_takens)):
        if Node.best_takens[index] == 0: 
		taken[Node.items_sorted[index].index] = 1
		value += Node.items_sorted[index].value



    # prepare the solution in the specified output format
    output_data = '%s 0\n' % value
    output_data += ' '.join(map(str, taken))
    return output_data
"""

class Node():
    best_value = 0
    best_selections = []
    capacity = 0
    items_sorted = []
    
    def __init__(self, value, room, selections, previous_estimate):
        self.value = value
        self.room = room
        self.estimate = previous_estimate if previous_estimate != -1 else get_best_estimate(Node.items_sorted, Node.capacity, selections)
        self.selections = selections
        self.index = len(self.selections)
        
    def get_left_child(self):
        item = Node.items_sorted[self.index]
        return Node(self.value + item.value, self.room - item.weight, self.selections + [1], self.estimate)
    
    def get_right_child(self):
        item = Node.items_sorted[self.index]
        return Node(self.value, self.room, self.selections + [0], -1)
    
    def is_leaf(self):
        return self.index == len(Node.items_sorted)

def get_best_estimate(items_sorted, capacity, selections):
    value = 0
    weight = 0
    for idx in xrange(len(items_sorted)):
        if idx < len(selections) and selections[idx] == 0: continue
        i = items_sorted[idx]
        if weight + i.weight > capacity:
            value += i.value * (((capacity - weight) * 1.0) / i.weight) 
            break
        value += i.value
        weight += i.weight
 
    return value

def branch_and_bound_solver(items, item_count, capacity):
    Node.best_value = 0
    Node.best_selections = []
    Node.capacity = capacity
    Node.items_sorted = sorted(items, key = lambda i: i.density, reverse = True)
    
    root = Node(0, capacity, [], -1)
    stack = [root.get_right_child(), root.get_left_child()]
    while stack:
        node = max(stack, key = lambda i: i.value)
        stack.remove(node)
        
        if node.room < 0 or node.estimate < Node.best_value: continue
        
        if node.is_leaf() and node.value > Node.best_value:
            Node.best_value = node.value
            Node.best_selections = node.selections
            continue
        
        if not node.is_leaf():
            stack.append(node.get_left_child())
            stack.append(node.get_right_child())
    
    selections = [0] * len(items)
    value = 0
    for idx in xrange(len(Node.best_selections)):
        if Node.best_selections[idx] == 1: 
		selections[Node.items_sorted[idx].index] = 1
		value += Node.items_sorted[idx].value

    # prepare the solution in the specified output format
    output_data = '%s 0\n' % value
    output_data += ' '.join(map(str, selections))
    return output_data
	


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in xrange(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1]), float(parts[0])/float(parts[1])))

    #return dynamic_programming_solver(items, item_count, capacity)
    return branch_and_bound_solver(items, item_count, capacity)

import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

