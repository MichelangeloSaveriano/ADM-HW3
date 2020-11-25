from bs4 import BeautifulSoup
import re
import os
from langdetect import detect


def from_list_to_str(lis):
    return ' ; '.join(lis)


def clean_str(string):
    string = string.strip().replace('\n', ' ').replace('\t', ' ')
    if not string:
        return ''
    if string[-1] == ',':
        string = string[:-1]
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
    try:
        with open(path, encoding="utf8") as fp:
            info = dict()
            soup = BeautifulSoup(fp, 'html.parser')
            info['bookTitle'] = clean_str(soup.find('h1', id='bookTitle').text)
            info['bookSeries'] = clean_str(soup.find('h2', id='bookSeries').text)[1:-1]
            info['bookAuthors'] = [clean_str(author.text) for author in soup.find_all('div', 'authorName__container')]
            info['ratingValue'] = clean_str(soup.find('span', itemprop='ratingValue').text)
            info['ratingCount'] = soup.find('a', 'gr-hyperlink', href='#other_reviews').text.split()[0]
            info['reviewCount'] = soup.find_all('a', 'gr-hyperlink', href='#other_reviews')[1].text.split()[0]
            plot = soup.find('div', id='description')
            if plot:
                info['plot'] = clean_str(plot.find_all('span')[-1].text)
            else:
                info['plot'] = ''
            numberOfPages = soup.find('span', itemprop='numberOfPages')
            if numberOfPages:
                info['numberOfPages'] = numberOfPages.text.split()[0]
            else:
                info['numberOfPages'] = ''
            published = soup.find_all('div', 'row')
            if len(soup.find_all('div', 'row')) > 1:
                info['published'] = get_publication_date(published[1].text)
            else:
                info['published'] = ''
            characters = soup.find('div', 'infoBoxRowTitle', string=re.compile("Characters"))
            if characters:
                info['characters'] = clean_str(re.sub('...(less|more)', '',
                                                      characters.find_next_sibling('div').text)).split(', ')
            else:
                info['characters'] = []
            setting = soup.find('div', 'infoBoxRowTitle', string=re.compile("Setting"))
            if not setting:
                info['setting'] = []
            else:
                setting = setting.find_next_sibling('div').find_all('a')
                info['setting'] = [clean_str(s.text) for s in setting]
            info['url'] = soup.find('meta', property='og:url')['content']
            return info
    except IOError:
        return None


def from_html_to_tsv(html_path, tsv_path):
    with open(tsv_path, mode='w', encoding="utf8") as tsv_file:
        if not os.path.isfile(html_path):
            tsv_file.close()
            return
        html_info = parse(html_path)
        try:
            if html_info['plot'] and (detect(html_info['plot']) != 'en'):
                print('Not English:', html_info)
                tsv_file.close()
                return
        except:
            print('Exception', html_info)
            tsv_file.close()
            return

        # print the keys on file
        tsv_file.write('\t'.join(html_info.keys()))
        tsv_file.write('\n')

        # print the values on file
        for k in html_info:
            if k in ['bookAuthors', 'characters', 'setting']:
                tsv_file.write(from_list_to_str(html_info[k]) + '\t')
            elif k == 'url':
                tsv_file.write(html_info[k])
            else:
                tsv_file.write(html_info[k] + '\t')


def process_pages(starting_page, ending_page, page_folder='./data/', destination_folder='./data/tsv/',
                  html_prefix='book', tsv_prefix='article', n_book_per_page=100, starting_number=1,
                  print_page=False, print_book=False):
    for num_page in range(starting_page, ending_page + 1):
        if print_page:
            print('Page:', num_page)
        for i in range(19704, n_book_per_page):
            if print_book:
                print('Book:', i)
            idx = str((num_page - 1) * n_book_per_page + i + starting_number)
            html_path = page_folder + 'page_' + str(num_page) + '/' + html_prefix + '_' + idx + '.html'
            tsv_path = destination_folder + tsv_prefix + '_' + idx + '.tsv'
            from_html_to_tsv(html_path, tsv_path)


if __name__ == '__main__':
    process_pages(1, 1, n_book_per_page=30000, starting_number=0, tsv_prefix='book')
