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
