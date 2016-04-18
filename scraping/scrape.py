#!/usr/bin/python3

import re
import json
import urllib.request
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

import lxml
import bs4
from bs4 import BeautifulSoup as BS

from database import *

URL_INDEX = "http://banweb7.nmt.edu/pls/PROD/hwzkcrof.p_uncgslctcrsoff"
URL_SEARCH = "http://banweb7.nmt.edu/pls/PROD/hwzkcrof.P_UncgSrchCrsOff"

def write_php(terms):
    with open("banweb_terms.php", "w") as out:
        out.write("<?php\n$terms = array(\n")
        for term in terms:
            out.write("\tarray('" + term[0] + "','" + term[1] + "'),\n")
        out.write(");\n?>")

def write_courses(term, subject, courses):
    print("\t" + subject[1] + " (" + str(len(courses)) + ")")

    year = int(term[1].split()[1])
    semester = term[1].split()[0].lower()[0:3]
    date_range = {
        "spr": (datetime(year, 1, 1), datetime(year, 5, 31, 23, 59, 59)),
        "sum": (datetime(year, 6, 1), datetime(year, 7, 31, 23, 59, 59)),
        "fal": (datetime(year, 8, 1), datetime(year, 12, 31, 23, 59, 59)),
    }

    def parse_int(x, y):
        if x == "":
            return y
        return int(x)

    last_crn = (0, 0)

    group = Classes.select().where(Classes.year == year,
                                   Classes.semester == semester)

    for fields in courses:
        crn = parse_int(fields[0], 0)

        new_crn = (0, 0)
        if crn != 0:
            last_crn = (crn, crn * 10)
        else:
            last_crn = (last_crn[0], last_crn[1] + 1)
            new_crn = last_crn

        entry = {}
        entry["crn"] = crn
        entry["year"] = year
        entry["semester"] = semester
        entry["subclass_identifier"] = new_crn[1]
        entry["entry"] = fields[1]
        entry["campus"] = fields[2]
        entry["days"] = fields[3]
        entry["time"] = fields[4]
        entry["location"] = fields[5]
        entry["hours"] = parse_int(fields[6], 0)
        entry["title"] = fields[7]
        entry["instructor"] = fields[8]
        entry["seats"] = parse_int(fields[9], 0)
        entry["limit"] = parse_int(fields[10], 0)
        entry["enroll"] = parse_int(fields[11], 0)

        dtl = []
        for day in entry["days"].split():
            dtl.append([day, entry["time"], entry["location"]])
        if not dtl:
            dtl.append(["", "", ""])
        entry["days_times_locations"] = json.dumps(dtl).strip()

        entry["parent_class"], entry["subclass_identifier"] = new_crn

        entry["subject"] = subject[0]
        entry["start_date"], entry["end_date"] = date_range[entry["semester"]]
        entry["last_mod_time"] = datetime.now()

        current = group.where(Classes.crn == crn,
                              Classes.subclass_identifier == new_crn[1])

        if current.exists():
            Classes.update(**entry).where(Classes.crn == crn,
                                           Classes.subclass_identifier == new_crn[1],
                                           Classes.year == year,
                                           Classes.semester == semester).execute()
        else:
            Classes.insert(**entry).execute()

def match_course(tag):
    if tag.name == "tr" and len(tag.contents) == 25:
        if tag.contents[1].name == "td":
            return True
    return False

def scrape_subject(term, subject):
    url = URL_SEARCH + \
            '?p_term=' + term[0] + \
            '&p_subj=' + re.sub(r'\s+', "%20", subject[0])
    page = BS(urllib.request.urlopen(url), "lxml")

    courses = []
    for row in page.find_all(match_course):
        entry = []
        row = row.contents[1]
        for i in range(0, 12):
            if row.string != None:
                entry.append(row.string.strip())
            else:
                entry.append("")
            row = row.next_sibling.next_sibling
        if set(entry) != {""}:
            courses.append(entry)

    if len(courses) != 0:
        write_courses(term, subject, courses)

def scrape_term(term, subjects):
    print("\n" + term[1])

    global URL_SEARCH

    year = int(term[1].split()[1])
    semester = term[1].split()[0].lower()[0:3]

    group = Subjects.select().where(Subjects.year == year,
                                    Subjects.semester == semester)

    with ThreadPoolExecutor(max_workers=5) as executor:
        for subject in subjects:
           if not group.where(Subjects.abbr == subject[0]).exists():
                entry = {"semester": semester,
                         "year": year,
                         "abbr": subject[0],
                         "title": subject[1]}
                Subjects.insert(**entry).execute()

           executor.submit(scrape_subject, term, subject)

def scrape_all():
    global URL_INDEX

    soup = BS(urllib.request.urlopen(URL_INDEX), "lxml")

    subjects = []
    for tag in soup.find(lambda tag: tag.get("name") == "p_subj"):
        if type(tag) == bs4.element.Tag:
            subjects.append((tag.get("value"), tag.string.strip()))

    subjects.append(("CUSTOM", "Custom"))

    terms = []
    for tag in soup.find(lambda tag: tag.get("name") == "p_term"):
        if type(tag) == bs4.element.Tag:
            terms.append((tag.get("value"), tag.string.strip()))

    write_php(terms)

    for term in terms:
        scrape_term(term, subjects)

scrape_all()

