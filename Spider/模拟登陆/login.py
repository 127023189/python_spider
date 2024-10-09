import requests



url = "https://www.luffycity.com/"

data = {
  "username": "17872295450",
  "password": "0520lijing"
}

header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "Cookie": "53gid2=16435661556003; 53gid0=16435661556003; 53gid1=16435661556003; 53revisit=1728130672716; 53kf_72415741_from_host=www.luffycity.com; 53kf_72415741_keyword=https%3A%2F%2Fcn.bing.com%2F; uuid_53kf_72415741=35aa41613265f89a40c68a7916f0518c; 53kf_72415741_land_page=https%253A%252F%252Fwww.luffycity.com%252F; kf_72415741_land_page_ok=1; 53uvid=1; onliner_zdfq72415741=0; visitor_type=old; token=490871774d73a9144104f67c73e676fed58dea71"
}

session = requests.Session()

response = session.post(url, data=data, headers=header)
page_text = response.text
print(page_text)
with open("login.html", "w", encoding="utf-8") as f:
    f.write(page_text)