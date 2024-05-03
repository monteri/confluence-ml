import requests
from atlassian import Confluence
from requests.auth import HTTPBasicAuth
import time


# Authentication
ATLASIAN_USERNAME = ''
ATLASIAN_TOKEN = ''
auth = HTTPBasicAuth(ATLASIAN_USERNAME, ATLASIAN_TOKEN)


def get_api_response(url, auth=None, params=None):
    response = requests.get(url, auth=auth, params=params)
    if response.status_code == 429:
        # Too many requests, wait and retry
        retry_after = int(response.headers.get('Retry-After', 60))  # Default to 60 seconds
        print(f"Rate limit exceeded. Waiting for {retry_after} seconds.")
        time.sleep(retry_after)
        return get_api_response(url, params)
    elif response.status_code != 200:
        # If the status code is not 200, print the status and response text for debugging
        print(f"Error: Received status code {response.status_code}")
        print("Response text:", response.text)
        return None
    return response


# List pages in a space
space_key = 'tech'
base_url = ''
# Base domain for your Confluence instance
base_domain = 'https://raccoongang.atlassian.net/wiki'
params = {'spaceKey': space_key, 'type': 'page'}
confluence = Confluence(
    url='',
    username=ATLASIAN_USERNAME,
    password=ATLASIAN_TOKEN,
    cloud=True,
    api_version="cloud",
)

print('START SCRIPTING')

while True:
    print('================================================')
    response = get_api_response(base_url, auth=auth, params=params)
    if response is not None:
        pages = response.json().get('results', [])
    pages = response.json().get('results', [])
    # Pagination handling
    next_page = response.json().get('_links', {}).get('next', None)
    print('next_page', next_page)
    i = 0
    for page in pages:
        i += 1
        print(f'>>>>>>>> {i}')
        page_id = page['id']
        print('page', page)

        try:
            data = confluence.export_page(page_id)
        except:
            print('ERROR', page_id, next_page)
            continue
        with open(f'page_{page_id}.pdf', 'wb') as file:
            file.write(data)

    if not next_page:
        break
    base_url = base_domain + next_page  # Concatenate base domain with the relative path
