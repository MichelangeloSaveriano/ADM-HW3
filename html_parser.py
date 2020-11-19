from bs4 import BeautifulSoup
import re


def clean_str(string):
    return ' '.join(string.split())


def get_publication_date(publication_string):
    word_list = publication_string.split()
    index = 1
    for i in range(len(word_list)):
        if word_list[i].isdigit():
            index = i
            break
    return ' '.join(word_list[1:index + 1])


def parse(path):
    with open(path, encoding="utf8") as fp:
        info = dict()
        soup = BeautifulSoup(fp, 'html.parser')
        info['bookTitle'] = clean_str(soup.find('h1', id='bookTitle').text)
        info['bookSeries'] = clean_str(soup.find('h2', id='bookSeries').text)[1:-1]
        info['bookAuthors'] = [clean_str(author.text) for author in soup.find_all('div', 'authorName__container')]
        info['ratingValue'] = clean_str(soup.find('span', itemprop='ratingValue').text)
        info['ratingCount'] = soup.find('a', 'gr-hyperlink', href='#other_reviews').text.split()[0]
        info['reviewCount'] = soup.find_all('a', 'gr-hyperlink', href='#other_reviews')[1].text.split()[0]
        info['plot'] = soup.find('div', id='description').find_all('span')[1].text
        info['numberOfPages'] = soup.find('span', itemprop='numberOfPages').text.split()[0]
        info['published'] = get_publication_date(soup.find_all('div', 'row')[1].text)
        info['characters'] = re.sub('...(less|more)',
                                    '',
                                    soup.find('div',
                                              'infoBoxRowTitle',
                                              string=re.compile("Characters")).find_next_sibling(
                                        'div').text).strip().split(
            ', ')
        setting = soup.find('div', 'infoBoxRowTitle', string=re.compile("Setting")).find_next_sibling('div').find_all(
            'a')
        info['setting'] = [s.text for s in setting]
        info['url'] = soup.find('meta', property='og:url')['content']
        return info


info = parse('./data/book_1.html')
for key, value in info.items():
    print("'", key, "': <", value, '>', sep='')
