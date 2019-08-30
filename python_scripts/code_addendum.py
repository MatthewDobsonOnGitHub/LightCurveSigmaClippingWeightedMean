def primary():

	print("WARNING: This code will save its output into a file of the same name as the input datafile. \nBefore proceeding, make sure all of the files that you wish to run the code on are named appropriately. \nReccomendation: Save the file as the name of its supernova (e.g. SN20XXyyy), meaning the code will produce a directory with the file containing the output data for a supernova named appropriately for said supernova.")

	print("If all files are named appropriately, enter 'y' to continue. \nIf you wish to make any changes, enter 'n'")

	condition = input()

	if condition == 'y':

		main()
