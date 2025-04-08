import argparse
import random
from collections import Counter
from typing import Iterable

from banana.board import Board
from banana.reasoning.generators import SimpleConstraintGenerator
from banana.reasoning.searches.dfs import DFS
from banana.validation import validate_word


def parse_args():
    parser = argparse.ArgumentParser(description="Solve a Bananagrams-style board.")
    parser.add_argument(
        "--words",
        type=argparse.FileType("r"),
        required=True,
        help="Path to a file containing valid words, one per line.",
    )
    parser.add_argument(
        "--letters",
        type=str,
        default="",
        help="String of available letters (e.g., 'ABCDEF').",
    )
    parser.add_argument(
        '--random_letters',
        type=int,
        default=0,
        help='Number of random letters to generate (e.g., 7).'
    )
    parser.add_argument(
        "--start",
        type=str,
        default="",
        help="Optional starting board string, multiline.",
    )
    return parser.parse_args()


def make_random_letters(n:int, words:list[str])->Iterable[str]:
    counts = Counter(''.join(words))
    letters = random.choices(list(counts.keys()), weights=list(counts.values()), k=n,)
    print(f'letters are {(''.join(sorted(letters)))!r}')
    return letters

def make_letters(args, words:Iterable[str])->list[str]:
    if args.random_letters:
        return make_random_letters(args.random_letters, words)
    elif args.letters:
        return args.letters.strip().upper()
    else:
        raise ValueError("Either --letters or --random_letters must be specified.")

def main():
    args = parse_args()

    words = [validate_word(line.strip()) for line in args.words if line.strip()]
    letters = make_letters(args, words)

    board = Board.from_str(args.start) if args.start else Board([])

    search = DFS(words, SimpleConstraintGenerator(words))
    try:
        result = search.search(board, letters)
        print("Solved board:")
        print(result)
    except DFS.SearchError:
        print("No solution found.")


if __name__ == "__main__":
    main()
