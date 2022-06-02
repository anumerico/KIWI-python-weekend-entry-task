import os
import sys
import argparse


def stdin():
    # required args
    path = ""
    input_origin = ""
    input_destination = ""

    # optional args
    input_bags = 0

    is_return = False

    parser = argparse.ArgumentParser(description="Parser tutorial")
    parser.add_argument("--bags", default=0, type=int,
                        required=False, help="This is the number of bags")
    parser.add_argument("--ret", action='store', default=False,
                        nargs='?', required=False, help="This is the return flight option")
    parser.add_argument("--exp", default="", type=str, nargs='*',
                        required=False, help="This is the option to save the json export")

    args, _ = parser.parse_known_args()

    # required args
    assert(sys.argv[1]), "Please provide path, origin and destination"
    path = sys.argv[1]
    is_exist = os.path.exists(path)

    assert(is_exist), "Provided path to csv is not valid"

    assert(sys.argv[2]), "Please provide both, origin and destination"
    input_origin = sys.argv[2]

    assert(sys.argv[3]), "Please provide both, origin and destination"
    input_destination = sys.argv[3]

    # optional args
    input_bags = args.bags    

    if args.ret is None:
        is_return = True
    else:
        is_return = args.ret

    # export .json name
    if args.exp == '':
        is_export = False
    elif args.exp == []:
        is_export = "export"
    else:
        is_export = args.exp[0]


    return path, input_origin, input_destination, input_bags, is_return, is_export
