import argparse

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
        required=True,
        help="String of available letters (e.g., 'ABCDEF').",
    )
    parser.add_argument(
        "--start",
        type=str,
        default="",
        help="Optional starting board string, multiline.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    words = [validate_word(line.strip()) for line in args.words if line.strip()]
    letters = args.letters.strip().upper()

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
