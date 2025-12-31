from bs4 import BeautifulSoup
import requests
import json

import Dates

# A lot of times, there's a '|' in various parts of parsed content
def remove_unwanted_chars(full_string: str, unwanted: str):
    return full_string.split(unwanted)[0].strip()

def generate_citation_MLA(author, title, site_name, publisher, date, url):
    if author is not None and len(author) > 0:
        if len(author) == 2:
            author_citation = f"{author[0].split()[1]}, {author[0].split()[0]}, and {author[1]}. "
        else:
            author_citation = f"{author[0].split()[1]}, {author[0].split()[0]}"
            
            if len(author) == 1:
                author_citation += ". "
            if len(author) >= 3:
                author_citation += ", et al. "

    else:
        author_citation = ""

    citation = author_citation

    if title is not None:
        citation += f"\"{title}.\" "

    if site_name is not None:
        citation += f"{site_name}, "

    if publisher is not None and site_name != publisher:
        citation += f"{publisher}, "

    if date is not None and len(date) > 0:
        citation += f"{date[2]} {date[1]} {date[0]}, "
    else:
        citation += "n.d. "

    citation += f"{url}."

    return citation


class CitationGenerator:
    def __init__(self, url: str):
        self.soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        self.data = None # Set data to None to start in order to avoid bugs

        m_json = self.soup.select_one('[type="application/ld+json"]')
        if m_json:
            contents = m_json.contents
            #print(m_json.contents[0])
            if contents:
                self.data = json.loads(contents[0])
                #print(json.dumps(data, indent=4))
                    

    def get_content(self, prop: str):
        if self.soup.find('meta', property= prop) is None:
            return

        content = self.soup.find('meta', property= prop)['content']
        if '|' in content:
            content = remove_unwanted_chars(content, '|')

        return content.title()


    def get_title(self):
        return self.get_content('og:title')


    def get_site_name(self):
        return self.get_content('og:site_name')
    

    def get_publisher(self):
        if self.data is None:
            return

        if type(self.data) is list:
            content = self.data[0].get("publisher")
        else:
            content = self.data.get("publisher")

        if content:
            return content["name"]


    def get_date(self):            
        return Dates.get_date(self.soup, self.data)


    def get_author(self):
        if self.data is None:
            return

        if type(self.data) is list:
            content = self.data[0].get("author")
            if content:
                return [i["name"] for i in self.data[0]["author"]]

        content = self.data.get("author")
        if content:
            return [i["name"] for i in self.data["author"]]
