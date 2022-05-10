# check if match was inserted
def check_for_match(conn, season_id, match_id):
    sql = "SELECT * FROM matches WHERE binary season_id = %s and binary match_id = %s"
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

# get active seasons
def get_seasons(conn):
    sql = "SELECT * FROM seasons WHERE active = 1"
    cursor = conn.cursor()
    cursor.execute(sql)
    seasons = cursor.fetchall()
    cursor.close()

    return seasons
