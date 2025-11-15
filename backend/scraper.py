import requests
from bs4 import BeautifulSoup
import time

HEADERS = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64)"}

def scrape_nykaa(query, max_results=10):
    url = f"https://www.nykaa.com/search/result/?q={requests.utils.quote(query)}"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")
    items = []
    for el in soup.select("div.product-card")[:max_results]:
        # selectors can change — test & update
        title = el.select_one(".product-card__product-title")
        price = el.select_one(".post-card__content-price .price")
        link = el.select_one("a")
        if title and link:
            items.append({
                "name": title.get_text(strip=True),
                "price": price.get_text(strip=True) if price else None,
                "link": "https://www.nykaa.com" + link.get("href"),
                "source": "nykaa"
            })
    time.sleep(0.5)
    return items

def scrape_minimalist(query, max_results=8):
    url = f"https://minimalist.co/search?q={requests.utils.quote(query)}"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")
    items = []
    for el in soup.select(".product-card")[:max_results]:
        title = el.select_one(".product-card__title")
        link = el.select_one("a")
        if title and link:
            items.append({
                "name": title.get_text(strip=True),
                "link": "https://minimalist.co" + link.get("href"),
                "source": "minimalist"
            })
    time.sleep(0.5)
    return items

# high-level scraper that calls specific scrapers
def fetch_products_for_profile(profile, limit=8):
    """
    profile is dict with keys:
      - skin_type: 0-dry,1-normal,2-oily (or mapping you use)
      - acne_level: 0..3
      - skin_tone: 0..5
      - sensitive: bool
    Build queries based on simple rules.
    """
    queries = []
    if profile["acne_level"] >= 2:
        queries.append("salicylic acid face wash")
        queries.append("niacinamide serum")
    else:
        queries.append("gentle moisturizer")
        queries.append("spf sunscreen")

    # adjust with skin type
    if profile["skin_type"] == 2:  # oily
        queries.append("oil free moisturizer")
    elif profile["skin_type"] == 0:  # dry
        queries.append("hydrating moisturizer ceramides")

    # sensitive -> fragrance free
    if profile.get("sensitive"):
        queries = [q + " fragrance free" for q in queries]

    products = []
    # try multiple scrapers
    for q in queries:
        products += scrape_nykaa(q, max_results=4)
        products += scrape_minimalist(q, max_results=2)

    # simple dedupe by name
    seen = set()
    unique = []
    for p in products:
        key = p["name"].lower()
        if key not in seen:
            seen.add(key); unique.append(p)
        if len(unique) >= limit:
            break
    return unique
