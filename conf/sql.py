import sys, os
import json

import sqlite3 as sql
from sqlite3 import Error

from datetime import datetime



def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sql.connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def sql_delete(table, where={}):
    cur = conn.cursor()
    try:
        w = ""
        if isinstance(where, dict):
            args = []
            for key, value in where.items():
                arg = str(key) + "="
                if isinstance(value, int):
                    arg = arg + str(value)
                else:
                    arg = arg + "'" + str(value).replace('\\', '\\\\').replace('\'', '\'\'') + "'"
                args.append(arg)
            if args:
                w = "WHERE " + " AND ".join(args)

        cur.execute(f""" DELETE FROM {table} {w}; """)
        conn.commit()
        cur.close()
        if res:
            return res
        else:
            return None
    except Exception as e:
        print(e)
        if cur:
            cur.close()
    return None

def sql_select(target, table, where={}, order={}, limit=0):
    cur = conn.cursor()
    try:
        if isinstance(target, list):
            t = ", ".join(target)
        elif target:
            t = str(target)
        else:
            t = "*"
        w = ""
        l = ""
        o = ""
        if isinstance(where, dict):
            args = []
            for key, value in where.items():
                arg = str(key) + "="
                if isinstance(value, int):
                    arg = arg + str(value)
                else:
                    arg = arg + "'" + str(value).replace('\\', '\\\\').replace('\'', '\'\'') + "'"
                args.append(arg)
            if args:
                w = "WHERE " + " AND ".join(args)
        if limit > 0:
            l = "LIMIT " + str(int(limit))
        if isinstance(order, dict):
            args = []
            for key, value in order.items():
                if value:
                    arg = str(key) + " " + "ASC"
                else:
                    arg = str(key) + " " + "DESC"
                args.append(arg)
            if args:
                o = "ORDER BY " + ", ".join(args)


        cur.execute(f""" SELECT {t} FROM {table} {w} {o} {l}; """)
        res = cur.fetchall()
        cur.close()
        if res:
            return res
        else:
            return None
    except Exception as e:
        print(e)
        if cur:
            cur.close()
    return None

def sql_select_one(target, table, where={}, order={}, limit=0):
    cur = conn.cursor()
    try:
        if isinstance(target, list):
            t = ", ".join(target)
        elif target:
            t = str(target)
        else:
            t = "*"
        w = ""
        l = ""
        o = ""
        if isinstance(where, dict):
            args = []
            for key, value in where.items():
                arg = str(key) + "="
                if isinstance(value, int):
                    arg = arg + str(value)
                else:
                    arg = arg + "'" + str(value).replace('\\', '\\\\').replace('\'', '\'\'') + "'"
                args.append(arg)
            if args:
                w = "WHERE " + " AND ".join(args)
        if limit > 0:
            l = "LIMIT " + str(int(limit))
        if isinstance(order, dict):
            args = []
            for key, value in order.items():
                if value:
                    arg = str(key) + " " + "ASC"
                else:
                    arg = str(key) + " " + "DESC"
                args.append(arg)
            if args:
                o = "ORDER BY " + ", ".join(args)


        cur.execute(f""" SELECT {t} FROM {table} {w} {o} {l}; """)
        res = cur.fetchone()
        cur.close()
        if res:
            return res
        else:
            return None
    except Exception as e:
        print(e)
        if cur:
            cur.close()
    return None

def sql_insert(target: dict, table):
    assert target, "Values is None"

    cur = conn.cursor()
    try:
        names = []
        values = []
        for key, value in target.items():
            names.append(str(key))
            if isinstance(value, int):
                values.append(str(value))
            else:
                values.append("'" + str(value).replace('\\', '\\\\').replace('\'', '\'\'') + "'")
        names = ",".join(names)
        values = ",".join(values)
        cur.execute(f""" INSERT INTO {table}({names}) VALUES ({values}); """)
        conn.commit()
        cur.close()
        return True
    except Exception as e:
        print(e)
        if cur:
            cur.close()
        return False

def sql_update(target: dict, table, where={}):
    assert target, "Values is None"

    cur = conn.cursor()
    try:
        w = ""
        if isinstance(where, dict):
            args = []
            for key, value in where.items():
                arg = str(key) + "="
                if isinstance(value, int):
                    arg = arg + str(value)
                else:
                    arg = arg + "'" + str(value).replace('\\', '\\\\').replace('\'', '\'\'') + "'"
                args.append(arg)
            if args:
                w = "WHERE " + " AND ".join(args)
        s = []
        for key, value in target.items():
            if isinstance(value, int):
                val = value
            else:
                val = "'" + str(value).replace('\\', '\\\\').replace('\'', '\'\'') + "'"
            s.append(f"{key}={val}")
        s = ",".join(s)
        cur.execute(f""" UPDATE {table} SET {s} {w}; """)
        conn.commit()
        cur.close()
    except Exception as e:
        print(e)
        if cur:
            cur.close()

def sql_execute(transaction):
    cur = conn.cursor()
    try:
        cur.execute(str(transaction))
        conn.commit()
        cur.close()
    except Exception as e:
        print(e)
        if cur:
            cur.close()



# ----------------------------------------
#          Working Functions
# ----------------------------------------

def add_invuser_city(name, chat_id, city: str, club: str='vtk'):
    sql_insert({"name": name, "chat_id": str(chat_id), "city": city, "club": club}, "InviteUsers")
    sql_update({
                "name": name,
                "is_complete": 0,
                "city": city,
                "names": [],
                "imeninnik_name": '-',
                "date_ts": 0,
                "club": club,
            }, "InviteUsers", where={"chat_id": str(chat_id)})
    
def set_invuser_city(chat_id, city: str):
    sql_update({"city": city}, "InviteUsers", where={"chat_id": str(chat_id)})
    
def set_invuser_imeninnikname(chat_id, imeninnik_name: str):
    sql_update({"imeninnik_name": imeninnik_name}, "InviteUsers", where={"chat_id": str(chat_id)})
    
def set_invuser_date(chat_id, date: datetime):
    sql_update({"date_ts": int(date.timestamp())}, "InviteUsers", where={"chat_id": str(chat_id)})
    
def set_invuser_minutes(chat_id, date_result: datetime):
    data = sql_select_one([
            "date_ts"
        ], "InviteUsers", where={"chat_id": str(chat_id)})

    if not data:
        return False
    
    date = datetime.fromtimestamp(data[0])
    date = datetime(date.year, date.month, date.day, date_result.hour, date_result.minute, 0, 0)
    
    sql_update({"date_ts": int(date.timestamp())}, "InviteUsers", where={"chat_id": str(chat_id)})
    
    return date
    
def add_invuser_name(chat_id, name: str):
    name = name.lower()
    
    data = sql_select_one([
            "names"
        ], "InviteUsers", where={"chat_id": str(chat_id)})

    if not data:
        return False

    try:
        names = json.loads(data[0].lower())
    except:
        names = []
        
    # Если имя уже добавлено - не добавлять и сообщить пользователю
    if name in names:
        return name
    
    names.append(name)

    nn = "[" + ",".join(names) + "]"
    print(nn)
    sql_update({"names": nn}, "InviteUsers", where={"chat_id": str(chat_id)})

    return True

def remove_invuser_name(chat_id, name: str):
    name = name.lower()
    
    data = sql_select_one([
            "names"
        ], "InviteUsers", where={"chat_id": str(chat_id)})

    if not data:
        return False

    try:
        names = json.loads(data[0].lower())
    except:
        names = []
        
    new_names = []
    for n in names:
        if n == name:
            continue
        new_names.append(n)

    nn = "[" + ",".join(new_names) + "]"
    sql_update({"names": nn}, "InviteUsers", where={"chat_id": str(chat_id)})

    return True

def get_invuser_names(chat_id):
    data = sql_select_one([
            "names"
        ], "InviteUsers", where={"chat_id": str(chat_id)})

    if not data:
        return []

    try:
        names = json.loads(data[0].lower())
    except Exception as e:
        print(e)
        names = []
        
    nn = []
    for name in names:
        nn.append(name.lower().title())
        
    return nn


def get_invuser_status(chat_id):
    data = sql_select_one([
            "is_complete",      # 0
            "city",             # 1
            "names",            # 2
            "imeninnik_name",   # 3
            "date_ts"           # 4
        ], "InviteUsers", where={"chat_id": str(chat_id)})

    if not data:
        return False

    # is_complete
    if data[0] != 0:
        return "complete"
    
    # city
    if data[1] != '-' and (data[3] == '-'):
        return "imeninnik_name"
    
    # imeninnik_name
    if data[3] != '-' and (data[4] == 0):
        return "date"
    
    # date
    if data[4] != 0:
        date = (datetime.fromtimestamp(data[4]))
        if date.hour == 0 and date.minute == 0:
            return "minutes"
        
    return "name"


def get_invuser_info(chat_id):
    data = sql_select_one([
            "imeninnik_name",
            "date_ts",
            "club"
        ], "InviteUsers", where={"chat_id": str(chat_id)})

    if not data:
        return []
        
    return data[0], (datetime.fromtimestamp(data[1])), data[2]


# ----------------------------------------
#            Dialog Statuses
# ----------------------------------------

def add_dialog_data(chat_id, status: str='-'):
    sql_insert({"chat_id": str(chat_id), "status": status}, "DialogStatuses")
    sql_update({
                "status": status
            }, "DialogStatuses", where={"chat_id": str(chat_id)})
    
    
def get_dialog_status(chat_id):
    data = sql_select_one([
            "status",      # 0
            "data"         # 1
        ], "DialogStatuses", where={"chat_id": str(chat_id)})

    if not data:
        add_dialog_data(chat_id, '-')
        return ('-', '')
        
    return (data[0], data[1])


def set_dialog_status(chat_id, status, data=''):
    sql_update({"status": str(status), "data": str(data)}, "DialogStatuses", where={"chat_id": str(chat_id)})
    

# ----------------------------------------
#            Start Database
# ----------------------------------------


sql_create_invite_users_table = """ CREATE TABLE IF NOT EXISTS InviteUsers (
                                    uid INTEGER PRIMARY KEY,
                                    name TEXT,
                                    chat_id TEXT UNIQUE,
                                    is_complete INTEGER DEFAULT 0,
                                    city TEXT DEFAULT "-",
                                    names TEXT DEFAULT "[]",
                                    imeninnik_name TEXT DEFAULT "-",
                                    date_ts INTEGER DEFAULT 0,
                                    club TEXT DEFAULT "vtk"
                                ); """
                                
sql_create_dialog_statuses_table = """ CREATE TABLE IF NOT EXISTS DialogStatuses (
                                    uid INTEGER PRIMARY KEY,
                                    chat_id TEXT UNIQUE,
                                    status TEXT DEFAULT "-",
                                    data TEXT DEFAULT ""
                                ); """




conn = create_connection(os.getcwd() + r"/conf/database.db")
assert conn != None, "Can't connect to Database"
create_table(conn, sql_create_invite_users_table)
create_table(conn, sql_create_dialog_statuses_table)
