#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

def add_tags(text):
  tags=""

  # Fefe
  if re.search("Das merken die NIE!",text,re.I):
    tags+="#dasmerkendienie "
  
  if re.search("Die BESTEN der BESTEN der BESTEN",text,re.I):
    tags+="#diebestenderbestenderbesten "

  if re.search("Die BESTEN der BESTEN der BESTEN, Sir",text,re.I):
    tags+="#diebestenderbestenderbestensir "

  if re.search("Bei uns ist Kernkraft sicher",text,re.I) or re.search("Bei uns ist die Kernkraft sicher",text,re.I) or re.search("Bei uns ist Atomkraft sicher",text,re.I) or re.search("Bei uns ist die Atomkraft sicher",text,re.I):
    tags+="#beiunsistKernkraftSICHER "

  if re.search("Verräterpartei",text,re.I):
    tags+="#verräterpartei "

  if re.search("Fnord",text):
    tags+="#fnord "

  if re.search("Contentmafia",text,re.I):
    tags+="#contentmafia "

  if re.search("Alternativlos",text,re.I):
    tags+="#alternativlos "

  if re.search("Captain Obvious",text,re.I):
    tags+="#CaptainObvious "

  if re.search("klarer Fall von Notwehr",text,re.I):
    tags+="#klarerfallvonnotwehr "

  if re.search("ehemaliges Nachrichtenmagazin",text,re.I) or re.search("ehemalige Nachrichtenmagazin",text,re.I) or re.search("ehemaligen Nachrichtenmagazin",text,re.I) :
    tags+="#ehemaligesNachrichtenmagazin "

  if re.search("keinerlei Gefahr für",text,re.I) or re.search("Gefahr für die Bevölkerung",text,re.I) or re.search("zu keinem Zeitpunkt eine Gefahr",text,re.I) or re.search("zu keinem Zeitpunkt irgendeine Gefahr",text,re.I):
    tags+="#zukeinemZeitpunktbestandGefahrfürdieBevölkerung "

  if re.search("DAMIT konnte ja wohl NIEMAND rechnen",text,re.I) or re.search("damit konnte ja auch niemand rechnen",text,re.I) or re.search("damit konnte niemand rechnen",text,re.I) or re.search("Damit konnte auch NIEMAND rechnen",text,re.I):
    tags+="#damitkonnteniemandrechnen "

  # Politik
  if re.search("Verfassungsschutz",text,re.I):
    tags+="#verfassungsschutz "

  if re.search("Piraten",text,re.I):
    tags+="#piraten "

  if re.search("FDP",text):
    tags+="#fdp "

  if re.search("SPD",text):
    tags+="#spd "

  if re.search("CDU",text):
    tags+="#cdu "

  if re.search("Grüne",text):
    tags+="#grüne "

  if re.search("Gauck",text):
    tags+="#gauck "

  if re.search("Wulff",text):
    tags+="#wulff "

  if re.search("ACTA",text,re.I):
    tags+="#acta "

  if re.search("Atomenergie",text,re.I):
    tags+="#atomenergie "

  if re.search("AKW",text):
    tags+="#akw "

  if re.search("EU",text):
    tags+="#EU "

  if re.search("BKA",text):
    tags+="#bka "

  if re.search("BND",text):
    tags+="#bnd "

  # CCC
  if re.search(" CCC",text):
    tags+="#ccc "

  if re.search("25c3",text,re.I):
    tags+="#25c3 "

  if re.search("26c3",text,re.I):
    tags+="#26c3 "

  if re.search("27c3",text,re.I):
    tags+="#27c3 "

  if re.search("28c3",text,re.I):
    tags+="#28c3 "

  if re.search("29c3",text,re.I):
    tags+="#29c3 "

  if re.search("30c3",text,re.I):
    tags+="#30c3 "

  if re.search("31c3",text,re.I):
    tags+="#31c3 "

  if re.search("32c3",text,re.I):
    tags+="#32c3 "

  if re.search("33c3",text,re.I):
    tags+="#33c3 "

  # Security
  if re.search("Malware",text,re.I):
    tags+="#malware "
  
  if re.search("Trojaner",text,re.I):
    tags+="#trojaner "

  # Netzthemen
  if re.search("facebook",text,re.I):
    tags+="#facebook "

  if re.search("twitter",text,re.I):
    tags+="#twitter "

  if re.search("google",text,re.I):
    tags+="#google "

  if re.search("DRM",text):
    tags+="#drm "

  if re.search("Ubuntu",text,re.I):
    tags+="#ubuntu "

  if re.search("Linux",text):
    tags+="#linux "

  if re.search("Microsoft",text,re.I):
    tags+="#microsoft "

  # Sonstiges
  if re.search("FAZ",text):
    tags+="#faz "

  if re.search(" taz",text):
    tags+="#taz "


  return tags
