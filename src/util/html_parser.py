from bs4 import BeautifulSoup


def get_text(html: str) -> str:
    soup = BeautifulSoup(html, features="html.parser")
    return soup.get_text()
