import json
from serpapi import GoogleSearch
from secrets import apiKey


def offset_calc(values):
    print(values)
    return (values - 1) * 10


for value in range(1, 6):
    offset = offset_calc(value)
    params = {
        "api_key": apiKey,
        "engine": "google_jobs",
        "google_domain": "google.com",
        "q": "software developer",
        "hl": "en",
        "gl": "us",
        "location": "Boston, Massachusetts, United States",
        "start": offset
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    job_results = results.get("jobs_results", [])

    with open("results.json", "a") as f:
        json.dump(job_results, f)

    # with open("results.json", "w") as f:
    #     json.dump(results.get("jobs_results"), f)
