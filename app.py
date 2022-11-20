import sys

from colorizer import Color
from sentence_generator import SentenceGenerator

C = Color()
gen = SentenceGenerator()


def get_input_sentences_restriction():
    return (C.FG.red(C.border(' Important! ')) + C.italic(C.bold(" PassiveVoicer")) +
            " can only work with sentences with " + C.reverse('SVO' + C.FG.lightgrey('MPT')) +
            " word order " + C.FG.lightgrey(f"(subject, verb, object, ") +
            C.FG.darkgrey("manner, place, time") + C.FG.lightgrey(")."))


def get_welcome_message():
    return ("Hi, I'm " + C.bold(C.bold(C.FG.purple("PassiveVoicer "))) +
            "— an assistant in working with passive voice.")


def get_options():
    return (C.bold("Choose one of my options:\n") + C.FG.lightgreen(" 0. ") +
            "Shut down the program.\n" + C.FG.lightgreen(" 1. ") +
            "Get a sentence in a passive voice.\n" + C.FG.lightgreen(" 2. ") +
            "Identify if a sentence is in the passive voice or not.\n" + C.FG.lightred(" 3. ") +
            C.strikethrough("Changing a sentence from active to passive voice.\n") +
            C.bold("Your choice? [0/1/2]: "))


def get_sentence_handler():
    while (tense := input(C.bold("Past, present or future tense? [pa/pr/fu]: "))[:2]) not in {"pa",
                                                                                              "pr",
                                                                                              "fu"}:
        pass
    tense_convert = {"pa": "past", "pr": "present", "fu": "future"}
    tense = tense_convert[tense]
    while (objnum := input(C.bold("Singular or plural? [s/p]: "))[:1]) not in {"s", "p"}:
        pass
    objnum_convert = {"s": "singular", "p": "plural"}
    objnum = objnum_convert[objnum]
    sentence = gen.get_sentence(tense, objnum)
    print()
    return (C.bold(f"{tense.capitalize()} tense, {objnum}, passive voice sentence example: ") +
            C.border(C.italic(" " + sentence + " ")))


def main():
    print(get_welcome_message())
    while (choice := input(get_options()).strip()) != "0":
        if choice == "1":
            print(get_sentence_handler())
        print()
    sys.exit()


if __name__ == "__main__":
    main()
