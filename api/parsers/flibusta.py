from lxml import html
import requests

api_base = 'http://flibusta.is'
page_size = 20

def get_search_result(book_name, sort='rating'):
    payload = {'ab': 'ab1', 't': book_name, 'sort': sort}
    try:
        response = requests.get('{}/makebooklist'.format(api_base), params = payload)
    except requests.exceptions.ConnectionError:
        print('Connection error')

    if response.text != 'Не нашлось ни единой книги, удовлетворяющей вашим требованиям.':
        return response.text

def get_book_cover(document):
    images = ['{}{}'.format(api_base, image.strip()) for image in document.xpath('//div[@id="main"]/img/@src')]
    if len(images) > 0:
        return images[0]

def get_book_description(document):
    descriptions = document.xpath('//div[@id="main"]/p')
    if len(descriptions) > 0:
        return descriptions[0].text

def calculate_previous_page_num(size, num):
    return (num-1)*size

def get_book_data(link, title):
    try:
        response = requests.get(link)
    except requests.exceptions.ConnectionError:
        print('Connection error')

    document = html.fromstring(response.text)

    id = link.split('/')[-1]

    return {'id': id, 'title': title, 'description': get_book_description(document), 'source': 'flibusta', 'link': link, 'cover': get_book_cover(document)}

def get_books_data(search_result, page):
    document = html.fromstring(search_result)
    books_data = [['{}{}'.format(api_base, link.xpath('@href')[0]), link.text] for link in document.xpath('//div/a') if 'download' not in link.xpath('@href')[0]]
    previous_page_num = calculate_previous_page_num(page_size, page)

    books = [
        get_book_data(book_item_data[0], book_item_data[1])
        for book_item_data in books_data[previous_page_num:previous_page_num+page_size]
    ]

    return books

def get_books(query, page=1):
    search_result = get_search_result(query)
    if search_result != None:
        books = get_books_data(search_result, page)
        return books
    return []

if __name__ == '__main__':
    books = get_books('Python')