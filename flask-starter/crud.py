import cs304dbi as dbi

def check_tt(conn, tt):
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        select *
        from movie
        where tt = %s''', [tt])
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
    #if tt != new tt:
     #if check_tt is not null then throw error
     #else update the tt
    curs.execute('''
        update movie
        set ''')
    conn.commit()
    return
