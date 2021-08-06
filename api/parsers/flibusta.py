import requests

def get_search_result(book_name, sort = 'rating'):
    payload = {'ab': 'ab1', 't': book_name, 'sort': sort}
    try:
        response = requests.get('http://flibusta.is/makebooklist', params = payload)
    except requests.exceptions.ConnectionError:
        print('Connection error')

    if response.text != 'Не нашлось ни единой книги, удовлетворяющей вашим требованиям.':
        return response.text


if __name__ == '__main__':
    print(get_search_result('Python'))