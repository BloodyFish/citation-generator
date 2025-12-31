from bs4 import BeautifulSoup

months = {
    1 : "Jan.",
    2 : "Feb.",
    3 : "Mar",
    4 : "Apr.",
    5 : "May",
    6 : "June",
    7 : "July",
    8 : "Aug.",
    9 : "Sept.",
    10 : "Oct.",
    11 : "Nov.",
    12 : "Dec."
}

def get_date(soup, data):
    if soup.find("time") is not None:
        # date_unformated gives Year-Month-DayTOtherNumbers
        date_unformated = str(soup.find("time")['datetime'])
    elif data:
        if type(data) is list:
            date_published = data[0].get("datePublished")
            date_modified = data[0].get("dateModified")
        else:
            date_published = data.get("datePublished")
            date_modified = data.get("dateModified")

        if date_modified: 
            date_unformated = date_modified
        elif date_published:
            date_unformated = date_published

    else:
        return "n.d. "


    # We need to get rid of the 'T'
    date_unformated = date_unformated.split('T')[0]
    date = date_unformated.split("-")

    # date is now a list formated as [Year, Month, Day]
    date[1] = months[int(date[1])]
    return date