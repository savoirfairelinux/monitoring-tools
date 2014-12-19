#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import lxml.html

from math import ceil


def obtain_parse_wiki_snp500():
  """Download and parse the Wikipedia list of S&P500 
  constituents using requests and libxml.

  Returns a list of tuples for to add to MySQL."""

  # Stores the current time, for the created_at record
  now = datetime.datetime.utcnow()

  # Use libxml to download the list of S&P500 companies and obtain the symbol table
  page = lxml.html.parse('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
  symbolslist = page.xpath('//table[1]/tr')[1:]

  # Obtain the symbol information for each row in the S&P500 constituent table
  #symbols = []
  #for symbol in symbolslist:
  #  tds = symbol.getchildren()
   # sd = {'ticker': tds[0].text,
   #     'name': tds[1].text,
   #     'sector': tds[3].text}
    # Create a tuple (for the DB format) and append to the grand list
  #  symbols.append( (sd['ticker'], 'stock', sd['name'],
  #    sd['sector'], 'USD', now, now) )
  print symbolslist
  return symbolslist

if __name__ == "__main__":
  symbols = obtain_parse_wiki_snp500()