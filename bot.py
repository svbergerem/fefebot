#! /usr/bin/env python3

import sqlite3
from time import gmtime, strftime
from xml.dom.minidom import parseString 
from fefe_tags import add_tags
import config
from diaspy_client import Client
from html2markdown import html2md
import urllib.request

def log_write(text):
    f = open('log.txt', 'a')
    f.write(strftime("%a, %d %b %Y %H:%M:%S ", gmtime()))
    f.write(text)
    f.write('\n')
    f.close()

# parse xml file
xmltree=parseString(urllib.request.urlopen(config.feedurl).read())
output=[]
guid=[]

for item in xmltree.getElementsByTagName('item'):
  link=item.getElementsByTagName('guid')[0].firstChild.data
  fefe_id=link[25:32]

  html=item.getElementsByTagName('description')[0].childNodes[1].data
  html=html2md(html)   
  html=html.encode('ascii','xmlcharrefreplace').decode("utf-8")

  guid.append(fefe_id)
  
  output.append("")
  output[len(output)-1]+="[[l]](" + link + ") "
  output[len(output)-1]+=html
  output[len(output)-1]+="\n"


conn = sqlite3.connect('fefe.db')
c = conn.cursor()
client=Client()

for i in range(len(output)-1,-1,-1):
  c.execute("SELECT post, diasporaid from posts WHERE fefeid=:guid", {"guid":guid[i]})
  post_in_db=c.fetchone()

  # post doesn't exist yet
  if post_in_db==None:
    text=output[i]
    text+="\n\n"
    text+=add_tags(output[i])
    post_id=client.post(text).id
    c.execute("INSERT INTO posts (fefeid,diasporaid,post) values (?,?,?)",(guid[i],post_id,output[i]))
    log_write("New Post: " + str(post_id))

  # post exists but was changed
  elif output[i]!=post_in_db[0]:
    len_db=len(post_in_db[0])
    len_out=len(output[i])
    if len_out>len_db and output[i][0:len_db]==post_in_db[0]:
      text=output[i][len_db:-1]
      client.comment(post_in_db[1], text)
      log_write("Commented on: " + str(post_in_db[1]))
    else:
      log_write("Not commented on: " + str(post_in_db[1]))
    c.execute("UPDATE posts SET post=:post WHERE diasporaid=:diasporaid",{"post":output[i],"diasporaid":post_in_db[1]})
conn.commit()
c.close()
