import main

def test_search():
    connection, cursor = main.open_db(":memory:")
    main.setup_db(cursor)
    for value in range(1, 6):
        main.search_save(value, cursor)
    cursor.execute("SELECT * FROM jobs")
    result = cursor.fetchall()
    assert len(result) == 50
    main.close_db(connection)

def test_insert_data():
    try:
        conn, cursor = main.open_db("TestDB")  # Open a test database
        main.setup_db(cursor)
        sample_job = ("Test Job", "Comp490 Inc", "Bridgewater, MA", "Work really hard and learn a lot",
                      "Tomorrow", None, None, "Yearly")
        main.make_initial_jobs(cursor, sample_job)
        cursor.execute("""SELECT job_title, location, salary
                          FROM jobs WHERE job_title = ?""", (sample_job[0],))
        record = cursor.fetchone()
        assert record[0] == sample_job[0]  # Check job title
        assert record[1] == sample_job[2]  # Check location
        assert record[2] == sample_job[5]  # Check salary
        print("Data insertion test passed successfully.")
    except Exception as e:
        print("Data insertion test failed:", e)
    finally:
        if conn:
            main.close_db(conn)  # Close the database connection