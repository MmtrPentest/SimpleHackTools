import requests
import re
import json

def emails(text):
    pattern = r'[A-Za-z0-9+%-.]+@[A-Za-z0-9-.]+\.[A-Za-z]+'
    return set(re.findall(pattern, text))

def links(text):
    bad_result = set()
    pattern = r'href="(.+)"'
    bad_urls = [
        'mailto:(.+)',
        'tel:(.+)',
        'javascript:(.*)',
        '#(.*)'
    ]
    urls = set(re.findall(pattern, text))
    for url in urls:
        for bad_url in bad_urls:
            if re.fullmatch(bad_url, url) != None:
                bad_result.add(url)
    return urls-bad_result

def forms(text):
    form_attr = ('name', 'method', 'action')
    forms = dict()
    pattern = r'<form\s(.+?)>.*?</form>'
    for form_id, form in enumerate(re.findall(pattern, text, re.DOTALL)):
        forms[form_id] = dict()
        for attr in form_attr:
            match = re.search(attr + r'=["\'](.*?)["\']', form)
            if match:
                forms[form_id][attr] = match.group(1)
    pattern = r'<form\s.+?>(.*?)</form>'
    for form_id, form in enumerate(re.findall(pattern, text, re.DOTALL)):
        forms[form_id]['content'] = form
    return forms


def hr():
    print('*'*100)

url = 'http://evil.bigazzzz.ru:15073/test.html'
html_response = requests.request('GET', url)
''' в html_response.text - текст html-документа'''
site = dict()
site['url'] = url
site['response'] = html_response
site['emails'] = emails(html_response.text)
site['links'] = links(html_response.text)
site['forms'] = forms(html_response.text)

hr()
print(site)
