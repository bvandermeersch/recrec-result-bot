# check if match was inserted
def check_for_match(conn, season_id, match_id):
    sql = "SELECT * FROM matches WHERE season_id = %s and match_id = %s"
    cursor = conn.cursor()
    cursor.execute(sql, (season_id, match_id))
    rowcount = cursor.rowcount
    cursor.close()

    return rowcount

# insert a reported match
def insert_match(conn, season_id,match_id):
    sql = "INSERT INTO matches (season_id, match_id) VALUES (%s, %s)"
    cursor = conn.cursor()
    cursor.execute(sql, (season_id, match_id))
    conn.commit()
    cursor.close()

    return