# Ariel Traver and Jennifer Shan
# crud.py

import cs304dbi as dbi

def check_tt(conn, tt):
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        select title, `release`, director, addedby
        from movie
        where tt = %s''', (tt))
    return curs.fetchall()

def insert_mov(conn, tt, title, release, addedby):
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        insert into movie
        values (%s, %s, %s, %s, %s)''', (tt, title, release, None, addedby))
    conn.commit()
    return

def update_mov(conn, tt, newtt, title, release, director, addedby):
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        update movie set tt = %s, title = %s, `release` = %s, director = %s, addedby = %s
        where tt = %s''', (newtt, title, release, director, addedby, tt))
    conn.commit()
    return

def delete_mov(conn, tt):
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        delete from movie where tt = %s''', (tt))
    conn.commit()
    return

def select_mov(conn):
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        select tt, title
        from movie
        where director is null or `release` is null''')
    return curs.fetchall()