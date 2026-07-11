"""
Yandex Reverse Image Search API: A Quick Start Example
See more at: https://apify.com/johnvc/yandex-reverse-image-search?fpr=9n7kx3
Input schema: https://apify.com/johnvc/yandex-reverse-image-search/input-schema?fpr=9n7kx3

This script shows how to call the Yandex Reverse Image Search API on Apify from
Python and read its structured JSON output. You give it the URL of an image and
it returns where that image appears online, visually similar images, other sizes
and resolutions, matching shop products, and descriptive tags. It exercises
several input parameters so you can see what is configurable, while keeping the
run small so your first call stays cheap.

Get your free Apify API key at: https://apify.com?fpr=9n7kx3
"""

import os
from collections import Counter

from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

# Initialize the Apify client with your API token (read from .env)
client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Build the Actor input.
# Inputs are kept small (the two default result types, a low max_results cap) to
# keep this first run inexpensive. Billing is one charge per result row returned,
# so turning on more result types or raising max_results increases cost. Raise
# these once you have your own API key and know your budget.
run_input = {
    # A public http(s) URL of the image to search by. Yandex fetches this URL,
    # so it must be reachable from the internet (no localhost or login-gated links).
    "image_url": "https://substack-post-media.s3.amazonaws.com/public/images/edbfb2cd-ebcb-4527-bec7-5315c182278f_445x445.png",

    # Optional: search only part of the image. Four ';'-separated fractions 0-1
    # in the order left;top;right;bottom. Left blank here to search the whole image.
    # "crop": "0.1;0.2;0.9;0.8",

    # Result types (a la carte). Only the ones you enable produce billable rows.
    "include_matching_pages": True,    # pages where the image appears online
    "include_similar_images": True,    # visually similar images from the web
    "include_image_sizes": False,      # other resolutions of the same image
    "include_image_tags": False,       # descriptive tags for the image content
    "include_shopping_results": False,  # matching products with prices
    "include_knowledge_graph": False,  # entity card for a recognizable subject

    # Regional Yandex domain to search from. One of: yandex.com, yandex.ru,
    # yandex.by, yandex.kz, yandex.uz, yandex.com.tr.
    "yandex_domain": "yandex.com",

    # Hard cap on rows returned and billed. 0 = everything found. A small number
    # keeps this first run cheap.
    "max_results": 20,
}

# Run the Actor and wait for it to finish
run = client.actor("johnvc/yandex-reverse-image-search").call(run_input=run_input)
if run is None:
    raise SystemExit("The Actor run did not return a result.")

# Read structured results from the run's default dataset
# (apify-client 3.x returns a Run object; use .default_dataset_id, not run["..."])
items = list(client.dataset(run.default_dataset_id).iterate_items())
print(f"Returned {len(items)} row(s).\n")

# Each row carries a result_type so you can filter. Count them first.
counts = Counter(item.get("result_type", "unknown") for item in items)
print("Rows by result_type:")
for result_type, count in counts.most_common():
    print(f"  {result_type}: {count}")
print()

# Show a few key fields from each row.
for item in items:
    result_type = item.get("result_type", "")
    title = item.get("title") or item.get("source") or ""
    link = item.get("link") or item.get("original") or ""
    source = item.get("source", "")
    print(f"[{result_type}] {title}")
    if source:
        print(f"    source: {source}")
    if link:
        print(f"    link:   {link}")
    print()
