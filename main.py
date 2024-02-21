import sqlite3
import openpyxl
from serpapi import GoogleSearch
from secrets import api_key
from typing import Tuple


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)
    cursor = db_connection.cursor()
    return db_connection, cursor


def setup_db(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS excel_data(
    company_name TEXT,
    posting_age TEXT,
    job_id TEXT PRIMARY KEY,
    country TEXT,
    location TEXT,
    publications TEXT,
    salary_max TEXT,
    salary_min TEXT,
    salary_type TEXT,
    job_title TEXT
    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs(
    job_id INTEGER PRIMARY KEY,
    job_title TEXT NOT NULL,
    company_name TEXT NOT NULL,
    remote TEXT,
    location TEXT NOT NULL,
    when_posted TEXT NOT NULL,
    job_desc TEXT,
    salary TEXT
    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS  qualifications(
    job_id INTEGER PRIMARY KEY,
    job_title TEXT,
    company_name TEXT,
    qualifications TEXT,
    FOREIGN KEY (job_title) REFERENCES jobs (job_title)
    ON DELETE CASCADE ON UPDATE NO ACTION,
    FOREIGN KEY (company_name) REFERENCES jobs (company_name)
    ON DELETE CASCADE ON UPDATE NO ACTION
    );''')


def make_initial_jobs(cursor: sqlite3.Cursor, job_data: list):
    detected_extensions = job_data.get("detected_extensions")
    try:
        cursor.execute('''INSERT INTO JOBS (job_title, company_name, location, remote,
        job_desc, when_posted, salary)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (job_data.get("title"), job_data.get("company_name"),
                        job_data.get("location", "N/A"),
                        detected_extensions.get("work_from_home", "N/A"),
                        job_data.get("description"),
                        detected_extensions.get("posted_at", "N/A"),
                        detected_extensions.get("salary", "N/A")))
    except sqlite3.Error as e:
        print("Error inserting job data:", e)
    highlights = job_data.get("job_highlights")
    try:
        cursor.execute('''INSERT INTO QUALIFICATIONS(job_title, company_name, qualifications)
                              VALUES (?, ?, ?)''',
                       (job_data.get("title"), job_data.get("company_name"),
                        highlights[0].get("items")[0]))
    except sqlite3.Error as e:
        print("Error inserting job data:", e)


def make_initial_jobs_from_excel(cursor: sqlite3.Cursor, excel_data):
    for row in excel_data:
        try:
            cursor.execute('''INSERT INTO excel_data (company_name, posting_age, job_id, country,
            location, publications, salary_max, salary_min, salary_type, job_title)
                                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)
        except sqlite3.Error as e:
            print("Error inserting Excel data:", e)


def close_db(connection: sqlite3.Connection):
    connection.commit()
    connection.close()


def offset_calc(value):
    offset = (value - 1) * 10
    return offset


def search_save(value, cursor):
    params = {
        "api_key": api_key,
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
    for job_data in job_results:
        make_initial_jobs(cursor, job_data)


def read_excel_data(filename):
    workbook = openpyxl.load_workbook(filename)
    sheet = workbook.active
    data = []
    for row in sheet.iter_rows(values_only=True):
        data.append(row)
    return data


def main():
    try:
        connection, cursor = open_db("your_database.db")
        setup_db(cursor)
        excel_data = read_excel_data("Sprint3Data.xlsx")
        make_initial_jobs_from_excel(cursor, excel_data)
        for value in range(1, 6):
            search_save(value, cursor)
        close_db(connection)
        print("Data insertion completed successfully.")
    except Exception as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    main()
