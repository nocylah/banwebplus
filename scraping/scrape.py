#!/usr/bin/python3

import re
import urllib.request

import lxml
import bs4
from bs4 import BeautifulSoup as BS

URL_INDEX = "http://banweb7.nmt.edu/pls/PROD/hwzkcrof.p_uncgslctcrsoff"
URL_SEARCH = "http://banweb7.nmt.edu/pls/PROD/hwzkcrof.P_UncgSrchCrsOff"

def write_data(term, subject, courses):
    print(term[1] + " " + subject[1] + " (" + str(len(courses)) + ")")

def match_course(tag):
    if tag.string != None:
        if re.match(r'[0-9]{5}', tag.string) != None:
            return True
    return False

def scrape_subject(page):
    courses = []
    for row in page.find_all(match_course):
        entry = []
        for i in range(0, 12):
            entry.append(row.string)
            row = row.next_sibling.next_sibling
        courses.append(entry)
    return courses

def scrape_term(term, subjects):
    global URL_SEARCH

    for subject in subjects:
        url = URL_SEARCH + \
                '?p_term=' + term[0] + \
                '&p_subj=' + re.sub(r'\s+', "%20", subject[0])
        page = BS(urllib.request.urlopen(url), "lxml")
        courses = scrape_subject(page)
        write_data(term, subject, courses)

def scrape_all():
    global URL_INDEX

    soup = BS(urllib.request.urlopen(URL_INDEX), "lxml")

    clean = lambda x: re.sub("\n", "", x)

    subjects = []
    for tag in soup.find(lambda tag: tag.get("name") == "p_subj"):
        if type(tag) == bs4.element.Tag:
            subjects.append((tag.get("value"), clean(tag.string)))

    terms = []
    for tag in soup.find(lambda tag: tag.get("name") == "p_term"):
        if type(tag) == bs4.element.Tag:
            terms.append((tag.get("value"), clean(tag.string)))

    for term in terms:
        scrape_term(term, subjects)

scrape_all()

