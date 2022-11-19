import datetime
import json
import os
import pickle
import random
from http import HTTPStatus

import requests
from dotenv import load_dotenv

load_dotenv()


class SentenceGenerator:
    MONTH_REQUESTS_LIMIT = 1000

    @staticmethod
    def _get_sentence_from_api(tense, objnum, subj_verb_obj_triple):
        url = "https://linguatools-sentence-generating.p.rapidapi.com/realise"
        headers = {
            "X-RapidAPI-Key": os.environ.get("RAPID_API_KEY", "SIGN-UP-FOR-KEY"),
            "X-RapidAPI-Host": "linguatools-sentence-generating.p.rapidapi.com"
        }
        subj, verb, obj = subj_verb_obj_triple
        querystring = {
            "object": obj,
            "subject": subj,
            "verb": verb,
            "tense": tense,
            "objnum": objnum,
            "passive": "passive",
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == HTTPStatus.OK:
            response = response.json()
            if response.get("result") == "OK":
                sentence = response.get("sentence")
                return sentence

    @staticmethod
    def _get_sentence_from_file(tense, objnum):
        with open("sentences.json", "r", encoding="utf-8") as sentences_file:
            sentences_list = json.load(sentences_file)
            sentence = random.choice(sentences_list[f"{tense}_{objnum}"])
            return sentence

    @staticmethod
    def _get_subj_verb_obj_triple():
        with open("subj_verb_obj_triples.json", "r", encoding="utf-8") as subj_verb_obj_triples_file:
            subj_verb_obj_triple = json.load(subj_verb_obj_triples_file)
            subj_verb_obj_triple = random.choice(subj_verb_obj_triple)
            return subj_verb_obj_triple

    @staticmethod
    def _check_expiration_requests():
        with open("requests.pickle", "rb+") as requests_file:
            requests_deque = pickle.load(requests_file)
            if requests_deque:
                while requests_deque[0] + datetime.timedelta(days=31) >= datetime.datetime.now():
                    requests_deque.popleft()
                    if not requests_deque:
                        break
                requests_file.seek(0)
                pickle.dump(requests_deque, requests_file)

    def get_sentence(self, tense, objnum, subj_verb_obj_triple=None):
        self._check_expiration_requests()
        with open("requests.pickle", "rb+") as requests_file:
            requests_list = pickle.load(requests_file)
            if len(requests_list) < self.MONTH_REQUESTS_LIMIT:
                requests_list.append(datetime.datetime.now())
                requests_file.seek(0)
                pickle.dump(requests_list, requests_file)
                if not subj_verb_obj_triple:
                    subj_verb_obj_triple = self._get_subj_verb_obj_triple()
                sentence = self._get_sentence_from_api(tense, objnum, subj_verb_obj_triple)
                if sentence:
                    with open("sentences.json", "r+", encoding="utf-8") as sentences_file:
                        sentences_list = json.load(sentences_file)
                        sentences_list[f"{tense}_{objnum}"].append(sentence)
                        sentences_file.seek(0)
                        json.dump(sentences_list, sentences_file)
                    return sentence
            sentence = self._get_sentence_from_file(tense, objnum)
            return sentence
