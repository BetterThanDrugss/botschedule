import sqlite3


def check_user(user):
    conn = sqlite3.connect("schbase.sqlite")
    cursor = conn.cursor()
    sql = ("SELECT * FROM sch WHERE ID = ?")
    cursor.execute(sql, [user])

    if cursor.fetchone() is not None:
        return True
    else:
        return False


def add_to_db(user_id, link):
    conn = sqlite3.connect("schbase.sqlite")
    cursor = conn.cursor()
    sql = ("INSERT INTO sch(ID, link) VALUES (?, ?)")
    cursor.execute(sql, (user_id, link))
    conn.commit()
    conn.close()


def get_user_link(user_id):
    conn = sqlite3.connect("schbase.sqlite")
    cursor = conn.cursor()
    sql = ("SELECT link FROM sch WHERE ID = ?")
    cursor.execute(sql, [user_id])
    conn.commit()
    temp = cursor.fetchall()
    conn.close()
    temp = temp[0]
    temp = temp[0]
    return temp


def update_link_db(us_id, link):
    conn = sqlite3.connect("schbase.sqlite")
    cursor = conn.cursor()
    sql = """ UPDATE sch SET link = ? WHERE ID = ?"""

    cursor.execute(sql, (link, us_id))
    conn.commit()
    conn.close()


def main():
    pass


if __name__ == "__main__":
    main()

