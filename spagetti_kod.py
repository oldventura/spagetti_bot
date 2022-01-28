import praw
import pdb
import os
import sys
import time
import openai
import hashlib
import random
import deep_translator
from deep_translator import GoogleTranslator

client_id = ""
client_secret = ""
username = ""
password = ""
user_agent = f"User-Agent: linux:com.{username}s.runner:v1.0 (by /u/{username}s)"

reddit = praw.Reddit(client_id = client_id,
                     client_secret = client_secret,
                     username = username,
                     password = password,
                     user_agent = user_agent)

openai.api_key = ""
completion = openai.Completion()

start_chat_log = ""

forbidden_comments = ['[removed]', '[deleted]', '', ' ', None, 'Erpasment']

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

trans = lambda x: x.translate(non_bmp_map)

def ask(question, chat_log=None):
    sampleList = ["davinci", "ada", "babbage", "curie"]
    person = "text-davinci-001"
    if chat_log is None:
        chat_log = start_chat_log
    prompt = f'{chat_log}Human: {question}\nAI:'
    response = completion.create(
        prompt=prompt, engine=person, stop=['\nHuman'], temperature=0.5,
        top_p=1, frequency_penalty=1, presence_penalty=0.4, best_of=1,
        max_tokens=800)
    answer = response.choices[0].text.strip()
    if "\nAI:" in answer:
        answer = answer.split("\nAI:")[0]
    if "Human:" in answer:
        answer = answer.split("Human:")[0]
    return answer

def slangify(text):
    sent = text.split(".")
    slang = [" amk."," aq."]
    cons = ""
    for i in sent:
        if random.random() < 0.9:
            cons += i+"."
        else:
            cons += i+random.choice(slang)+"."
            print("Sucsessfully planted swear word!")
    cons = cons.replace(","," ").lower()
    cons = cons.replace("..",".")
    cons = cons.replace("?.","?")
    cons = cons.replace("!.","!")
    return cons.replace("  "," ")

if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []
else:
    with open("posts_replied_to.txt", "r") as f:
       posts_replied_to = f.read()
       posts_replied_to = posts_replied_to.split("\n")
       posts_replied_to = list(filter(None, posts_replied_to))


tr2en = GoogleTranslator(source='tr', target='en')
en2tr = GoogleTranslator(source='en', target='tr')

print("Initializing...")
subreddit = reddit.subreddit("kgbtr")

begin = time.monotonic()-500

while True:
    try:
        if round(time.monotonic()-begin) > 500:
            begin = time.monotonic()
            for i in subreddit.new(limit=1):
                if i.author not in forbidden_comments and not i.over_18 and i.id not in posts_replied_to:
                    print("Replying to:",trans(i.title))
                    if i.selftext not in forbidden_comments:
                        arranger = str(i.title)+"\n"+str(i.selftext)
                    else:
                        arranger = str(i.title)+"\n"
                    arranger = arranger.lower()
                    arranger = arranger.replace("aq", "amk")
                    arranger = arranger.replace("amk", "amına koyayım")
                    arranger = arranger.replace(" oc", " orospu çocuğu")
                    arranger = arranger.replace(" oç", " orospu çocuğu")
                    arranger = arranger.replace("sg", "siktir git")
                    arranger = arranger.replace(" bot", " yapay zeka")
                    arranger = arranger.replace("kes lan", "kapa çeneni")
                    arranger = tr2en.translate(arranger)
                    out = ask(arranger, None)
                    try: out = en2tr.translate(out).strip(".")
                    except AttributeError:
                        continue
                    except deep_translator.exceptions.NotValidPayload:
                        out = "..."
                        item.reply(out)
                        posts_replied_to.append(i.id)
                        continue
                    except deep_translator.exceptions.NotValidLength:
                        out = "Bu ne amk çok uzun"
                        item.reply(out)
                        posts_replied_to.append(i.id)
                        continue
                    out = out.replace("girişiniz için teşekkür ederiz","geri dönütünüz için teşekkür ederiz")
                    out = out.replace("ai ", "yapay zeka ")
                    out = out.replace("numara", "hayır")
                    out = slangify(out.replace("Numara", "Hayır"))
                    posts_replied_to.append(i.id)
                    i.reply(out)

        if round(time.monotonic()-begin) > 100:
            for item in reddit.inbox.unread(limit=None):
                print("Replying to:",trans(item.body))
                if "good bot" in item.body.lower():
                    item.reply("Sende iyi insansın amk")
                elif "bad bot" in item.body.lower():
                    item.reply("Kes lan amk soran mı oldu >:/")
                else:
                    try:
                        prev = "AI: "+tr2en.translate(mail.parent().body)+"\n"
                    except:
                        prev = None


                    arranger = item.body.lower()
                    arranger = arranger.replace("aq", "amk")
                    arranger = arranger.replace("amk", "amına koyayım")
                    arranger = arranger.replace(" oc", " orospu çocuğu")
                    arranger = arranger.replace(" oç", " orospu çocuğu")
                    arranger = arranger.replace("amk", "amına koyayım")
                    arranger = arranger.replace("sg", "siktir git")
                    arranger = arranger.replace(" bot", " yapay zeka")
                    arranger = arranger.replace("kes lan", "kapa çeneni")
                    arranger = tr2en.translate(arranger)
                    out = ask(arranger, prev)
                    try: out = en2tr.translate(out).strip(".")
                    except AttributeError:
                        item.mark_read()
                        time.sleep(5)
                        continue
                    except deep_translator.exceptions.NotValidPayload:
                        out = "..."
                        item.reply(out)
                        item.mark_read()
                        continue
                    except deep_translator.exceptions.NotValidLength:
                        out = "Bu ne amk çok uzun"
                        item.reply(out)
                        item.mark_read()
                        continue
                    out = out.replace("numara", "hayır")
                    out = out.replace("girişiniz için teşekkür ederiz","geri dönütünüz için teşekkür ederiz")
                    out = out.replace("ai ", "yapay zeka ")
                    #time.sleep(15) #rate-limit?
                    item.reply(slangify(out))
                item.mark_read()
    except praw.exceptions.RedditAPIException:
        pass
    except Exception as e:
        print(e)

    with open("posts_replied_to.txt", "w") as f:
        if len(posts_replied_to) > 0:
            print("Saving Replied Posts...")
            to_remove = []
            for post_id in posts_replied_to:
                f.write(post_id + "\n")
                to_remove.append(post_id)
            for post_id in to_remove:
                posts_replied_to.remove(post_id)
