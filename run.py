import argparse

from compiler.compiler import create_compiler
from compiler.utils import Logger


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('--output', help="specify output file")

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    if args.output:
        logger = Logger(to_file=args.output)
    else:
        logger = Logger()

    logger.log('START')

    compiler = create_compiler(with_logger=logger)
    with open(args.input, 'r') as f:
        source = f.read()
        compiler.typecheck(source)

    logger.log('DONE')
