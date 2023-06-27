from fastapi import FastAPI, Request
from typing import List, Tuple
import requests
import bs4
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index(request: Request):
    headings_with_links = fetch_headings_with_links()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "headings": headings_with_links})


def fetch_headings_with_links() -> List[Tuple[str, str]]:
    headings_with_links = []

    # bbc
    bbc = "https://www.bbc.com/news"
    response = requests.get(bbc)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    headings_bbc = soup.select(".gs-c-promo-heading")

    for heading in headings_bbc:
        text_heading = heading.text.strip()  # strip to remove all spaces
        try:
            link = heading.attrs["href"]
            if not link.startswith("https"):
                link = "https://www.bbc.com/" + link
            headings_with_links.append((text_heading, link))
        except KeyError:
            pass

    # newyork times
    new_york_times = "https://www.nytimes.com/international/"
    response = requests.get(new_york_times)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    headings_newyork = soup.select(".indicate-hover")
    links = soup.select(".css-9mylee")

    for heading, link_element in zip(headings_newyork, links):
        text_heading = heading.text
        link = link_element["href"]
        headings_with_links.append((text_heading, link))

    # dailymail
    response = requests.get("https://www.dailymail.co.uk/home/index.html")
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    headings_dailymail = soup.select(".linkro-darkred")

    for heading in headings_dailymail:
        text_heading = heading.text.strip()
        urls = heading.a["href"]
        if not urls.startswith("https"):
            urls = "https://www.dailymail.co.uk/" + urls
        headings_with_links.append((text_heading, urls))

    return headings_with_links


@app.get("/showallheadings")
def show_all_headings(request: Request):
    headings_with_links = fetch_headings_with_links()
    number_of_news = len(headings_with_links)
    return templates.TemplateResponse("show_all_headings.html",
                                      {
                                         "request": request,
                                          "headings": headings_with_links,
                                          "number_of_news": number_of_news
                                      })


@app.get("/search")
def search_news(request: Request, query: str=""):
    filtered_headings = filter_headings(query)
    number_of_filtered_headings = len(filtered_headings)
    return templates.TemplateResponse("search_headings.html", {
        "request": request,
        "headings": filtered_headings,
        "query": query,
        "number_of_filtered_headings": number_of_filtered_headings})


def filter_headings(query: str) -> List[Tuple[str, str]]:
    headings_with_links = fetch_headings_with_links()
    filtered_headings = []
    for heading, link in headings_with_links:
        if query.lower() in heading.lower():
            filtered_headings.append((heading, link))

    return filtered_headings
