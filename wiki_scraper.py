import urllib
from pyquery import PyQuery

WIKI_URL = 'https://feheroes.gamepedia.com/Hero_List'

html = urllib.request.urlopen(WIKI_URL).read()
d = PyQuery(html)

unit_table = d('.wikitable').eq(0)
for hero_index in range(0, unit_table.children('.hero-filter-element').length):
    hero_html = unit_table.children('.hero-filter-element').eq(hero_index)
    name = hero_html.children('td').eq(0).children('a').eq(0).attr('title')
    print(name)