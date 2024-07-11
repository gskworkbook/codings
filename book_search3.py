import requests
from bs4 import BeautifulSoup

def search_flipkart_book(book_name):
    
    search_query = book_name.replace(' ', '+')
    url = f'http://www.flipkart.com/search?q={search_query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&sort=popularity&page=1'
    
    # Send HTTP request to Flipkart search results page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extracting the titles and prices of the books
    books = []
    results = soup.find_all('div', class_='slAVV4')
    for result in results:

        title_tag = result.find('a', class_='wjcEIp')
        if(title_tag is None):
            title = "No Title"
        else:
            title = title_tag.get_text()

        price_tag = result.find('div', class_='Nx9bqj')
        if(price_tag is None):
            price = 0.0
        else:
            price = float(price_tag.get_text().replace(',', '').replace('\u20b9', '')) #replacing rupee symbol (\u20b9)

        rating_tag = result.find('div', class_='XQDdHH')
        if(rating_tag is None):
            rating = 1.0
        else:
            rating = float(rating_tag.get_text())

        books.append({'title': title, 'price': price, "rating": rating})
    
    return books

if __name__ == '__main__':
    book_name = input("Enter the name of the book to search: ")
    results = search_flipkart_book(book_name)
    
    if results:
        print(f"Search results for '{book_name}' on Flipkart:")

        sorted_books = sorted(results, key=lambda x: (-x['rating'], x['price']))

        print("{:<3} {:<70} {:<10} {:<10}".format("   ", "Title", "Rating", "Price"))

        for idx, book in enumerate(sorted_books, start=1):
            print("{:<3}. {:<70} {:<10} \u20b9{:<10}".format(idx, book['title'], book['rating'], book['price']))
    else:
        print(f"No results found for '{book_name}' on Flipkart.")
