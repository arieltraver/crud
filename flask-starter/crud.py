import cs304dbi as dbi
from pymysql import NULL

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
    return curs.fetchall()

#def update_mov(conn, tt, title, release, director, addedby):
    #curs = dbi.dict_cursor(conn)
    #curs.execute('''
        #update''')
    #conn.commit()
    #return