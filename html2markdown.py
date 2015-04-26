#! /usr/bin/env python3

import re
import html2text

def _fefe_linksintern(text):
  text=re.sub('^]\(\/\?ts=','](https://blog.fefe.de/?ts=',text)
  text=re.sub('^]\(\/\?q=','](https://blog.fefe.de/?q=',text)
  return text

def html2md(html):
  parser = html2text.HTML2Text()
  parser.body_width = 0;
  parser.protect_links = True;

  html = parser.handle(html)
  html = _fefe_linksintern(html)
  return html
