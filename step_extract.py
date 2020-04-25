#!/usr/bin/python3
import sys
from pathlib import Path
import argparse

def initialize_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', dest='output_dirname', default='output')
    parser.add_argument('-i', dest="input_filename", help="Input file")
    parser.add_argument('--isolate', dest='own_directory', action='store_true', help="Isolate each run in its own directory.")
    # parser.add_argument('--output-type')
    return parser
def get_outfile(name, ext, output_dir, previous_file=None):
	if previous_file:
		previous_file.close()
	newfile = output_dir / '{}.{}'.format(name, ext)
	return newfile.open('w+')

if __name__ == "__main__":
    parser = initialize_parser()
    args = parser.parse_args()
    
    if not args.input_filename:
        print("Error: -i requires an argument; Please input a valid LTSpice exported text file.")
        exit(1)
    
    output_dir_base = Path(args.output_dirname)
    output_dir_base.mkdir(exist_ok=True)

    if args.own_directory:
        own_directory = True
    else:
        own_directory = False

    with open(args.input_filename) as infile:
        datafields = infile.readline()
        outfile_index = 0
        outfile = None
        for line in infile:
            if not line[0].isnumeric():
                outfile_index = outfile_index + 1
                # Individualized directory for each run, if specified
                if own_directory:
                    run_output_dir = output_dir_base / '{}'.format(outfile_index)
                    run_output_dir.mkdir(exist_ok=True)
                else:
                    run_output_dir = output_dir_base
                # Update the new output file, but respect reentrant
                outfile = get_outfile(outfile_index, 'txt', run_output_dir, outfile)
                outfile.write(datafields)
                infofile = get_outfile(outfile_index, 'info', run_output_dir)
                infofile.write(line)
                infofile.close()
                continue
            outfile.write(line)
        outfile.close()