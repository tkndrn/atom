import requests

# base url al
r = requests.get("https://data-reality.com/domain.php")
base = r.json()["baseurl"]

with open("link.txt", "w") as f:
    f.write(base + "\n")
    f.write("https://milyontv3.com/")
