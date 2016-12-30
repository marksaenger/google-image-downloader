""" Simple program to request images using Google's Customsearch API """

import datetime
import math
import os.path
import urllib.error
import urllib.request
from urllib.request import urlretrieve

from googleapiclient.discovery import build

MAX_REQUESTS = 100 # max requests per day imposed by Google for those with free accounts
MAX_RESULTS_PER_REQUEST = 10

def gid(api_key, cx_id, num_search_results, search_term, img_size, img_type, safe_search, search_type):
    """
    Google Image Downloader
    Download images based on function parameters to local folder
    """

    # TODO use an object to reduce the number of local scope variables

    remaining_requests = num_search_results

    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.
    service = build("customsearch", "v1", developerKey=api_key)

    if remaining_requests % MAX_RESULTS_PER_REQUEST == 0:
        # math.ceil is used so that num_requests gets converted to an integer
        # floats don't play nice with for loop ranges apparently
        num_requests = math.ceil(remaining_requests / MAX_RESULTS_PER_REQUEST)
    else:
        num_requests = math.ceil(remaining_requests / MAX_RESULTS_PER_REQUEST)

    # Create a unique directory containing the current time and search term for each query
    time = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    directory = time + '_' + search_term
    if not os.path.exists(directory):
        os.makedirs(directory)

    start_num = 1
    cur_results = remaining_requests
    if cur_results > MAX_RESULTS_PER_REQUEST:
        cur_results = MAX_RESULTS_PER_REQUEST

    for i in range(0, num_requests):
        # see https://developers.google.com/custom-search/json-api/v1/reference/cse/list
        # for detailed documentation
        res = service.cse().list(
            q=search_term,
            cx=cx_id,
            imgSize=img_size,
            imgType=img_type,
            num=cur_results, #number of search results, max of 10
            safe=safe_search,
            searchType=search_type,
            start=start_num
            ).execute()

        if 'items' in res:
            for item in res['items']:
                size = item['image']['height'] * item['image']['width']
                print('{}:\n\t{}'.format(item['title'], item['link']))
                try:
                    # TODO add some logic to detect irregular urls
                    #  urls with stuff after the extension
                    #  urls without an extension
                    #  ...
                    urlretrieve(item['link'], directory + "//" + str(size) + '___' + \
                        os.path.basename(item['link']))
                except urllib.error.HTTPError:
                    print("Error downloading image\n")
        else:
            print("No results\n")
            break

        start_num += MAX_RESULTS_PER_REQUEST
        remaining_requests -= MAX_RESULTS_PER_REQUEST
        if remaining_requests < MAX_RESULTS_PER_REQUEST:
            cur_results = remaining_requests
