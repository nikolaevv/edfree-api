from lxml import html
import requests

api_base = 'http://flibusta.is'
page_size = 20

rating = {
    'файл не оценен': 0,
    'файл на 1': 1,
    'файл на 2': 2,
    'файл на 3': 3,
    'файл на 4': 4,
    'файл на 5': 5
}

def get_search_result(book_name, sort='rating'):
    payload = {'ab': 'ab1', 't': book_name, 'sort': sort}
    try:
        response = requests.get('{}/makebooklist'.format(api_base), params = payload)
    except requests.exceptions.ConnectionError:
        print('Connection error')

    if response.text != 'Не нашлось ни единой книги, удовлетворяющей вашим требованиям.':
        return response.text

def get_book_cover(link):
    try:
        response = requests.get(link)
    except requests.exceptions.ConnectionError:
        print('Connection error')

    document = html.fromstring(response.text)
    images = ['{}{}'.format(api_base, image.strip()) for image in document.xpath('//div[@id="main"]/img/@src')]
    if len(images) > 0:
        return images[0]

def calculate_previous_page_num(size, num):
    return (num-1)*size

def get_books_data(search_result, page):
    document = html.fromstring(search_result)
    books_data = [['{}{}'.format(api_base, link.xpath('@href')[0]), link.text] for link in document.xpath('//div/a') if 'download' not in link.xpath('@href')[0]]
    previous_page_num = calculate_previous_page_num(page_size, page)

    books = [{'title': book_item_data[1], 'source': 'flibusta', 'link': book_item_data[0], 'cover': get_book_cover(book_item_data[0])} 
        for book_item_data in books_data[previous_page_num:previous_page_num+page_size]
    ]

    return books

def get_books(query, page=1):
    search_result = get_search_result(query)
    if search_result != None:
        books = get_books_data(search_result, 1)
        return books

if __name__ == '__main__':
    books = get_books('Python')