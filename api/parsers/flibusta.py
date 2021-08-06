from lxml import html
import requests

api_base = 'http://flibusta.is'

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

    page = html.fromstring(response.text)
    images = ['http:{}'.format(image.strip()) for image in page.xpath('//div[@id="main"]/img/@src')]
    if len(images) > 0:
        return images[0]

def get_books_data(search_result, num):
    document = html.fromstring(search_result)
    book_links = ['{}{}'.format(api_base, link) for link in document.xpath('//div/a/@href') if 'download' not in link]
    books = [[book_link, get_book_cover(book_link)] for book_link in book_links[:num]]
    return books

def get_books(book_name, sort):
    search_result = get_search_result(book_name, sort)
    if search_result != None:
        books = get_books_data(search_result, 20)
        return books

if __name__ == '__main__':
    books = get_books('Python', 'litres')