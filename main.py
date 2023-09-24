import requests
import sqlite3
from bs4 import BeautifulSoup

seed = "https://www.olx.ua/uk/transport/gruzovye-avtomobili/"

DATABASE = "olx.sqlite"


def get_links():
    r = requests.get(seed)
    soup = BeautifulSoup(r.content, "html.parser")
    links = []
    news_elements = soup.find_all("a", class_="css-rc5s2u")
    for element in news_elements:
        link = element["href"]
        links.append(link)
    return links


def get_page_content(link):
    full_url = "https://www.olx.ua" + link
    page = requests.get(full_url)
    soup = BeautifulSoup(page.content, "html.parser")
    name = soup.find("h1", class_="css-1dhh6hr er34gjf0").text
    cost = soup.find("h3", class_="css-1twl9tf er34gjf0").text
    image_url = soup.find("img", class_="css-1bmvjcs")["src"]
    description = soup.find("div", class_="css-bgzo2k er34gjf0").text
    number = soup.find("span", class_="css-12hdxwj er34gjf0").text
    timestamp = soup.find("span", class_="css-19yf5ek").text
    user_url = soup.find("a", class_="css-eaigk1")["href"]

    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO products(url_page, number, name, cost, image_url, description, timestamp, user_url) VALUES (?,?,?,?,?,?,?,?)",
            (
                link,
                number,
                name,
                cost,
                image_url,
                description,
                timestamp,
                user_url,
            ),
        )
        db.commit()
        print(f"Запись успешно добавлена в базу данных: {link}")
    except sqlite3.IntegrityError:
        # Если запись с таким URL уже существует, пропустите ее
        print(f"Запись с URL {link} уже существует в базе данных")
    db.close()


def main():
    links = get_links()
    for link in links:
        get_page_content(link)


if __name__ == "__main__":
    main()
