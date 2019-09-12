Atlas Throughput Evolution Code ReadMe Document

This is a document that summarises the workings of the AtlasThroughputEvolutionCode. 

The purpose of this code is to import data taken from the ATLAS telescopes at the two sites - Haleakala and Mauna Loa - and plot a quantifier of photon detection sensitivity (throughput) as a function of time to track the detector sensitivity over long time periods.

There are three methods of quantifying the throughput of the telescopes: 

	1. The zeropoint magnitude (defined as the magnitude of the brightness of an object that emits 1 photon per second)
	2. The 5-sigma magnitude 
	3. The 'seeing' - the width of the approximately Gaussian distribution of light observed from a point source through the Earth's atmosphere

All these quantities are known for every given measurement made with the telescope. 

The data that covers the entire operational time of the ATLAS telescopes is split between two files. This code can be run for two files of sensitivity data for a given telescope in a .bash script, using the following code syntax:

	python AtlasThroughputEvolution filename1 filename2

where 'filename1' is the name of the throughput data file that runs from the earliest recorded measurement to an intermediate one; 'filename2' is that from said intermediate measurement to the most recent one.

Note: the code can be amended for the input of a single file that contains the telescope sensitivity data across its entire operational time by editing the 'main' function -- the penultimate portion of the code -- from: 


	def main(argv=None):
		if argv is None:
			argv = sys.argv

	# The number of arguments to the code can be set to any given number; we set it to 2, as two files must be entered at a time.
		usage = "Usage: %s <Throughput filename> <Throughput filename>" % argv[0]
		if len(argv) != 3:
			sys.exit(usage)

		filename1 = str(argv[1])
		filename2 = str(argv[2])

		f1 = open(filename1)
		f2 = open(filename2)
		firstLine1 = f1.readlines()[0]
		print(firstLine1)
		firstLine2 = f2.readlines()[0]
		print(firstLine2)

		if "MJD-OBS" in firstLine1 and "MJD-OBS" in firstLine2:
			timeKey = "MJD-OBS"
			delimitingcharacter = '\t'

to:

	def main(argv=None):
		if argv is None:
			argv = sys.argv

	# The number of arguments to the code can be set to any given number; we set it to 1, as only one file need be entered at a time.
		usage = "Usage: %s <Throughput filename>" % argv[0]
		if len(argv) != 2:
			sys.exit(usage)

		filename = str(argv[1])

		f = open(filename1)
		firstLine = f.readlines()[0]
		print(firstLine)

		if "MJD-OBS" in firstLine:
			timeKey = "MJD-OBS"
			delimitingcharacter = '\t'


Upon running the code, the Command Line will prompt the user to enter the name of the telescope under analysis via the keyboard - the telescope name will form part of the plot that the code outputs. It will then ask the user to confirm the entered name; if the user wishes to proceed, 'y' must be entered into the Command Line; if the name entered was incorrect, and the user wishes to change it, 'n' must be entered and the code will stop.

If 'y' is entered, the code will then prompt the user to select one of the three measures of throughput (see above). Once this is entered, the code will run.

The code uses logical conditions that allow it to extract the required quantifier of telescope sensitivity from the datafiles. The code will import the sensitivity of every measurement made with the telescope under analysis, along with the MJD time on which each measurement was made. These measurements are then sorted by the filter that was used to take them (orange or cyan). The throughput and time values are then plotted on a graph (throughput vs time), allowing the former's temporal evolution to be easily visualised; axis labels and plot titles are specified according to the selected sensitivity quantifier automatically in code.

