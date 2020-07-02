import sys, requests
from bs4 import *
#from functions import *

valid_parameters = ["-default", "-o", "-c", "-r", "-l", "-f", "-maple", "-mathematica", "-prog", "-crossrefs", "-k", "-a", "-extensions", "-s", "-example"]
parameters = ["-default"]
valid_type_of_sort = ["-ask", "-relevance", "-references", "-number", "-modified", "-created"]
valid_arguments = ["-search", "-sequence", "-user"]

#print a beautiful message
def welcome():
	print("----  |**  ---  ---    ----  |**|  |***")
	print("|  |  |--   |   |__    |  |  |__|  |  __")
	print("----  |__  ---  ___| . ----  | \\   |___|")

#the function below checks if the configuration file .oeis is valid
def valid_config(parameters):
	list_of_parameters = parameters.split()
	if "default" in list_of_parameters:
		return ["-default"]
	else:
		valid_list = list()
		for i in range(len(list_of_parameters)):
			if list_of_parameters[i] in valid_parameters and list_of_parameters[i] not in valid_list:
				valid_list.append(list_of_parameters[i])
	if valid_list == []:
		return ["-default"]
	else:
		return valid_list

#the function below checks if the type of sort precised in the file .oeis is valid
def valid_sort(type_of_sort):
	line = type_of_sort.split()
	if len(line) != 1:
		return "-ask"
	elif line[0] not in valid_type_of_sort:
		return "-ask"
	else:
		return line[0]

#the function below is to get a clean description of the sequence
def clean_description(desc):
	clean_desc = desc[0]
	for i in range(1, len(desc)):
		if not (desc[i] == " " and desc[i-1] == " "):
			clean_desc += desc[i]
	return clean_desc

#the function below is to clean the list of the first values of the sequence
def clean_first_val(unclean_list):
	clean_list = ""
	for i in range(len(unclean_list)):
		if not(unclean_list[i].isdigit()) and unclean_list[i] != " " and unclean_list[i] != ",":
			break
		else:
			clean_list += unclean_list[i]
	return clean_list

#the function below is to clean the full description of the sequence
def clean_full_descritpion(unclean_full_desc):
	clean_full_desc = list()
	for i in range(1, len(unclean_full_desc)):
		clean_full_desc.append(unclean_full_desc[i].replace("\n\n", "\n"))
	return clean_full_desc

#the function below is to print the description of the sequence depending your configuration
def disp_full_description(desc):
	if "-default" in parameters:
		for i in range(len(desc)):
			print(desc[i])
	else:
		for i in range(len(desc)):
			if "-o" not in parameters and desc[i][1] == "O":
				print(desc[i])
			if "-c" not in parameters and desc[i][1] == "C" and desc[i][2] == "O":
				print(desc[i])
			if "-r" not in parameters and desc[i][1] == "R":
				print(desc[i])
			if "-l" not in parameters and desc[i][1] == "L":
				print(desc[i])
			if "-f" not in parameters and desc[i][1] == "F":
				print(desc[i])
			if "-maple" not in parameters and desc[i][1] == "M" and desc[i][3] == "P":
				print(desc[i])
			if "-mathematica" not in parameters and desc[i][1] == "M" and desc[i][3] == "T":
				print(desc[i])
			if "-prog" not in parameters and desc[i][1] == "P":
				print(desc[i])
			if "-crossrefs" not in parameters and desc[i][1] == "C" and desc[i][2] == "R":
				print(desc[i])
			if "-k" not in parameters and desc[i][1] == "K":
				print(desc[i])
			if "-a" not in parameters and desc[i][1] == "A":
				print(desc[i])
			if "-extensions" not in parameters and desc[i][1] == "E" and desc[i][3] == "T":
				print(desc[i])
			if "-example" not in parameters and desc[i][1] == "E" and desc[i][3] == "A":
				print(desc[i])
			if "-s" not in parameters and desc[i][1] == "S":
				print(desc[i])

#the function below find the number of results in the page
def find_nb_result(search_result):
	content_list = search_result.split()
	id_result = content_list[1].split("-")
	begin = int(id_result[0])
	end = int(id_result[1])
	return end-begin+1

#the function below generate the url for the request
def gen_search_url(search):
	url = "https://oeis.org/search?q="
	url += search[0]
	for i in range(1, len(search)):
		url += "+"+str(search[i])
	url += "&start="+str(begin)
	url += "&sort="+type_of_sort[1:]
	return url

#the function below generate the url for the request
def gen_sequence_url(sequence):
	return "https://oeis.org/" + str(sequence)

def gen_sequence_author(name):
	url = "https://oeis.org/w/index.php?title=User:" 
	for i in range(len(name)-1):
		url += name[i]+"_"
	url+=name[len(name)-1]
	url += "&action=edit"
	return url

#the function below analyse the full webpage after a search	
def analyse_page_search(soup, nb_result):

	#find the name of each sequence and its description
	table = soup.find_all("table", attrs={"width":"100%"}) #10 tables containing our informations for each of the 10 sequences of the page
	description = list()
	for i in range(3, 3+nb_result):
		unclean_desc = table[i].get_text().replace("\n", "")
		description.append(clean_description(unclean_desc))

	#find the first values of the sequence an the full description
	table = soup.find_all("table", attrs={"cellpadding":"2"})
	first_values = list()
	full_desc = list()
	for i in range(0, 2*nb_result, 2):
		unclean_list = table[i].get_text().replace("\n", "")
		first_values.append(clean_first_val(unclean_list))
		unclean_full_desc = table[i+1].get_text().split("\n\n\n")
		full_desc.append(clean_full_descritpion(unclean_full_desc))

	for i in range(nb_result):	
		print(38*"-")
		print(description[i])
		print(first_values[i])
		disp_full_description(full_desc[i])
		print(38*"-")
		print()

#the function below analyse the full webpage of a specific sequence
def analyse_page_sequence(soup):
	#find the name of the sequence and its description
	table = soup.find_all("table", attrs={"width":"100%"}) #10 tables containing our informations for each of the 10 sequences of the page
	if len(table) < 2: #then there is no result
		print(44*"-")
		print("Sorry, the page you requested was not found.")
		print(44*"-")
		return
	unclean_desc = table[1].get_text().replace("\n", "")
	description = clean_description(unclean_desc)

	#find the first values of the sequence an the full description
	table = soup.find_all("table", attrs={"cellpadding":"2"})
	unclean_list = table[0].get_text().replace("\n", "")
	first_values = clean_first_val(unclean_list)
	unclean_full_desc = table[1].get_text().split("\n\n\n")
	full_desc = clean_full_descritpion(unclean_full_desc)
	
	print(38*"-")
	print(description[1:])
	print(first_values)
	disp_full_description(full_desc)
	print(38*"-")
	print()

#the function below analyse the full webpage of a specific user
def analyse_page_user(soup):
	div = soup.find_all("textarea")
	if len(div) == 0:
		print("This user does not exist.")
	else:
		description = div[0].get_text()
		print(38*"-")
		print(description)
		print(38*"-")

welcome()

arguments = sys.argv
file = open(".oeis", "r")
content = file.readlines()
given_parameters = str(content[16]).replace("\n", "")
parameters = valid_config(given_parameters) #if the given parameters are not valid, we use valid parameters
print("Configuration:", *parameters)

if len(arguments) != 2 or arguments[1] == "-search" or arguments[1] not in valid_arguments:
	type_of_use= "s" #a search is made
elif arguments[1] == "-sequence":
	type_of_use = "q" #we want the page of a specific sequence
elif arguments[1] == "-user":
	type_of_use = "a"


if type_of_use == "s":
	given_type_of_sort = str(content[18]).replace("\n", "")
	type_of_sort = valid_sort(given_type_of_sort)
	if type_of_sort == "-ask":
		type_of_sort = input("Type of sort; -relevance -references -number -modified -created: ").replace("\n", "")
	if type_of_sort == "-ask" or type_of_sort not in valid_type_of_sort:
		type_of_sort = "-relevance"


search = list(map(str, input("Search: ").split()))
search_not_stop = True
begin = 0
while search_not_stop:
	if type_of_use == "s":
		url = gen_search_url(search)
	elif type_of_use == "q":
		url = gen_sequence_url(search[0])
	elif type_of_use == "a":
		url = gen_sequence_author(search)
	print(url)
	oeis_request = requests.get(url)
	source_code = oeis_request.text
	soup = BeautifulSoup(source_code, "lxml")

	if type_of_use == "s":
		#find the number of results
		table = soup.find_all("table", attrs={"bgcolor":"#FFFFCC"}) #there are two <table> with bgcolor=#FFFFCC but only the first one is interesting
		out = table[0].get_text().replace("\n", "").split(".") # the sentence "Displaying x-x of xxxx results found" is isolate in a very dirty way
		print(38*"*")
		print(out[0])
		print(38*"*")
		print()
		if out[0][0] != "F" and out[0][0] != "S": #if there is no result or too much result, we stop
			nb_result = find_nb_result(out[0])
			begin += nb_result
			analyse_page_search(soup, nb_result)
			if nb_result < 10:
				search_not_stop = False
		if search_not_stop:
			next_page = input("Go to next page ? [y/n] ")
			if next_page.replace("\n", "") != "y":
				search_not_stop = False

	if type_of_use == "q":
		analyse_page_sequence(soup)
		search_not_stop = False

	if type_of_use == "a":
		analyse_page_user(soup)
		search_not_stop = False