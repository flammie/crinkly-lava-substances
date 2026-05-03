#!/bin/env - python3
"""Minimalistic hangman word game."""
import random
from argparse import ArgumentParser


def main():
    """Main CLI for hangman."""
    argp = ArgumentParser()
    argp.add_argument("-i", "--input", metavar="INFILE", dest="infile",
                      type=open, help="read words from INFILE", required=True)
    argp.add_argument("-v", "--verbose", action="store_true",
                      help="print verbosely while processing")
    options = argp.parse_args()
    puzzles = []
    if options.verbose:
        print(f"Reading words from {options.infile.name}")
    skip_headers = True
    for line in options.infile:
        if skip_headers:
            skip_headers = False
            continue
        fields = line.rstrip().split("\t")
        word = fields[0]
        if len(fields) > 1:
            hint = fields[1]
        else:
            hint = None
        if len(fields) > 2:
            explanation = fields[2]
        else:
            explanation = None
        puzzles.append({"word": word, "hint": hint, "explanation":
                        explanation})
    if options.verbose:
        print(f"{len(puzzles)} words read")
    correct = 0
    deads = 0
    wounds = 0
    riddle = random.choice(puzzles)
    guessed = set()
    wordsguessed = set()
    print("Guess a letter or write quit to give up:")
    while puzzles:
        if riddle["hint"]:
            print(f"hint: {riddle["hint"]}")
        if wounds > 0:
            print(f"{wounds}/8 wrong guesses used")
        if guessed:
            print("Letters guessed:",
                  " ".join(guessed))
        if wordsguessed:
            print("Words guessed:",
                  ", ".join(wordsguessed))
        for c in riddle["word"]:
            if c in guessed:
                print(c, end=" ")
            else:
                print("_", end=" ")
        answer = input("? ")
        if answer == "quit":
            break
        elif answer == riddle["word"]:
            print(f"{answer} is correct!")
            correct += 1
            puzzles.remove(riddle)
            if not puzzles:
                break
            riddle = random.choice(puzzles)
            guessed.clear()
            wordsguessed.clear()
            wounds = 0
        elif len(answer) == 1:
            if answer in riddle["word"]:
                hits = riddle["word"].count(answer)
                print(f"{hits} hits for {answer}")
            else:
                print(f"{answer} is not in the word")
                wounds += 1
            guessed.add(answer)
        else:
            print(f"{answer} is not correct")
            wounds += 1
            wordsguessed.add(answer)
        if wounds >= 8:
            print("you were hung")
            print(f"correct word was {riddle["word"]}")
            deads += 1
            puzzles.remove(riddle)
            if not puzzles:
                break
            riddle = random.choice(puzzles)
            guessed.clear()
            wordsguessed.clear()
            wounds = 0
    if deads == 0:
        print("perfect game.")
    else:
        print("You got hanged {deads} times")


if __name__ == "__main__":
    main()
