import requests

api_base = 'https://stepik.org'

def render_course_link(id):
    return 'https://stepik.org/course/{}/promo'.format(id)

def get_course_descriptions(ids):
    params = {
        'ids[]': ids
    }

    response = requests.get(
        '{}/api/courses'.format(api_base),
        params = params
    )

    data = response.json()

    return [course['summary'] for course in data['courses']]

def get_data(item, description):
    return {'id': item['course'], 'title': item['course_title'], 'description': description, 'source': 'stepik', 'link': render_course_link(item['course']), 'cover': item['course_cover']} 

def get_courses(query, page=1):
    params = {
        'is_popular': 'true',
        'is_public': 'true',
        'order': 'likes_rate__none,comments_count__log2p,rating__none,quality__none',
        'page': page,
        'query': query,
        'type': 'course',
        'is_paid': False
    }

    try:
        response = requests.get(
            '{}/api/search-results'.format(api_base), 
            params = params
        )
    except requests.exceptions.ConnectionError:
        return []

    data = response.json()

    course_ids = [str(search_result['course']) for search_result in data['search-results']]
    descriptions = get_course_descriptions(course_ids)

    courses = [
        get_data(item, descriptions[idx])
        for idx, item in enumerate(data['search-results'])
    ]
    return courses

if __name__ == '__main__':
    print(get_courses('python'))