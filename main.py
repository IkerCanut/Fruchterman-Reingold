import argparse
from layout import Layout
from graph import Graph


def parse():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='activate comments during execution',
        dest='v',
        default=False
    )
    parser.add_argument(
        '-i', '--iterations',
        help='max number of iterations permitted',
        dest='i',
        type=int,
        default=400
    )
    parser.add_argument(
        '-t', '--temperature',
        help='initial temperature',
        dest='t',
        type=float,
        default=100.0
    )
    parser.add_argument(
        '-d', '--damping',
        help='temperature\'s damping factor',
        dest='d',
        type=float,
        default=0.977
    )
    parser.add_argument(
        '-c', '--constant',
        help='algorithm\'s force constant to modify the spread',
        dest='c',
        type=float,
        default=1.3
    )
    parser.add_argument(
        '-w', '--width',
        help='frame width',
        dest='w',
        type=int,
        default=1000
    )
    parser.add_argument(
        '-m', '--margin',
        help='multiplier to adjust graph size',
        dest='m',
        type=float,
        default=1.8
    )
    parser.add_argument(
        '-na', '--not-animated',
        action='store_true',
        help='do not animate the plot',
        dest='na',
        default=False,
    )
    parser.add_argument(
        '-p', '--pause',
        help='time between frames, if animated',
        dest='p',
        type=float,
        default=0.01
    )
    parser.add_argument(
        '-r', '--refresh',
        help='frames between plots, if animated',
        dest='r',
        type=int,
        default=10
    )
    parser.add_argument(
        'file_name',
        help='file containing graph description'
    )

    return parser.parse_args()


def main():

    args = parse()

    graph = Graph.read(args.file_name)

    layout_graph = Layout(
        graph,
        args.v,
        args.i,
        args.t,
        args.d,
        args.w,
        args.m,
        not args.na,
        args.c,
        args.p,
        args.r
    )

    layout_graph.layout()
    return


if __name__ == '__main__':
    main()
