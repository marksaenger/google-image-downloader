""" Sample usage of the Google Image Downloader """

import sys
import gid
import config

NUM_SEARCH_RESULTS = 10
SEARCH_TERM = "jurassic park"
IMAGE_SIZE = "huge" # icon, small, medium, large, xlarge, xxlarge, huge
IMAGE_TYPE = "photo" # clipart, face, lineart, news, photo
SAFE_SEARCH = "medium" # off, medium, high for safe search filtering
SEARCH_TYPE = "image" # must be 'image' otherwise results will be limited to webpages

def main():
    """ Main file """

    api_key = config.get_config_value('DEFAULT', 'APIKey')
    if api_key == 'False':
        sys.exit()

    cx_id = config.get_config_value('DEFAULT', 'CX')
    if cx_id == 'False':
        sys.exit()

    gid.gid(api_key, cx_id, \
        NUM_SEARCH_RESULTS, SEARCH_TERM, IMAGE_SIZE, IMAGE_TYPE, SAFE_SEARCH, SEARCH_TYPE)

if __name__ == '__main__':
    main()
