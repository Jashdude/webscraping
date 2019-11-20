from requests.exceptions import HTTPError
import requests
from bs4 import BeautifulSoup
import re

def simple_get(url, params=None):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        resp = requests.get(url, timeout=5, params=params)
        # If the response was successful, no Exception will be raised
        resp.raise_for_status()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        # sanity check
        # is this HTML?
        content_type = resp.headers['Content-Type'].lower()
        # True if the response seems to be HTML, False otherwise.
        # Followed by 'death'
        assert content_type.find('html') >= 0

    return resp

def who_actors(url):

    resp = simple_get(url)
    # get the decoded payload.  the text() method uses metadata to devine encoding.
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')

    # to be returned
    actor_list = []

    # After inpspection of the HTML, I found that img elements
    # that have a title attribute that begin with the text 'Slide'
    # will give me the actor names I after (mostly anyway)
    for img in soup.find_all('img', title=re.compile(r'^Slide\s+\d+:\s+[A-Z]')):

        # I want the name from the title attribute which looks like this:
        # Slide 10: Sixth Doctor: Colin Baker
        # Another good use for REs.
        # This RE starts the same as before; however, afer the first :
        # the [^:]+ says "gobble up all characters that are not a : until you run into a colon
        # that is followed by a space. After that, capture all remaining characters in a group named <actor>" 
        #
        title = img['title']

        m = re.search(r'^Slide\s+\d+:[^:]+[:]\s+(?P<actor>.*)$', title)
        # if no match, then I've screwed up something
        assert m is not None
        if m:
            actor_list.append(m.group('actor'))

    # Great, got my list of actors.  Scram...
    return actor_list

def who_stats(dr_who):
    # the names are separated by \s chars.  In wikipedia
    # urls those spaces become underscores (_)
    dr_who = dr_who.replace(' ', '_')

    #url = 'https://en.wikipedia.org/w/index.php?title=dr_who_nm&action=info'.replace('dr_who_nm', dr_who)
    url = 'https://en.wikipedia.org/w/index.php?title=' + dr_who

    # Notice that navigation to the info page is a query param
    resp = simple_get(url, params={'action': 'info'})
    # get the decoded payload.  the text() method uses metadata to devine encoding.
    html = resp.text

    # By inspection of HTTP results you will find that the
    # stat we seek is extremely easy to find:
    # <div class="mw-pvi-month">58,243</div>
    # the <div> tag has a class attr designed to display the "pvi" - page view in...months!

    soup = BeautifulSoup(html, 'html.parser')

    #  Only need a find (not find_all) since there is only a single tag
    # that has a class attr = mw-pvi-month

    div = soup.find('div', class_='mw-pvi-month')
    # sanity check
    assert div is not None
    # this text may have commas which need to be removed
    # prior to parsing as an int
    return int(div.text.replace(',',''))

def main():
    # PHASE 1:
    # Get the Dr.Who actors from EW_URL
    EW_URL = 'http://ew.com/tv/doctor-who-actors/'

    actor_list = who_actors(EW_URL)

    # PHASE 2:
    # Collect the stats from Wikipedia
    # for each who actor
    #
    actor_stats_dict = {}

    for a in actor_list:
        pvim_stat = who_stats(a)
        actor_stats_dict[a] = pvim_stat

    # PHASE 3:
    # Sort number of views in desc order
    sorted_actor_list = sorted(actor_stats_dict, key=actor_stats_dict.get, reverse=True)

    print("Drum roll please...\nThe top 5 Dr. Who actors are:")
    for a in sorted_actor_list[0:5]:
        cnt = actor_stats_dict[a]
        print(f'\t{a} : {cnt}')

if __name__ == "__main__":
    main()