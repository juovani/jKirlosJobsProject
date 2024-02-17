import main
from main import search_save, open_db, setup_db, close_db


def test_search():
    connection, cursor = open_db(":memory:")
    setup_db(cursor)
    for value in range(1, 6):
        search_save(value, cursor)
    cursor.execute("SELECT * FROM jobs")
    result = cursor.fetchall()
    assert len(result) == 50
    close_db(connection)

def test_insert_data():
    conn, cursor = main.open_db("TestDB")
    main.setup_db(cursor)
    sample_job = ("IDzxcvergqaer", "Test Job", "Comp490 Inc", "Work really hard and learn a lot",
                  "Bridgewater, MA", 50000, 90000, "Yearly", "Tomorrow",
                  "https://webhost.bridgew.edu/jsantore/Spring2024/Capstone/Project1Sprint2.html", True)
    main.make_initial_jobs(cursor, sample_job)
    cursor.execute("""SELECT job_title, location, salary
    FROM jobs WHERE job_id = ?""", (sample_job[0],))
    record = cursor.fetchone()
    assert record[0] == "Test Job"
    assert record[1] == "Bridgewater, MA"
    assert record[2] == 50000