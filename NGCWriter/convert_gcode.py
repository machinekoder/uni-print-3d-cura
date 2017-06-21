#!/usr/bin/env python

import sys
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="""
    convert a RepRap/Marlin flavor GCode file to a Machinekit/Velocity-Extrusion flavor GCode file
    """)
    parser.add_argument('-i', '--input', help='Input file', required=True)
    parser.add_argument('-o', '--output', help='Output file', default=None)
    parser.add_argument('-nv', '--no-velocity-extrusion', help='Disable velocity extrusion', action='store_true')
    parser.add_argument('-s', '--start-gcode', help='GCode to be added at beginning of file', default=None)
    parser.add_argument('-e', '--end-gcode', help='GCode to e added at end of file', default=None)
    args = parser.parse_args()

    sys.path = [os.path.abspath(os.path.dirname(__file__))] + sys.path
    from converter.gcode2ngc import GCode2Ngc
    from converter.ngc2ve import Ngc2Ve

    input_name = args.input
    output_name = args.output
    if output_name is None:
        (path, _) = os.path.splitext(input_name)
        output_name = '%s.ngc' % path

    print('converting %s -> %s' % (input_name, output_name))
    gcodeConverter = GCode2Ngc()
    veConverter = Ngc2Ve()

    input_file = open(input_name, 'rt')
    output_file = open(output_name, 'wt')

    if args.start_gcode:
        output_file.write(args.start_gcode)

    processable = []
    processable.append(input_file.read())
    gcodeConverter.process(processable)
    if not args.no_velocity_extrusion:
        veConverter.process(processable)

    output_file.write(processable[0])

    if args.end_gcode:
        output_file.write(args.end_gcode)

    input_file.close()
    output_file.close()

if __name__ == '__main__':
    main()
