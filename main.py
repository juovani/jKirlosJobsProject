import json
from serpapi import GoogleSearch
from secrets import apiKey


def offset_calc(values):
    offset = (values - 1) * 10
    return offset


def search_save(value):
    params = {
        "api_key": apiKey,
        "engine": "google_jobs",
        "google_domain": "google.com",
        "q": "software developer",
        "hl": "en",
        "gl": "us",
        "location": "Boston, Massachusetts, United States",
        "start": offset_calc(value)
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    job_results = results.get("jobs_results", [])
    with open("results.json", "a") as f:
        json.dump(job_results, f)


def main():
    for value in range(1, 6):
        search_save(value)


if __name__ == "__main__":
    main()