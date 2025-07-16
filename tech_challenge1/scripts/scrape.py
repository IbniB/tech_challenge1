import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin
import os

BASE_URL = "https://books.toscrape.com/"


def get_soup(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def get_category_urls():
    soup = get_soup(BASE_URL)
    category_tags = soup.select(".side_categories ul li ul li a")
    return {tag.text.strip(): urljoin(BASE_URL, tag['href']) for tag in category_tags}


def parse_book_info(book_tag, category):
    title = book_tag.h3.a['title']
    price = book_tag.select_one(".price_color").text.strip()
    availability = book_tag.select_one(".availability").text.strip()
    rating_class = book_tag.select_one("p.star-rating")["class"]
    rating = rating_class[1] if len(rating_class) > 1 else "None"
    image_rel_url = book_tag.select_one("img")["src"]
    image_url = urljoin(BASE_URL, image_rel_url.replace("../../", ""))

    return {
        "title": title,
        "price": price,
        "availability": availability,
        "rating": rating,
        "category": category,
        "image_url": image_url
    }


def scrape_category(category_name, category_url):
    print(f"Scraping categoria: {category_name}")
    books = []
    page_url = category_url
    while True:
        soup = get_soup(page_url)
        book_tags = soup.select("article.product_pod")
        for book_tag in book_tags:
            books.append(parse_book_info(book_tag, category_name))

        next_button = soup.select_one("li.next > a")
        if next_button:
            page_url = urljoin(page_url, next_button["href"])
            time.sleep(1)  # Respeitar o servidor
        else:
            break
    return books


def scrape_all_books():
    all_books = []
    categories = get_category_urls()
    for name, url in categories.items():
        books = scrape_category(name, url)
        all_books.extend(books)
    return all_books


if __name__ == "__main__":
    print("Iniciando scraping dos livros")
    books_data = scrape_all_books()
    df = pd.DataFrame(books_data)
    df.insert(0, "id", range(len(df)))  # adiciona coluna id incremental
    output_dir = os.path.join(os.path.dirname(__file__), "..", "api", "data")
    os.makedirs(output_dir, exist_ok=True)

    csv_path = os.path.join(output_dir, "livros.csv")
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"✅ Scraping finalizado. {len(df)} livros salvos em data/livros.csv.")