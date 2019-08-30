import sys

# To call thi code for multiple files, use the following code in a bash terminal:

#for file in `ls *.csv`; do python test.py $file; done

# Note the backquote ` -- it means take the result of the command to list all the .csv files (the asterisk), and iterate through each one line by line. 'file' is the result of the `ls *.csv` and the 'do' loop is the oject which performs the iteration. (syntax: for "files" do "everything in the do loop" done (done closes the loop). A variable inside bash is represented by the dollar $ sign.

def main(argv=None):
    if argv is None:
        argv = sys.argv

    usage = "Usage: %s <SN filename>" % argv[0]
    if len(argv) != 2:
        sys.exit(usage)

    filename = argv[1]

    print(filename)

    f = open(filename)
    firstLine = f.readlines()[0]
    print(firstLine)
    
    if "###MJD" in firstLine:

        determiner = 1

    elif "mjd" in firstLine:

        determiner = 2

    else:

        determiner = 0
        print("File not in correct format")

    print(determiner)

    return

if __name__ == '__main__':
    main()

