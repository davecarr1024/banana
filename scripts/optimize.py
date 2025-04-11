import argparse
import random
from typing import Callable

import optuna

from banana.board import Board
from banana.reasoning.generators import SimpleConstraintGenerator
from banana.reasoning.searches import BeamSearch
from banana.validation import validate_word

from .experiment import Experiment, RandomLetterGenerator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run banana experiments.")
    parser.add_argument(
        "--words",
        type=str,
        required=True,
        help="Path to a file containing valid words.",
    )
    parser.add_argument(
        "--num_trials",
        type=int,
        help="Number of trials to run.",
        default=100,
    )
    parser.add_argument(
        "--random_seed",
        type=int,
        default=0,
        help="Random seed for reproducibility. 0 to disable.",
    )
    parser.add_argument(
        "--random_letters",
        type=int,
        required=True,
        help="Number of random letters to generate (e.g., 7).",
    )
    parser.add_argument(
        "--random_letter_samples",
        type=int,
        required=True,
        help="Number of random letter samples to generate.",
    )
    parser.add_argument(
        "--failure_rate_weight",
        type=float,
        default=1000,
        help="Weight for failure rate in objective function.",
    )
    parser.add_argument(
        "--total_time_weight",
        type=float,
        default=1,
        help="Weight for total time in objective function.",
    )
    parser.add_argument(
        "--beam_size",
        type=int,
        nargs=2,
        default=[1, 25],
        help="Range for beam size in objective function.",
    )
    parser.add_argument(
        "--remaining_letters_weight",
        type=float,
        nargs=2,
        default=[-1, 1],
        help="Range for remaining letters weight in objective function.",
    )
    parser.add_argument(
        "--board_size_weight",
        type=float,
        nargs=2,
        default=[-1, 1],
        help="Range for board size weight in objective function.",
    )
    parser.add_argument(
        "--average_word_length_weight",
        type=float,
        nargs=2,
        default=[-1, 1],
        help="Range for average word length weight in objective function.",
    )
    parser.add_argument(
        "--constraints_weight",
        type=float,
        nargs=2,
        default=[-1, 1],
        help="Range for constraints weight in objective function.",
    )
    parser.add_argument(
        "--letter_rarity_weight",
        type=float,
        nargs=2,
        default=[-1, 1],
        help="Range for letter rarity weight in objective function.",
    )
    return parser.parse_args()


def suggest_flag_int(
    args: argparse.Namespace, trial: optuna.trial.Trial, name: str
) -> int:
    """Suggest an int flag value based on a flag range."""
    vals: tuple[int, int] = vars(args)[name]  # type:ignore
    return trial.suggest_int(name, *vals)


def suggest_flag_float(
    args: argparse.Namespace, trial: optuna.trial.Trial, name: str
) -> float:
    """Suggest a float flag value based on a flag range."""
    vals: tuple[float, float] = vars(args)[name]  # type:ignore
    return trial.suggest_float(name, *vals)


def objective(
    args: argparse.Namespace,
    words: list[str],
) -> Callable[[optuna.trial.Trial], float]:
    def _objective(trial: optuna.trial.Trial) -> float:
        experiment = Experiment(
            board=Board([]),
            letter_sets=RandomLetterGenerator(
                args.random_letters,
                args.random_letter_samples,
            ).generate(),
            words_filename=args.words,
            search=BeamSearch(
                constraint_generator=SimpleConstraintGenerator(words),
                words=words,
                beam_size=suggest_flag_int(
                    args,
                    trial,
                    "beam_size",
                ),
                remaining_letters_weight=suggest_flag_float(
                    args,
                    trial,
                    "remaining_letters_weight",
                ),
                board_size_weight=suggest_flag_float(
                    args,
                    trial,
                    "board_size_weight",
                ),
                average_word_length_weight=suggest_flag_float(
                    args,
                    trial,
                    "average_word_length_weight",
                ),
                constraints_weight=suggest_flag_float(
                    args,
                    trial,
                    "constraints_weight",
                ),
                letter_rarity_weight=suggest_flag_float(
                    args,
                    trial,
                    "letter_rarity_weight",
                ),
            ),
        )
        results = list(experiment.run())
        failure_rate = sum(not result.success for result in results) / len(results)
        total_time = sum(result.elapsed_time for result in results)
        score = (
            failure_rate * args.failure_rate_weight
            + total_time * args.total_time_weight
        )
        print(
            f"Trial {trial.number}\n"
            f"\tfailure_rate: {failure_rate:.2f}\n"
            f"\ttotal_time: {total_time:.2f}\n"
            f"\tscore: {score:.2f}\n"
        )
        return score

    return _objective


def main() -> None:
    args = parse_args()

    if args.random_seed:
        random.seed(args.random_seed)

    with open(args.words, "r") as f:
        words = [validate_word(word) for word in f.read().split()]

    study = optuna.create_study()
    study.optimize(
        objective(args, words),
        n_trials=args.num_trials,
    )

    print(f"Best params: {study.best_params}")


if __name__ == "__main__":
    main()
