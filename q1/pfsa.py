import argparse
import pytest
import json


def construct(file_str: str) -> dict[str, dict[str, float]]:
    """Takes in the string representing the file and returns pfsa
    The given example is for the statement "A cat"
    """
    file_str = file_str.lower()

    trie = dict()
    trie["*"] = dict()
    for word in file_str.split():
        if word[0:1] not in trie:
            trie["*"][word[0:1]] = 1
            trie[word[0:1]] = dict()
        else:
            trie["*"][word[0:1]] += 1

        for i in range(2, len(word) + 1):
            if word[:i] not in trie:
                trie[word[:i]] = dict()
                trie[word[: i - 1]][word[:i]] = 1
            else:
                trie[word[: i - 1]][word[:i]] += 1

        if word not in trie:
            trie[word] = dict()
        trie[word][word + "*"] = 1

    for prefix in trie:
        count = 0
        for key in trie[prefix]:
            count += trie[prefix][key]
        for key in trie[prefix]:
            trie[prefix][key] /= count

    return trie


#     # TODO: FILE IN THIS FUNCTION
#     return {
#         "*": {"a": 0.5, "c": 0.5},
#         "a": {"a*": 1.0},
#         "c": {"ca": 1.0},
#         "ca": {"cat": 1.0},
#         "cat": {"cat*": 1.0},
#     }


def main():
    """
    The command for running is `python pfsa.py text.txt`. This will generate
    a file `text.json` which you will be using for generation.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="Name of the text file")
    args = parser.parse_args()

    with open(args.file, "r") as file:
        contents = file.read()
        output = construct(contents)

    name = args.file.split(".")[0]

    with open(f"{name}.json", "w") as file:
        json.dump(output, file)


if __name__ == "__main__":
    main()


STRINGS = ["A cat", "A CAT", "", "A", "A A A A"]
DICTIONARIES = [
    {
        "*": {"a": 0.5, "c": 0.5},
        "a": {"a*": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
    {
        "*": {"a": 0.5, "c": 0.5},
        "a": {"a*": 1.0},
        "c": {"ca": 1.0},
        "ca": {"cat": 1.0},
        "cat": {"cat*": 1.0},
    },
    {
        "*": {},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
    {
        "*": {"a": 1.0},
        "a": {"a*": 1.0},
    },
]


@pytest.mark.parametrize("string, pfsa", list(zip(STRINGS, DICTIONARIES)))
def test_output_match(string, pfsa):
    """
    To test, install `pytest` beforehand in your Python environment.
    Run `pytest pfsa.py` Your code must pass all tests. There are additional
    hidden tests that your code will be tested on during VIVA.
    """
    result = construct(string)
    print(result)

    assert result == pfsa
