#!/usr/bin/env python3

import sqlite3

conn = sqlite3.connect('fefe.db')
c = conn.cursor()
c.execute("CREATE table posts (id INTEGER PRIMARY KEY, fefeid TEXT, diasporaid TEXT, post TEXT)")
conn.commit()
c.close()
