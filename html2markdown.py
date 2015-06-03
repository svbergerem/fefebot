#! /usr/bin/env python3.2

import re

def _subpre(text):
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

def _subblock(text):
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

def _sublinks(text):
  return re.sub('<a href=\"(?P<link>.*?)\">(?P<linktext>.*?)</a>', lambda m : '[' + _markdownify_linktext(m.group('linktext')) + '](' + _fefe_linksintern(m.group('link')) + ')', text)

def _markdownify(text):
  list=re.split('(\[.*\]\(.*\))',text)
  # only change when not a link
  for i in range(0,len(list),2):
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

def _markdownify_linktext(text):
  list=re.split('(\[.*\]\(.*\))',text)
  # only change when not a link
  for i in range(0,len(list),2):
    list[i]=re.sub('\*','\\*',list[i])
    list[i]=re.sub('_','\\_',list[i])
    list[i]=re.sub('<b>','**',list[i])
    list[i]=re.sub('</b>','**',list[i])
    list[i]=re.sub('<i>','_',list[i])
    list[i]=re.sub('</i>','_',list[i])
  return ''.join(list)

def _fefe_linksintern(text):
  text=re.sub('^\/\?ts=','https://blog.fefe.de/?ts=',text)
  text=re.sub('^\/\?q=','https://blog.fefe.de/?q=',text)
  return text

def html2md(html):
  html=_subpre(html)   
  html=_subblock(html)   
  html=_sublinks(html)
  html=_markdownify(html)
  return html
