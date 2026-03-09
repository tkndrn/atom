import requests

# base url çek
r = requests.get("https://data-reality.com/domain.php")
base = r.json()["baseurl"]

# txt yaz
with open("link.txt", "w") as f:
    f.write(base)
