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
        conn, cursor = main.open_db("TestDB")
        main.setup_db(cursor)
        sample_job = ("Test Job", "Comp490 Inc", "Bridgewater, MA", "Work really hard and learn a lot",
                      "Tomorrow", None, None, "Yearly")
        main.make_initial_jobs(cursor, sample_job)
        cursor.execute("""SELECT job_title, location, salary
                          FROM jobs WHERE job_title = ?""", (sample_job[0],))
        record = cursor.fetchone()
        assert record[0] == sample_job[0]
        assert record[1] == sample_job[2]
        assert record[2] == sample_job[5]
        print("Data insertion test passed successfully.")
    except Exception as e:
        print("Data insertion test failed:", e)
    finally:
        if conn:
            main.close_db(conn)


def test_excel_data_goes_into_table():
    try:
        conn, cursor = main.open_db("TestDB")
        main.setup_db(cursor)
        excel_data = main.read_excel_data("Sprint3Data.xlsx")
        main.make_initial_jobs_from_excel(cursor, excel_data)
        cursor.execute("""SELECT *
                          FROM excel_data WHERE id = 1""")
        record = cursor.fetchone()
        expected_data = excel_data[0]
        assert record == expected_data, f"Expected: {expected_data}, Actual: {record}"

        print("New Excel data goes into table test passed successfully.")
    except Exception as e:
        print("New Excel data goes into table test failed:", e)
    finally:
        if conn:
            main.close_db(conn)


def test_read_at_least_300_rows():
    data = main.read_excel_data("Sprint3Data.xlsx")
    assert len(data) >= 300


def test_read_multiple_columns():
    data = main.read_excel_data("Sprint3Data.xlsx")
    assert all(len(row) >= 2 for row in data)

