import requests
from bs4 import BeautifulSoup
import string
import re


def caesar(text, step):

    def shift_alphabet(alphabet):
        return alphabet[step:] + alphabet[:step]

    alphabets = (string.ascii_lowercase, string.ascii_uppercase, string.digits)
    shifted_alphabets = tuple(map(shift_alphabet, alphabets))
    joined_aphabets = ''.join(alphabets)
    joined_shifted_alphabets = ''.join(shifted_alphabets)
    table = str.maketrans(joined_aphabets, joined_shifted_alphabets)
    return text.translate(table)


def remove_residues(s):
    return re.sub('=a.*?#?\?','',s, flags=re.DOTALL)
    #return re.sub('=a.*?=9a\?','',s, flags=re.DOTALL)

def make_pretty(s):
    s=s.replace("=strong?", "")
    s=s.replace("=strong 9?", "")
    s=s.replace("=9strong?", "")
    s=s.replace("=9a?", "")

    s=s.replace("{", "z")
    s=s.replace(")", "(")
    s=s.replace("*", ")")

    s=s.replace("-", "~§")
    s=s.replace(",", "-")
    s=s.replace("~§", ",")

    s=s.replace("@", "?")
    s=s.replace(".", "-")
    s=s.replace("/", ".")
    s=s.replace(":", "9")
    s=s.replace(";", ":")
    s=s.replace("[", "Z")
    s=s.replace("÷", "ö")
    s=s.replace("ý", "ü")
    s=s.replace("Ý", "Ü")

    s=s.replace("à", "ß")
    s=s.replace("å", "ä")

    return s



def get_paragraphs(soup):
    return [f.get_text() for f in soup.select('p[class*="rticle__paragraph"]')]



def decode(URL, shift=-1):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.title.string

    description = soup.find("meta",  property="og:description").get("content")

    paragraphs = get_paragraphs(soup)

    decoded = [caesar(p, shift) for p in paragraphs]
    decoded = [make_pretty(d) for d in decoded]
    decoded = [remove_residues(d) for d in decoded]

    print(title, "\n")
    print(description, "\n")
    for d in decoded:
        print(d, "\n")
