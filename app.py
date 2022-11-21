import sys
from time import sleep

import spacy
from textacy.extract import subject_verb_object_triples

from colorizer import Color
from sentence_generator import SentenceGenerator

C = Color()
gen = SentenceGenerator()
nlp = spacy.load("en_core_web_sm")


def get_input_sentences_for_change_restriction():
    return (C.FG.red(C.border(" Important! ")) + C.italic(C.bold(" PassiveVoicer")) +
            " can only work with sentences with " + C.reverse("SVO" + C.FG.lightgrey("MPT")) +
            " word order " + C.FG.lightgrey(f"(subject, verb, object, ") +
            C.FG.darkgrey("manner, place, time") + C.FG.lightgrey(")."))


def get_input_sentences_for_tense_restriction():
    return (C.FG.red(C.border(' Important! ')) + C.italic(C.bold(" PassiveVoicer")) +
            " can only work with sentences with " + C.reverse('one grammatical basis') + ".")


def get_welcome_message():
    return ("Hi, I'm " + C.bold(C.bold(C.FG.purple("PassiveVoicer "))) +
            "— an assistant in working with passive voice.")


def get_options():
    return (C.bold("Choose one of my options:\n") + C.FG.lightgreen(" 0. ") +
            "Shut down the program.\n" + C.FG.lightgreen(" 1. ") +
            "Get a sentence in a passive voice.\n" + C.FG.lightgreen(" 2. ") +
            "Identify if a sentence is in a passive voice or not.\n" + C.FG.lightred(" 3. ") +
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


def identify_passive_handler():
    sentence = input(C.bold("Enter sentence: ")).strip()
    if sentence[-1] != ".":
        sentence += "."
    doc = nlp(sentence)
    subj_verb_obj_triples = list(subject_verb_object_triples(doc))
    if not subj_verb_obj_triples:
        sentence = sentence.replace(".", " by zombies.")
        doc = nlp(sentence)
        subj_verb_obj_triples = list(subject_verb_object_triples(doc))
    if subj_verb_obj_triples:
        triple = subj_verb_obj_triples[0]
        auxiliary_verbs, action_verb = triple.verb[:-1], triple.verb[-1]
        if action_verb.tag_ == "VBN":
            tenses = {"past simple": {"was", "were"},
                      "present simple": {"am", "is", "are"},
                      "future simple": {"will", "shall", "be"},
                      "present progressive (continuous)": {"am", "is", "are", "being"},
                      "past progressive (continuous)": {"was", "were", "being"},
                      "past perfect": {"had", "been"},
                      "present perfect": {"have", "has", "been"},
                      "future perfect": {"will", "shall", "have", "been"}}
            sentence_tense = ""
            for tense in tenses:
                if set((verb.text.lower() for verb in auxiliary_verbs)).issubset(tenses[tense]):
                    sentence_tense = tense
                    break
            if sentence_tense:
                objnums = {"singular": {"NN", "NNP"}, "plural": {"NNS", "NNPS"}}
                sentence_objnum = ""
                for objnum in objnums:
                    if triple.subject[-1].text in objnums[objnum]:
                        sentence_objnum = objnum
                print()
                return (C.bold("This is a ") +
                        C.border(C.italic(" " + sentence_tense + " passive"
                                          + sentence_objnum + " ")) +
                        C.bold(" tense."))
    print()
    return C.bold("This is probably not a passive voice sentence.")


def main():
    print(get_welcome_message())
    while (choice := input(get_options()).strip()) != "0":
        if choice == "1":
            print(get_sentence_handler())
        elif choice == "2":
            print(get_input_sentences_for_tense_restriction())
            print(identify_passive_handler())
        print()
        sleep(1)
    sys.exit()


if __name__ == "__main__":
    main()
