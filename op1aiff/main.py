#!/usr/bin/env python3
"""OP-1 Preset Tool."""

import argparse
from . import op_aiff


__author__ = 'Richard Lewis'
__copyright__ = 'Copyright 2018, Richard Lewis'
__license__ = 'MIT'
__status__ = 'Development'
__version__ = '0.0.1'


description = """
TODO: Write description.
"""

help = """TODO: Write help."""


def main():
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    # parser.add_argument('action', choices=['unpack', 'modify', 'repack'],
    #                     help='action to perform on the firmware')
    parser.add_argument('path', type=str, nargs=1, help='preset file to use')
    # parser.add_argument('--options', nargs='+', help=help)
    # parser.add_argument('--debug', action='store_true', help='print debug messages')
    # parser.add_argument('--version', action='version', version=__version__,
    #                     help='show program\'s version number and exit')
    args = parser.parse_args()

    in_path = args.path[0]
    out_path = in_path + '.mod.aif'

    op_aiff.analyze_preset(in_path)

    data = op_aiff.read_preset(in_path)
    data = {'adsr': [2112, 3008, 0, 9792, 2048, 4000, 4000, 4000], 'fx_active': True, 'fx_params': [5760, 15544, 8328, 8000, 0, 0, 0, 0], 'fx_type': 'delay', 'knobs': [16367, 10168, 12464, 32767, 0, 0, 0, 0], 'lfo_active': False, 'lfo_params': [6144, 27847, 2704, 10160, 0, 0, 0, 0], 'lfo_type': 'value', 'name': '20161129_1135', 'octave': 4, 'synth_version': 2, 'type': 'iter'}
    op_aiff.write_preset(in_path, out_path, data)

    # print(data)


if __name__ == '__main__':
    main()
