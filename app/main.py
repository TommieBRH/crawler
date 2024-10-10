import requests
from bs4 import BeautifulSoup

file = open("output.txt", "a")

def getUrls(base: str, count: int = 0, urls=[], url_history = {}, stop: int = 1, uri_count: int = 0):
    soup = None
    error = False

    if count >= stop:
        return

    base_url = f"https://{base}"
    urls.append(f"{base_url}/")

    if count not in url_history:
        url_history[count] = [base_url]
    else:
        url_history[count].append(base_url)

    new_count = count + 1
    if new_count not in url_history:
        url_history[new_count] = []

    update_uri_count = uri_count
    for v in url_history[count]:
        error = False
        resp = requests.get(v)
        soup = BeautifulSoup(resp.text, "html.parser")

        for link in soup.find_all("a"):
            uri = link.get("href")

            if uri and "/" in uri and uri != "/":
                if "https" not in uri and "http" not in uri:
                    if not uri.startswith("/"):
                        uri = f"/{uri}"
                    uri = f"{base_url}{uri}"

                for k, arr in url_history.items():
                    if uri in arr:
                        error = True
                    else:
                        error = False

                if uri.startswith(base_url) and uri not in urls and not error:
                    update_uri_count += 1
                    urls.append(uri)
                    url_history[new_count].append(uri)
                    print(uri)
                    file.write(f"{uri} \n")

    getUrls(base=base, count=new_count, urls=urls, url_history=url_history, stop=stop, uri_count=update_uri_count)


urls = getUrls(base="broekhuis-hosting.broekhuis.online", stop=10)
file.close()