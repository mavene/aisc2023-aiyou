from org.transcrypt.stubs.browser import *
import random

def gen_random_int(number, seed):
	random.seed(seed)
	array = [random.randint(-50, 50) for i in range(number)]
	return array

def generate():
	number = 10
	seed = 200

	# call gen_random_int() with the given number and seed
	# store it to the variable array
	array = gen_random_int(number, seed)

	array_str = ", ".join(array) + "."

	# This line is to place the string into the HTML
	# under div section with the id called "generate"	
	document.getElementById("generate").innerHTML = array_str


def sortnumber1():
	'''	This function is used in Exercise 1.
		The function is called when the sort button is clicked.

		You need to do the following:
		- get the list of numbers from the "generate" HTML id, use document.getElementById(id).innerHTML
		- create a list of integers from the string of numbers
		- call your sort function, either bubble sort or insertion sort
		- create a string of the sorted numbers and store it in array_str
	'''
	array_str = document.getElementById("generate").innerHTML
	
	sortedarray = [int(i) for i in array_str.strip().split(",")]

	# MY SORTING ALGO HERE
	n = len(sortedarray)
	swapped = True
	while swapped:
		swapped = False
		new_n = 0
		for inner_index in range(1, n):
			if sortedarray[inner_index - 1] > sortedarray[inner_index]:
				sortedarray[inner_index], sortedarray[inner_index - 1] = sortedarray[inner_index - 1], sortedarray[inner_index]
				swapped = True
				new_n = inner_index
		n = new_n

	array_str = ", ".join(sortedarray) + "."

	document.getElementById("sorted").innerHTML = array_str

def sortnumber2():
	'''	This function is used in Exercise 2.
		The function is called when the sort button is clicked.

		You need to do the following:
		- Get the numbers from a string variable "value".
		- Split the string using comma as the separator and convert them to 
			a list of numbers
		- call your sort function, either bubble sort or insertion sort
		- create a string of the sorted numbers and store it in array_str
	'''
	# The following line get the value of the text input called "numbers"
	value = document.getElementsByName('numbers')[0].value

	# Throw alert and stop if nothing in the text input
	if value == "":
		window.alert("Your textbox is empty")
		return

	sortedarray = [int(i) for i in value.strip().split(",")]

	n = len(sortedarray)
	for outer_index in range(1, n):
		inner_index = outer_index
		temp_val = sortedarray[inner_index]
		while (inner_index > 0) and (temp_val < sortedarray[inner_index - 1]):
			sortedarray[inner_index] = sortedarray[inner_index - 1]
			inner_index -= 1
		sortedarray[inner_index] = temp_val

	array_str = ", ".join(sortedarray) + "."

	document.getElementById("sorted").innerHTML = array_str