import urllib, json, io, os
from constants import SAD_EMOJI, ID_EMOJI, BOOKS_EMOJI, SCHOOL_EMOJI, LINK_EMOJI

HOST_URL = 'https://www.edjoin.org/'
API_URI = 'Home/LoadJobs?'

DEFAULT_KEYWORDS = ['history', 'social studies', 'social science']
DEFAULT_BLACKLIST = ['autism']

def search():
    search_results = get_search_results()

    _write_search_results(search_results)

    return format_search_results(search_results)

def get_search_results():
    search_results = []

    keywords = get_keywords()
    blacklist = get_blacklist()

    for keyword in keywords:
        search_vars = {
            'rows': 10,
            'page': 1,
            'sort': 'postingDate',
            'order': 'desc',
            'keywords': keyword,
            'searchType': 'all',
            'states': 24,
            'regions': 30,
            'jobTypes': '5,4,46,0',
            'days': 0,
            'catID': 0,
            'onlineApps': 'false',
            'recruitmentCenterID': 0,
            'stateID': 0,
            'regionID': 0,
            'districtID': 0,
            'countryID': 0
        }

        url = HOST_URL + API_URI + urllib.urlencode(search_vars)
        jobs_json = urllib.urlopen(url).read()

        for position in json.loads(jobs_json)['data']:
            if (position not in search_results) and not any((blacklist_word in position['positionTitle'].lower() or blacklist_word in position['districtName'].lower()) for blacklist_word in blacklist):
                search_results.append(position)

    return search_results

def _write_search_results(search_results):
    with io.open('edjoin_last_search.json', 'w', encoding = 'utf-8') as file:
        if len(search_results) > 0:
            file.write(json.dumps(search_results, ensure_ascii = False))
        else:
            file.write(unicode(''))

def format_search_results(search_results):
    search = keywords_string() + '\n\n'

    if len(search_results) > 0:
        for position in search_results:
            search += BOOKS_EMOJI
            search += ' '
            search += position['positionTitle']
            search += '\n'
            search += SCHOOL_EMOJI
            search += ' '
            search += position['districtName']
            search += '\n'
            search += LINK_EMOJI
            search += ' https://www.edjoin.org/Home/JobPosting/'
            search += str(position['postingID'])
            search += '\n\n'

        search = search[:-2]
    else:
        search += 'No jobs found. '
        search += SAD_EMOJI

    return search

def _write_keywords(keywords):
    with io.open('edjoin_keywords.txt', 'w', encoding = 'utf-8') as file:
        for word in keywords:
            file.write(unicode(word + ','))

def get_keywords():
    keywords = []

    with io.open('edjoin_keywords.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            words = line.split(',')
            keywords.extend(words)

    if len(keywords) > 0:
        last_word = keywords[len(keywords) - 1]
        if "\n" in last_word:
            keywords[len(keywords) - 1] = last_word[:-1]

    return [keyword.encode('utf-8') for keyword in filter(None, keywords)]

def add_keyword(keyword):
    keywords = get_keywords()

    if keyword not in keywords:
        keywords.append(keyword)
        _write_keywords(keywords)

    return get_keywords()

def remove_keyword(keyword):
    keywords = get_keywords()

    if keyword in keywords:
        keywords.remove(keyword)
        _write_keywords(keywords)

    return get_keywords()

def default_keywords():
    _write_keywords(DEFAULT_KEYWORDS)

    return get_keywords()

def keywords_string():
    keywords = get_keywords()

    if len(keywords) > 0:
        return 'Keywords:\n' + str(keywords)
    else:
        return 'Keywords list is empty. ' + SAD_EMOJI

def _write_blacklist(blacklist):
    with io.open('edjoin_blacklist.txt', 'w', encoding = 'utf-8') as file:
        for word in blacklist:
            file.write(unicode(word + ','))

def get_blacklist():
    blacklist = []

    with io.open('edjoin_blacklist.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            words = line.split(',')
            blacklist.extend(words)

    if len(blacklist) > 0:
        last_word = blacklist[len(blacklist) - 1]
        if "\n" in last_word:
            blacklist[len(blacklist) - 1] = last_word[:-1]

    return [word.encode('utf-8') for word in filter(None, blacklist)]

def add_to_blacklist(word):
    blacklist = get_blacklist()

    if word not in blacklist:
        blacklist.append(word)
        _write_blacklist(blacklist)

    return get_blacklist()

def remove_from_blacklist(word):
    blacklist = get_blacklist()

    if word in blacklist:
        blacklist.remove(word)
        _write_blacklist(blacklist)

    return get_blacklist()

def default_blacklist():
    _write_blacklist(DEFAULT_BLACKLIST)

    return get_blacklist()

def blacklist_string():
    blacklist = get_blacklist()

    if len(blacklist) > 0:
        return 'Blacklist:\n' + str(blacklist)
    else:
        return 'Blacklist is empty.'

def _get_last_search_json():
    json_size = os.path.getsize('edjoin_last_search.json')

    # Empty .json file is only 2 bytes
    if (json_size > 2):
        with io.open('edjoin_last_search.json', 'r', encoding = 'utf-8') as file:
            last_search = json.load(file)
    else:
        last_search = None

    return last_search

def get_last_search():
    last_search = _get_last_search_json()

    if last_search is not None:
        return format_search_results(last_search)
    else:
        return 'No search found. Sorry!'
