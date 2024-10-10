import requests
from bs4 import BeautifulSoup


def getUrls(base: str, count: int = 0, urls=[], url_history = {}, stop: int = 1):
    if count >= stop:
        return urls

    base_url = f"https://{base}"

    if count not in url_history:
        url_history[count] = [base_url]
    else:
        url_history[count].append(base_url)

    new_count = count + 1
    if new_count not in url_history:
        url_history[new_count] = []

    for v in url_history[count]:
        resp = requests.get(v)
        soup = BeautifulSoup(resp.text, "html.parser")
        for link in soup.find_all("a"):
            uri = link.get("href")

            if uri and "/" in uri and uri != "/":
                if "https" not in uri:
                    if not uri.startswith("/"):
                        uri = f"/{uri}"
                    uri = f"{base_url}{uri}"
                if base in uri and uri not in urls:
                    urls.append(uri)
                    url_history[new_count].append(uri)
                    if "fiets" in uri:
                        print(uri)
    getUrls(base=base, count=new_count, urls=urls, url_history=url_history, stop=stop)

urls = getUrls(base="broekhuis-hosting.broekhuis.online", stop=5)
print(urls)