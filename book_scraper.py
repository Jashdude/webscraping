from requests.exceptions import HTTPError
import requests
from bs4 import BeautifulSoup
import re
import csv

def simple_get(url, params=None):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        resp = requests.get(url, timeout=5, params=params)
        # If the response was successful, no Exception will be raised
        resp.raise_for_status()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        # sanity check
        # is this HTML?
        content_type = resp.headers['Content-Type'].lower()
        # True if the response seems to be HTML, False otherwise.
        # Followed by 'death'
        assert content_type.find('html') >= 0

    return resp

# R2. For each book category URL, follow the URL to the book category page.
# You may restrict your data scraping to the first page of books returned for the category URL.
books_category_link = {}
def book_scraper(url):
    resp = simple_get(url)
    html = resp.text
    soup = BeautifulSoup(html, 'lxml')
    #soup.encode("utf-8")
    for link in soup.find_all('a', href=re.compile(r'^catalogue/category/books/.*')):
        books = link.text
        books_category_link.update({books.strip():link['href']})
    return books_category_link

# Challenge Question - Function to get the current and next page
# if the category has multiple pages until category is exhausted.
next_page=[]
def get_next(category, root_url, link):
    book_url = root_url + '/' + link
    print(book_url)
    book_resp = simple_get(book_url)
    html = book_resp.text
    soup = BeautifulSoup(html, 'lxml')
    current = soup.find()
    nxt_ = soup.find('li', class_="next")
    pager = soup.find('li', class_="current")
    new_link = link.replace('index.html', '')
    if nxt_ is not None:
        # Add the current page the control is in, to the list.
        next_page.append({category: new_link + nxt_.a["href"]})
        # Get the next page href
        href = nxt_.a["href"]
        if pager is not None:
            # print(int(pager.text.strip()[-1]))
            # Loop through the pages using the number mentioned on the pager.
            for i in range(2, int(pager.text.strip()[-1])+1):
                book_url = root_url + '/' + new_link + href
                print(book_url)
                book_resp = simple_get(book_url)
                html = book_resp.text
                soup = BeautifulSoup(html, 'lxml')
                next_inner = soup.find('li', class_="next")
                if next_inner is not None:
                    #print(new_link + next_inner.a["href"])
                    # Add the page href to the list and reset the href to next page.
                    next_page.append({category: new_link + next_inner.a["href"]})
                    href = next_inner.a["href"]

book_details = []
def get_books(category, root_url, link):
    # R4. Convert the ordinal star rating data to a numeric scale.
    # For example, the string ‘star-rating One’ would be converted to the number 1, ‘star-rating Two’
    # would be converted to 2, and so on.
    rating_map = {"ONE":1, "TWO":2, "THREE":3, "FOUR":4, "FIVE":5}
    book_url = root_url + '/' + link
    book_resp = simple_get(book_url)
    html = book_resp.text
    soup = BeautifulSoup(html, 'lxml')
    # R1. Examine the HTML returned from the Books to Scrape top-level URL.
    # Your objective is to identify and extract book category and the book category URL information from this page.
    for books in soup.findAll('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3"):
        #R3. For each of the books on a category page, capture the book title, star rating and price.
        bookname = books.find('img', class_="thumbnail")['alt'].replace("\x80\x99", "'").replace("â", "")
        rating = books.find('p', class_=re.compile(r"star-rating.*"))['class'][1]
        price = books.find('p', class_="price_color").text.replace("Â", '').strip()
        book_details.append([category, bookname, rating_map[rating.upper()], price, book_url])

root_url = "http://books.toscrape.com"
def main():
    category_url_dict = book_scraper(root_url)
    for category, link in category_url_dict.items():
        get_next(category, root_url, link)

    for pages in next_page:
        for category, href in pages.items():
            get_books(category, root_url, href)

    # R2. For each book category URL, follow the URL to the book category page.
    # You may restrict your data scraping to the first page of books returned for the category URL.
    for category, href in category_url_dict.items():
        get_books(category, root_url, href)

    sorted_book_details = sorted(book_details)
    print(*sorted_book_details, sep="\n")

    # R5. For each book, output one line containing the book category, title, numeric star rating and price to a CSV file.
    with open("book_data.csv", mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"',quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Category','Book_name', 'Ratings', 'Price', 'Book_Url'])
        for row in sorted_book_details:
            writer.writerow(row)

if __name__ == "__main__":
    main()