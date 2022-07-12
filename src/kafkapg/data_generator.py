import json
import requests
import random
import re
from urllib import request


def website_data(test_url):
    url = ""
    # If no url was send, using prepared ones
    if test_url == "":
        urls = ["https://www.python.org/", "https://kafka.apache.org/", "https://www.wikipedia.org/"]
        # Checking random website from the list
        url = random.choice(urls)
    else:
        url = test_url

    resp = request.urlopen(url)
    # Retrieve response_time and status_code
    response_time = round(requests.get(url).elapsed.total_seconds(), 4)
    status_code = resp.code

    # Check if the pattern is found
    data = resp.read()
    html = data.decode("UTF-8")
    pattern = re.search("\si.\sa", html)

    if pattern is not None:
        pattern = "Regexp pattern '\si.\sa' found: " + pattern.group()
    else:
        pattern = "Regexp pattern '\si.\sa' not found"

    value = {'website': url,
    'response_time': response_time,
    'status_code': status_code,
    'page_pattern': pattern}


    return json.dumps(value)

    #return {
       # {'website': url,
        #'response_time': response_time,
       # 'status_code': status_code,
        #'page_pattern': pattern}
    #}


if __name__ == '__main__':
    website_data()
