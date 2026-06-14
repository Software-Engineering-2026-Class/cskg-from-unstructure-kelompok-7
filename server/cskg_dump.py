import os

import requests

VIRTUOSO_ENDPOINT = os.getenv("VIRTUOSO_ENDPOINT", "http://localhost:8890/sparql")
GRAPH_URI = os.getenv("GRAPH_URI", "http://group2.org/cskg")
OUTPUT_FILE = os.getenv("OUTPUT_FILE", "cskg_full_dump.ttl")


def dump_ttl():
    print(f"Connecting to {VIRTUOSO_ENDPOINT}...")
    print(f"Dumping named graph <{GRAPH_URI}> only...")

    query = f"""
CONSTRUCT {{ ?s ?p ?o }}
WHERE {{ GRAPH <{GRAPH_URI}> {{ ?s ?p ?o }} }}
"""

    params = {
        "query": query,
        "format": "text/turtle",  # Request Turtle format
    }

    try:
        response = requests.get(
            VIRTUOSO_ENDPOINT,
            params=params,
            headers={"Accept": "text/turtle"},
            stream=True,
            timeout=60,
        )
        response.raise_for_status()

        print(f"Downloading graph to '{OUTPUT_FILE}'...")

        with open(OUTPUT_FILE, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Dump complete: {OUTPUT_FILE}")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Virtuoso. Is Docker running?")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    dump_ttl()
