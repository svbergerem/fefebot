#! /usr/bin/env python3.2

import sqlite3
from time import gmtime, strftime
from xml.dom.minidom import parseString 
import re
from difflib import SequenceMatcher
from tags import add_tags
import config
import diaspy
import urllib.request

__pod__ = config.__pod__
__username__ = config.__username__
__passwd__ = config.__passwd__
__feedurl__ = config.__feedurl__

def post(connection, text):
  return diaspy.streams.Stream(connection).post(text, provider_display_name='fefebot').id

def comment(connection, post_id, text):
  diaspy.models.Post(connection,id=post_id).comment('text')

def subpre(text):
  list=re.split('(<pre>|</pre>)',text)
  for i in range(len(list)):
    # begin of pre
    if i%4==1:
      list[i]='\n\n    '
    # in pre
    elif i%4==2:
      list[i]=re.sub('<p>|<br>|\n\n', '\n\n    ',list[i])
    # end of pre
    elif i%4==3:
      list[i]='\n\n'
  return ''.join(list)

def subblock(text):
  list=re.split('(<blockquote>|</blockquote>)',text)
  for i in range(len(list)):
    # begin of blockquote
    if i%4==1:
      list[i]='\n\n> '
    # in blockquote
    elif i%4==2:
      list[i]=re.sub('<p>|<br>|\n\n', '\n\n> ',list[i])
    # end of blockquote
    elif i%4==3:
      list[i]='\n\n'
  return ''.join(list)

def sublinks(text):
  return re.sub('<a href=\"(?P<link>.*?)\">(?P<linktext>.*?)</a>', lambda m : '[' + markdownify_linktext(m.group('linktext')) + '](' + fefe_linksintern(m.group('link')) + ')', text)

def markdownify(text):
  list=re.split('(\[.*\]\(.*\))',text)
  for i in range(len(list)):
    # only change when not a link
    if i%2==0:
      list[i]=re.sub('\*','\\*',list[i])
      list[i]=re.sub('_','\\_',list[i])
      list[i]=re.sub('<b>','**',list[i])
      list[i]=re.sub('</b>','**',list[i])
      list[i]=re.sub('<i>','_',list[i])
      list[i]=re.sub('</i>','_',list[i])
      list[i]=re.sub('<u>','\n',list[i])
      list[i]=re.sub('</u>','\n',list[i])
      list[i]=re.sub('<li>','\n - ',list[i])
      list[i]=re.sub('</li>','\n',list[i])
      list[i]=re.sub('<p>','\n\n',list[i])
      list[i]=re.sub('</p>','\n\n',list[i])
      list[i]=re.sub('<br>','\n\n',list[i])
  return ''.join(list)

def markdownify_linktext(text):
  list=re.split('(\[.*\]\(.*\))',text)
  for i in range(len(list)):
    # only change when not a link
    if i%2==0:
      list[i]=re.sub('\*','\\*',list[i])
      list[i]=re.sub('_','\\_',list[i])
      list[i]=re.sub('<b>','**',list[i])
      list[i]=re.sub('</b>','**',list[i])
      list[i]=re.sub('<i>','_',list[i])
      list[i]=re.sub('</i>','_',list[i])
  return ''.join(list)

def fefe_linksintern(text):
  text=re.sub('^\/\?ts=','https://blog.fefe.de/?ts=',text)
  text=re.sub('^\/\?q=','https://blog.fefe.de/?q=',text)
  return text

diaspora_connection = diaspy.connection.Connection( pod= __pod__ , username= __username__ , password= __passwd__ )
diaspora_connection.login()
xmltree=parseString(urllib.request.urlopen( __feedurl__ ).read())
output=[]
guid=[]
for item in xmltree.getElementsByTagName('item'):
  link=item.getElementsByTagName('guid')[0].firstChild.data
  fefe_id=link[24:31]
  html=item.getElementsByTagName('description')[0].childNodes[1].data
  html=subpre(html)   
  html=subblock(html)   
  html=sublinks(html)
  html=markdownify(html)
  html=html.encode('ascii','xmlcharrefreplace')
  guid.append(fefe_id)
  output.append("")
  output[len(output)-1]+="[[l]](" + link + ") "
  output[len(output)-1]+=html.decode("utf-8")
  output[len(output)-1]+="\n"
conn = sqlite3.connect('fefe.db')
c = conn.cursor()
for i in range(len(output)-1,-1,-1):
  c.execute("SELECT post, diasporaid from posts WHERE fefeid=:guid", {"guid":guid[i]})
  post_in_db=c.fetchone()
  if post_in_db==None:
    text=output[i]
    text+="\n\n"
    text+=add_tags(output[i])
    post_id=post(diaspora_connection, text)
    c.execute("INSERT INTO posts (fefeid,diasporaid,post) values (?,?,?)",(guid[i],post_id,output[i]))
    log = open('log.txt', 'a')
    log.write(strftime("%a, %d %b %Y %H:%M:%S", gmtime()))
    log.write(" Post angelegt: ")
    log.write(str(post_id))
    log.write('\n')
    log.close()
  elif len(output[i])!=len(post_in_db[0]):
    s=SequenceMatcher(None,output[i],post_in_db[0])
    m=s.get_matching_blocks()
    #matched the last char of output[i] -> comment
    if m[-2][1]+m[-2][2]==len(post_in_db[0]):
      text=output[i][m[-2][0]+m[-2][2]:-1]
      comment(diaspora_connection, post_in_db[1], text)
      log = open('log.txt', 'a')
      log.write(strftime("%a, %d %b %Y %H:%M:%S", gmtime()))
      log.write(" Comment angelegt: ")
      log.write(str(post_in_db[1]))
      log.write('\n')
      log.close()
    else:
      log = open('log.txt', 'a')
      log.write(strftime("%a, %d %b %Y %H:%M:%S", gmtime()))
      log.write(" Error comment: ")
      log.write(str(post_in_db[1]))
      log.write('\n')
      log.close() 
    c.execute("UPDATE posts SET post=:post WHERE diasporaid=:diasporaid",{"post":output[i],"diasporaid":post_in_db[1]})
conn.commit()
c.close()
