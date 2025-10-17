#!/usr/bin/env python3
import os
import json
import time
import requests

BASE_URL = "https://mass.cultureelerfgoed.nl/api/v1"
CACHE_DIR = "cache"

LIST_URL = f"{BASE_URL}/list/nl/"
GET_URL_TEMPLATE = f"{BASE_URL}/get/nl/{{id}}"

# Ensure cache directory exists
os.makedirs(CACHE_DIR, exist_ok=True)

def cache_path(name):
    """Return the full path for a cache file."""
    return os.path.join(CACHE_DIR, name)

def load_from_cache(filename):
    """Return cached data if exists, else None."""
    path = cache_path(filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_to_cache(filename, data):
    """Save JSON data to cache."""
    path = cache_path(filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def fetch_json(url):
    """Fetch JSON from URL."""
    print(f"Fetching: {url}")
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def main():
    # Step 1: Fetch or load list
    list_cache = "list_nl.json"
    data_list = load_from_cache(list_cache)

    if data_list is None:
        data_list = fetch_json(LIST_URL)
        save_to_cache(list_cache, data_list)
        print("Fetched and cached list.")
        time.sleep(5)
    else:
        print("Loaded list from cache.")

    # Step 2: Fetch details for each element
    for item in data_list:
        item_id = item.get("id")
        if not item_id:
            continue

        filename = f"item_{item_id}.json"
        if load_from_cache(filename) is not None:
            print(f"Cache hit: {filename}")
            continue

        # Fetch and cache new item
        url = GET_URL_TEMPLATE.format(id=item_id)
        data = fetch_json(url)
        save_to_cache(filename, data)
        print(f"Fetched and cached {filename}.")
        time.sleep(5)

if __name__ == "__main__":
    main()

