import argparse
import random
from collections import Counter
from typing import Iterable

from banana.board import Board
from banana.reasoning.generators import SimpleConstraintGenerator
from banana.reasoning.searches import BeamSearch
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
        "--random_letters",
        type=int,
        default=0,
        help="Number of random letters to generate (e.g., 7).",
    )
    parser.add_argument(
        "--start",
        type=str,
        default="",
        help="Optional starting board string, multiline.",
    )
    parser.add_argument(
        "--beam_size",
        type=int,
        default=100,
        help="Beam size for beam search.",
    )
    parser.add_argument(
        "--random_seed",
        type=int,
        default=0,
        help="Random seed for reproducibility. 0 to disable.",
    )
    parser.add_argument(
        "--max_depth",
        type=int,
        default=0,
        help="Maximum depth for beam search. 0 to disable.",
    )
    return parser.parse_args()


def make_random_letters(n: int, words: list[str]) -> Iterable[str]:
    # counts = Counter("".join(words))
    # print(f"raw letter counts are {sorted(dict(counts).items())}")
    counts = Counter(
        {
            "A": 13,
            "B": 3,
            "C": 3,
            "D": 6,
            "E": 18,
            "F": 3,
            "G": 4,
            "H": 3,
            "I": 12,
            "J": 2,
            "K": 2,
            "L": 5,
            "M": 3,
            "N": 8,
            "O": 11,
            "P": 3,
            # "Q": 2,
            "R": 9,
            "S": 6,
            "T": 9,
            "U": 6,
            "V": 3,
            "W": 3,
            "X": 2,
            "Y": 3,
            "Z": 2,
        }
    )
    # letters = random.choices(
    #     list(counts.keys()),
    #     weights=list(counts.values()),
    #     k=n,
    # )
    letters = list(counts.elements())
    random.shuffle(letters)
    letters = letters[:n]
    print(f"random letters are {(''.join(sorted(letters)))!r}")
    return letters


def make_letters(args, words: Iterable[str]) -> list[str]:
    if args.random_letters:
        return make_random_letters(args.random_letters, words)
    elif args.letters:
        return args.letters.strip().upper()
    else:
        raise ValueError("Either --letters or --random_letters must be specified.")


def main():
    args = parse_args()

    if args.random_seed:
        random.seed(args.random_seed)

    words = [
        validate_word(word)
        for line in args.words
        for word in line.split()
        if line.strip()
    ]
    letters = make_letters(args, words)

    board = Board.from_str(args.start) if args.start else Board([])

    search = BeamSearch(
        words,
        SimpleConstraintGenerator(words),
        beam_size=args.beam_size,
        max_depth=args.max_depth,
    )
    try:
        result = search.search(board, letters)
        print("Solved board:")
        print(result)
    except BeamSearch.SearchError as e:
        print(f"No solution found: {e}")


if __name__ == "__main__":
    main()
