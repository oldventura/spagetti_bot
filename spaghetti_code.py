#!/usr/bin/python
# -*- encoding:utf-8 -*-
import configparser
import os
import random
import sys
import time

import deep_translator
import openai
import praw
from deep_translator import GoogleTranslator


class Spaghetti_Monster:
    def __init__(self):
        # It is always wise to declare variables beforehand
        # to see the list of used variables.
        self.tr2en = None
        self.en2tr = None
        self.reddit = None
        self.subreddit = None

        self.start_chat_log = ""
        self.forbidden_comments = ['[removed]', '[deleted]', '', ' ', None]
        self.posts_replied_to = []

        self.completion = openai.Completion()
        self.non_bmp_map = dict.fromkeys(
            range(0x10000, sys.maxunicode + 1), 0xfffd)

        self.load_openai_config()
        self.load_replied_to()
        self.load_translators()
        self.load_reddit()

        self.begin = time.monotonic()-500

        print("Initializing...")

        # This runs the main loop function
        self.runner()

    def trans(self, x):
        return x.translate(self.non_bmp_map)

    def load_openai_config(self):
        # Function for loading up the openai key
        self.config = configparser.ConfigParser()
        self.config.read('openai.ini')
        if 'openai' not in self.config.sections():
            print("Error: 'openai.ini'")
            exit()
        openai.api_key = self.config['openai']['key']

    def load_replied_to(self):
        # Actually we just need one function to load up
        # 'posts_replied_to.txt' for both reading and
        # writing.
        #
        # This also creates the file if it does not
        # exist.
        self.replied_to = open("posts_replied_to.txt", "a+")
        self.replied_to.seek(0)
        content = self.replied_to.read().split("\n")
        self.posts_replied_to = list(filter(None, content))

        # This moves the cursor to the end of the file
        self.replied.seek(0, 2)

    def load_translators(self):
        self.tr2en = GoogleTranslator(source='tr', target='en')
        self.en2tr = GoogleTranslator(source='en', target='tr')

    def load_reddit(self):
        self.reddit = praw.Reddit(
            "kerbal_galactic",
            config_interpolation="basic"
        )
        self.subreddit = self.reddit.subreddit("kgbtr")

    def ask(self, question, chat_log=None):
        person = "text-davinci-001"
        if chat_log is None:
            chat_log = self.start_chat_log
        prompt = f'{chat_log}Human 1: {question}\nHuman 2:'
        response = self.completion.create(
            prompt=prompt, engine=person, stop=['\nHuman'], temperature=0.9,
            top_p=1, frequency_penalty=0, presence_penalty=0, best_of=1,
            max_tokens=150)
        answer = response.choices[0].text.strip()
        if "\nAI:" in answer:
            answer = answer.split("\nAI:")[0]
        if "Human 1:" in answer:
            answer = answer.split("Human 1:")[0]
        if "Human 2:" in answer:
            answer = answer.split("Human 2:")[0]
        if "Human:" in answer:
            answer = answer.split("Human:")[0]
        return answer

    def slangify(self, text):
        sent = text.split(".")
        if len(sent) < 2:
            return "".join(sent)
        slang = [" amk.", " aq."]
        cons = ""
        for i in sent:
            if random.random() < 0.9:
                cons += i+"."
            else:
                cons += i+random.choice(slang)+"."
                print("Successfully planted swear word!")
        cons = cons.replace(",", " ").lower()
        cons = cons.replace("..", ".")
        cons = cons.replace("?.", "?")
        cons = cons.replace("!.", "!")
        return cons.replace("  ", " ")

    def runner(self):
        # Actual Main Function
        while True:
            try:
                if round(time.monotonic()-begin) > 500:
                    begin = time.monotonic()
                    for i in self.subreddit.new(limit=1):
                        if i.author not in self.forbidden_comments and not i.over_18 and i.id not in self.posts_replied_to:
                            print("Replying to:", self.trans(i.title))
                            if i.selftext not in self.forbidden_comments:
                                arranger = str(i.title)+"\n"+str(i.selftext)
                            else:
                                arranger = str(i.title)+"\n"
                            arranger = arranger.lower()
                            arranger = arranger.replace("aq", "amk")
                            arranger = arranger.replace("amk", "amına koyayım")
                            arranger = arranger.replace(
                                " oc", " orospu çocuğu")
                            arranger = arranger.replace(
                                " oç", " orospu çocuğu")
                            arranger = arranger.replace("sg", "siktir git")
                            arranger = arranger.replace(" bot", " yapay zeka")
                            arranger = arranger.replace(
                                "kes lan", "kapa çeneni")
                            arranger = self.tr2en.translate(arranger)
                            out = self.ask(arranger, None)
                            try:
                                out = self.en2tr.translate(out).strip(".")
                            except AttributeError:
                                continue
                            except deep_translator.exceptions.NotValidPayload:
                                out = ". . ."
                                item.reply(out)
                                self.posts_replied_to.append(i.id)
                                continue
                            except deep_translator.exceptions.NotValidLength:
                                out = "##bu ne amk çok uzun"
                                item.reply(out)
                                self.posts_replied_to.append(i.id)
                                continue
                            out = out.lower()
                            out = out.replace(
                                "girişiniz için teşekkür ederiz", "geri dönütünüz için teşekkür ederiz")
                            out = out.replace("ai ", "yapay zeka ")
                            out = out.replace(" ai", " yapay zeka")
                            out = out.replace("numara", "hayır")
                            out = self.slangify(out.replace("Numara", "Hayır"))
                            self.posts_replied_to.append(i.id)
                            i.reply(out)

                if round(time.monotonic()-begin) > 100:
                    for item in self.reddit.inbox.unread(limit=None):
                        print("Replying to:", self.trans(item.body))
                        if "good bot" in item.body.lower():
                            item.reply("sende iyi insansın amk")
                        elif "bad bot" in item.body.lower():
                            item.reply("kes lan amk soran mı oldu >:/")
                        else:
                            try:
                                prev = "Human 1: " + \
                                    self.tr2en.translate(
                                        mail.parent().body)+"\n"
                            except:
                                prev = None

                            arranger = item.body.lower()
                            arranger = arranger.replace("aq", "amk")
                            arranger = arranger.replace("amk", "amına koyayım")
                            arranger = arranger.replace(
                                " oc", " orospu çocuğu")
                            arranger = arranger.replace(
                                " oç", " orospu çocuğu")
                            arranger = arranger.replace("amk", "amına koyayım")
                            arranger = arranger.replace("sg", "siktir git")
                            arranger = arranger.replace(" bot", " yapay zeka")
                            arranger = arranger.replace(
                                "kes lan", "kapa çeneni")
                            arranger = self.tr2en.translate(arranger)
                            out = self.ask(arranger, prev)
                            try:
                                out = self.en2tr.translate(out).strip(".")
                            except AttributeError:
                                item.mark_read()
                                time.sleep(5)
                                continue
                            except deep_translator.exceptions.NotValidPayload:
                                out = ". . ."
                                item.reply(out)
                                item.mark_read()
                                continue
                            except deep_translator.exceptions.NotValidLength:
                                out = "##bu ne amk çok uzun"
                                item.reply(out)
                                item.mark_read()
                                continue
                            out = out.lower()
                            out = out.replace("numara", "hayır")
                            out = out.replace("ai ", "yapay zeka ")
                            out = out.replace(" ai", " yapay zeka")
                            out = out.replace(
                                "girişiniz için teşekkür ederiz", "geri dönütünüz için teşekkür ederiz")
                            time.sleep(15)
                            item.reply(self.slangify(out))
                        item.mark_read()

            except praw.exceptions.RedditAPIException as e:
                print(str(e))
            except Exception as e:
                print(str(e))

            # Add replied comments I guess
            if len(self.posts_replied_to) > 0:
                to_remove = []
                for post_id in self.posts_replied_to:
                    self.replied_to.write(post_id + "\n")
                    to_remove.append(post_id)
