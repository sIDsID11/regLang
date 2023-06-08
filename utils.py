from itertools import chain, combinations


def powerset(s: set) -> set[tuple]:
    s_list = list(s)
    ps = set(chain.from_iterable(combinations(s_list, r) for r in range(len(s_list) + 1)))
    ps = set(frozenset(x) for x in ps)
    return ps


       


if __name__ == "__main__":
    print(powerset({1, 2, 3}))