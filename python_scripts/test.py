import sys

def main(argv=None):
    if argv is None:
        argv = sys.argv

    usage = "Usage: %s <SN filename>" % argv[0]
    if len(argv) != 2:
        sys.exit(usage)

    filename = argv[1]

    print(filename)

    return

if __name__ == '__main__':
    main()

