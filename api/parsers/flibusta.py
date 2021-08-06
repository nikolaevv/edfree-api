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

    print(response.text)
    if response.text != 'Не нашлось ни единой книги, удовлетворяющей вашим требованиям.':
        return response.text

def get_book_cover(link):
    pass

def get_books_ids(search_result):
    document = html.fromstring(search_result)
    book_links = ['{}{}'.format(api_base, link) for link in document.xpath('//div/a/@href') if 'download' not in link]
    books = [(book_link, get_book_cover(book_link)) for book_link in book_links]
    print(books)

def get_links(book_name, sort):
    search_result = get_search_result(book_name, sort)
    if search_result != None:
        pass
        book = get_books_ids(search_result)
        #link = f'http://flibusta.is{book}/{file_format}'
        #return link

if __name__ == '__main__':
    get_links('Python', 'litres')