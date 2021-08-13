import requests

api_base = 'https://stepik.org'

def render_course_link(id):
    return 'https://stepik.org/course/{}/promo'.format(id)

def get_course_description(id):
    params = {
        'ids[]': id
    }

    response = requests.get(
        '{}/api/courses'.format(api_base),
        params = params
    )

    data = response.json()
    return data['courses'][0]['summary']

def get_data(item):
    description = get_course_description(item['course'])
    return {'title': item['course_title'], 'description': description, 'source': 'stepik', 'link': render_course_link(item['course']), 'cover': item['course_cover']} 

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
    courses = [
        get_data(item)
        for item in data['search-results']
    ]
    return courses

if __name__ == '__main__':
    print(get_courses('python'))