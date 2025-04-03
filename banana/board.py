# from collections.abc import Mapping, MutableMapping
# from typing import Iterable, override


# class Board(MutableMapping[tuple[int, int], str]):

#     class Error(Exception): ...

#     class ValueError(Error, ValueError): ...

#     class KeyError(Error, KeyError): ...

#     @staticmethod
#     def _validate_value(value: str) -> None:
#         if len(value) != 1:
#             raise Board.ValueError(f"Value must be a single character, not {value!r}")

#     def __init__(self, chars: Mapping[tuple[int, int], str]) -> None:
#         for value in chars.values():
#             Board._validate_value(value)
#         self._chars = chars

#     @override
#     def __getitem__(self, key: tuple[int, int]) -> str:
#         return self._chars.get(key, " ")

#     @override
#     def __setitem__(self, key: tuple[int, int], value: str) -> None:
#         Board._validate_value(value)
#         self._chars[key] = value

#     @override
#     def __delitem__(self, key: tuple[int, int]) -> None:
#         del self._chars[key]

#     def get_words(self) -> Iterable[str]:
#         raise NotImplementedError()
#         # words = list[str]()
#         # traversed_positions = set[tuple[int, int]]()

#         # def _traverse_and_add(
#         #     position: tuple[int, int],
#         #     direction: tuple[int, int],
#         #     add_operator: Callable[[str], str],
#         #     word: str,
#         # ) -> str:
#         #     raise NotImplementedError()

#         # for position, value in self._chars.items():
#         #     if position in traversed_positions:
#         #         continue
#         #     traversed_positions.add(position)
#         #     raise NotImplementedError()

#         # return words
