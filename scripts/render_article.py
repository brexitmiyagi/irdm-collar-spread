# fills the article template with results/article_numbers.json, so every number in the text comes from one anchor
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
v = json.load(open(os.path.join(HERE, '..', 'results', 'article_numbers.json')))
t = open(os.path.join(HERE, sys.argv[1])).read()
print(t.format(**v), end='')
