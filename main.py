import argparse
from layout import Layout
from graph import Graph



def parse():
    
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Muestra más informacion al correr el programa',
        dest='v',
        default=False
    )
    # Cantidad de iteraciones, opcional, 50 por defecto
    parser.add_argument(
        '-i', '--iterations',
        help='Cantidad de iteraciones a efectuar',
        dest='i',
        type=int,
        default=150
    )
    # Temperatura inicial
    parser.add_argument(
        '-t', '--temperature',
        help='Temperatura inicial',
        dest='t',
        type=float,
        default=100.0
    )
    parser.add_argument(
        '-d', '--damping',
        help='Factor de decrecimiento de la T',
        dest='d',
        type=float,
        default=0.977
    )
    # Ancho máximo
    parser.add_argument(
        '-w', '--width',
        help='Ancho máximo',
        dest='w',
        type=int,
        default=1500
    )
    # Ancho máximo
    parser.add_argument(
        '-m', '--margin',
        help='Constante del ancho',
        dest='m',
        type=float,
        default=1.8
    )
    # 
    parser.add_argument(
        '-a', '--animate',
        action='store_true',
        help='Muestra la animación hasta equilibrar el grafo',
        dest='a',
        default=False,
    )
    # 
    parser.add_argument(
        '-c', '--constant',
        help='La constante',
        dest='c',
        type=float,
        default=1.3
    )
    parser.add_argument(
        '-p', '--pause',
        help='Tiempo de espera entre frames',
        dest='p',
        type=float,
        default=0.001
    )
    parser.add_argument(
        '-r', '--refresh',
        help='Cada cuántas frames muestra',
        dest='r',
        type=int,
        default=5
    )
    # Archivo del cual leer el grafo
    parser.add_argument(
        'file_name',
        help='Archivo del cual leer el grafo a dibujar'
    )
    
    return parser.parse_args()
    

def main():
    
    args = parse()

    gr = Graph.read(args.file_name)

    layout_gr = Layout(
        gr,
        args.file_name,
        args.i,
        args.r,  #refresh
        args.v,
        args.w,
        args.m,
        args.t,
        args.c,
        args.p,
        args.d
    )
    
    layout_gr.layout()
    return


if __name__ == '__main__':
    main()
