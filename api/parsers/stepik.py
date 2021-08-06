import requests

api_base = 'https://stepik.org'

def get_courses(query, page=1):
    params = {
        'is_popular': 'true',
        'is_public': 'true',
        'order': 'likes_rate__none,comments_count__log2p,rating__none,quality__none',
        'page': page,
        'query': query,
        'type': 'course'
    }

    try:
        response = requests.get(
            '{}/api/search-results'.format(api_base), 
            params = params
        )
    except requests.exceptions.ConnectionError:
        return []

    data = response.json()
    courses = [{'title': item['course_title'], 'cover': item['course_cover']} for item in data['search-results']]
    return courses

if __name__ == '__main__':
    print(get_courses('python'))