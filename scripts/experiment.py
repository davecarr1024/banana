import argparse
import random
import time
from abc import ABC, abstractmethod
from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Optional, override

from tabulate import tabulate

from banana.board import Board
from banana.reasoning import Search
from banana.reasoning.generators import SimpleConstraintGenerator
from banana.reasoning.searches import BeamSearch
from banana.validation import validate_letter, validate_word


def parse_args():
    parser = argparse.ArgumentParser(description="Run banana experiments.")
    parser.add_argument(
        "--words",
        type=str,
        required=True,
        nargs="+",
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
        "--random_letter_samples",
        type=int,
        default=1,
        help="Number of random letter samples to generate.",
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
        default=[10],
        nargs="+",
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
        default=[0],
        nargs="+",
        help="Maximum depth for beam search. 0 to disable.",
    )
    parser.add_argument(
        "--remaining_letters_weight",
        type=float,
        default=[-2],
        nargs="+",
        help="Heuristic weight for the number of remaining letters.",
    )
    parser.add_argument(
        "--board_size_weight",
        type=float,
        default=[1],
        nargs="+",
        help="Heuristic weight for the size of the board.",
    )
    parser.add_argument(
        "--average_word_length_weight",
        type=float,
        default=[1],
        nargs="+",
        help="Heuristic weight for the average word length.",
    )
    parser.add_argument(
        "--constraints_weight",
        type=float,
        default=[-1],
        nargs="+",
        help="Heuristic weight for the number of constraints.",
    )
    parser.add_argument(
        "--letter_rarity_weight",
        type=float,
        default=[1.5],
        nargs="+",
        help="Heuristic weight for the rarity of letters.",
    )
    return parser.parse_args()


class LetterGenerator(ABC):
    @abstractmethod
    def generate(self) -> list[tuple[str, ...]]: ...

    @staticmethod
    def from_args(args: argparse.Namespace) -> "LetterGenerator":
        if args.random_letters:
            return RandomLetterGenerator(
                args.random_letters,
                args.random_letter_samples,
            )
        elif args.letters:
            return FixedLetterGenerator(args.letters)
        else:
            raise ValueError("Either --letters or --random_letters must be specified.")


@dataclass(frozen=True)
class FixedLetterGenerator(LetterGenerator):
    letters: list[str]

    @override
    def generate(self) -> list[tuple[str, ...]]:
        return [tuple(map(validate_letter, self.letters))]


@dataclass(frozen=True)
class RandomLetterGenerator(LetterGenerator):
    num_letters: int
    samples: int

    @override
    def generate(self) -> list[tuple[str, ...]]:
        print(f"generating {self.samples} samples of {self.num_letters} random letters")
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
                "Q": 2,
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
        assert self.num_letters <= counts.total()
        letters = list(counts.elements())

        def make_random_letters() -> tuple[str, ...]:
            random.shuffle(letters)
            return tuple(letters[: self.num_letters])

        return [make_random_letters() for _ in range(self.samples)]


@dataclass(frozen=True)
class Experiment:
    search: Search
    letter_sets: list[tuple[str, ...]]
    board: Board
    words_filename: str

    def run(self) -> Iterable["Result"]:
        print(
            f"running experiment for search {self.search} "
            f"with words {self.words_filename} "
            # f"and letter sets {[''.join(letters) for letters in self.letter_sets]}"
        )
        for letters in self.letter_sets:
            start = time.time()
            try:
                result = self.search.search(self.board, letters)
                success = True
            except RuntimeError:
                result = None
                success = False
            yield Result(
                success=success,
                elapsed_time=time.time() - start,
                board=result,
                letter_set=letters,
            )

    @override
    def __str__(self) -> str:
        s = "Experiment:\n"
        if self.board:
            s += f"\tboard={self.board}\n"
        s += f"\tsearch={self.search}\n"
        s += f"\tletter_sets={[''.join(letters) for letters in self.letter_sets]}\n"
        return s


@dataclass(frozen=True)
class Result:
    success: bool
    elapsed_time: float
    board: Optional[Board]
    letter_set: tuple[str, ...]

    @override
    def __str__(self) -> str:
        s = "Result:\n"
        s += f"\tletter_set={''.join(self.letter_set)}\n"
        if self.board is not None:
            s += str(self.board)
        s += f"\tsuccess={self.success}\n"
        s += f"\telapsed_time={self.elapsed_time:.2f}s\n"
        return s


def run_experiments(
    experiments: list[Experiment],
) -> Iterable[tuple[Experiment, list[Result]]]:
    for experiment in experiments:
        yield experiment, list(experiment.run())


@dataclass(frozen=True)
class Summary:
    search: str
    words_filename: str
    samples: int
    success_rate: float
    average_time: float


def run_and_summarize_results(experiments: list[Experiment]) -> None:
    summaries = list[Summary]()
    for experiment, results in run_experiments(experiments):
        print(f"{experiment}")
        for result in results:
            print(f"{result}")
        success_count = sum(1 for result in results if result.success)
        success_percent = success_count / len(results) * 100
        print(f"Success rate: {success_percent:.2f}% ({success_count}/{len(results)})")
        average_time = sum(result.elapsed_time for result in results) / len(results)
        print(f"Total time: {sum(result.elapsed_time for result in results):.2f}s")
        print(f"Average time: {average_time:.2f}s")
        summaries.append(
            Summary(
                search=str(experiment.search),
                samples=len(results),
                success_rate=success_percent,
                words_filename=experiment.words_filename,
                average_time=average_time,
            )
        )
    print(
        tabulate(
            [s.__dict__ for s in summaries],
            headers="keys",
            floatfmt=".2f",
            tablefmt="grid",
        )
    )


def main() -> None:
    args = parse_args()
    if args.random_seed:
        random.seed(args.random_seed)
    letter_generator = LetterGenerator.from_args(args)
    letter_sets = letter_generator.generate()
    board = Board.from_str(args.start) if args.start else Board([])
    word_sets: dict[str, list[str]] = {
        words_filename: [
            validate_word(word) for word in open(words_filename, "r").read().split()
        ]
        for words_filename in args.words
    }
    experiments = [
        Experiment(search, letter_sets, board, words_filename)
        for words_filename, words in word_sets.items()
        for search in [
            BeamSearch(
                words,
                SimpleConstraintGenerator(words),
                beam_size=beam_size,
                max_depth=max_depth,
                remaining_letters_weight=remaining_letters_weight,
                board_size_weight=board_size_weight,
                average_word_length_weight=average_word_length_weight,
                constraints_weight=constraints_weight,
                letter_rarity_weight=letter_rarity_weight,
            )
            for beam_size in args.beam_size
            for max_depth in args.max_depth
            for remaining_letters_weight in args.remaining_letters_weight
            for board_size_weight in args.board_size_weight
            for average_word_length_weight in args.average_word_length_weight
            for constraints_weight in args.constraints_weight
            for letter_rarity_weight in args.letter_rarity_weight
        ]
    ]
    run_and_summarize_results(experiments)


if __name__ == "__main__":
    main()
