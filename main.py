import sys
from CitationGenerator import CitationGenerator, generate_citation_MLA

if __name__ == "__main__":
    url = str(sys.argv[1])

    citation_generator = CitationGenerator(url)

    title = citation_generator.get_title()
    date = citation_generator.get_date()
    site_name = citation_generator.get_site_name()
    publisher = citation_generator.get_publisher()
    author = citation_generator.get_author()

    print("Title: ", title)
    print("Date: ", date)
    print("Site Name: ", site_name)
    print("Publisher: ", publisher)
    print("Author(s): ", author)
    print()

    '''
    MLA CITATIONS

    Last name, First name. "Title." Title of website, Publisher, Day Month Year, URL

    IF TWO AUTHORS:
    Last name, First name, and First name Last name.

    IF THREE OR MORE AUTHORS:
    Last name, First name, et al.
    '''

    print(generate_citation_MLA(author, title, site_name, publisher, date, url))
