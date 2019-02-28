from utils import fetch_pages, extract_urls, Url
from celery_app import app
import json

def children_to_visit(links, visited):
    return [l for l in links if not Url(l) in visited]

@app.task
def crawl(urls, depth):
    visited = []
    data = {}
    while depth > 0 and urls:
        res = []
        fetch_pages(res, urls)
        images, children = extract_urls(res)
        [visited.append(Url(url)) for url in urls if Url(url) not in visited]
        for k in images.keys():
            data[k] = images[k]
        urls = children_to_visit(children, visited)
        depth -= 1
    print(f"Computed data with {sum([len(x) for x in data.values()])} items.")
    return json.dumps(data)

if __name__ == '__main__':
    data = crawl(['https://www.cnn.com'], 1)
    print(data)
    
    