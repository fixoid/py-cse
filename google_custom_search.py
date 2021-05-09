import urllib.request
import json
import config_cse
GCS_KEY, GCS_CX = config_cse.varconf()

def create_url(gcs_req, start=1):
    gcs_req = gcs_req.replace(' ','%20')
    return 'https://www.googleapis.com/customsearch/v1?key='+GCS_KEY+'&cx='+GCS_CX+'&num=10&start='+str(start)+'&q='+gcs_req

def get_url(url): 
    s = 'error'
    try:
        f = urllib.request.urlopen(url)
        s = f.read()
    except urllib.error.HTTPError:
        s = 'connect error'
    except urllib.error.URLError:
        s = 'url error'
    return s

def get_json(gcs_req, mode='url', start=1, filename='gcsRes.json'):
    """gets JSON formatted string from url or file  
    args:
        gcsReq - search request
        mode - 'url' - open url, 'save' - open url + save to file, 'file - open file'
    return:
        JSON formatted string
    """
    if mode =='url' or mode == 'save':
        req_url = create_url(gcs_req, start)
        page = get_url(req_url)
        if page == 'connect error' or page == 'url error':
            page = ('{ "kind" : "'+page+'" }').encode('utf-8')
        if mode == 'save':
            with open(filename, 'wb') as f:
                f.write(page)
        return page
    elif mode == 'file':
        with open(filename, 'rb') as f:
            page =  json.loads(f.read())        
    return page

def is_next_page(dict):
    if dict['queries'].get('nextPage') == None: return False
    else: return True

def total_results(dict):
    return int(dict['searchInformation']['totalResults'])

def next_page_start(dict):
    return dict['queries']['nextPage'][0]['startIndex']

def search_request(dict):
    return dict['queries']['request'][0]['searchTerms']

def page_links(dict):
    links = []
    for result in dict['items']:
        links.append(result['link'])
    return links

def all_links(gcs_req, pages_max=3, show_info=False, mode='url'):
    gcsDict = {}
    links = []
    resStart = 1
    first_page = True
    if (pages_max > 10): pages_max = 10     # limit of Google Custom Search API
    while first_page == True or is_next_page(gcsDict) == True and next_page_start(gcsDict) < pages_max*10:
        if first_page == True: first_page = False
        gcsDict = json.loads(get_json(gcs_req, mode, resStart))
        if (gcsDict['kind'] != 'connect error'):
            if total_results(gcsDict) > 0:
                links += page_links(gcsDict)
                if is_next_page(gcsDict) == True:
                    resStart = next_page_start(gcsDict)
    if show_info == True: print('Request: '+search_request(gcsDict)+'    Results: '+str(len(links)))
    return links