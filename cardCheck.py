#!/usr/bin/python

import time
import sys
import os
import re

class credit_valid ():
      def __init__ (self):
	  self.ccnum = ''
	  self.cc_file = 'cardinfo.csv'
	  self.reject_counter = 0
	  self.industry = ''
	  self.issuer = ''
	  self.acctno = ''
	  self.validity = ''	

      def request_details (self):
	  if (self.reject_counter < 3):
	     try:
	        self.ccnum = input ("Enter card number: ")
	     except:
		os.system ("clear")
		if (self.reject_counter < 2):
	           print ("reenter card details")
	        self.reject_counter = self.reject_counter + 1
		self.request_details ()
	     self.ccnum = str (self.ccnum)
	     self.file_chk ()
	     self.perf_checks ()
	  else:
	     self.locking_mech ()

      def locking_mech (self): 
	  os.system ("clear")
	  print ("Credit Valid program is locked for 30 sec") 
	  for x in range (30, 0, -1): 
	      msg = ("will unlock in %s sec " % (x))
	      print (msg)
	      sys.stdout.write ("\033[F")
	      time.sleep (1)
	  self.reject_counter = 0
	  os.system ("clear")
	  self.request_details ()

      def load_checkinfo (self): 
          self.MII_info = {"1": "Airlines",
		           "2": "Airlines",
		      	   "3": "Travel",
		      	   "4": "Banking and Financial",
		      	   "5": "Banking and Financial",
		      	   "6": "Merchandising and Banking/Financial",
		       	   "7": "Petroleum",
		     	   "8": "Healthcare, Telecommunications",
		      	   "9": "National Assignment"}
	  self.BIN_info = {"34": {"15": "Amex"},
		      	   "37": {"15": "Amex"},
			   "4": {"13": "Visa", "16": "Visa"},
			   "51": {"16": "MasterCard"},
                           "55": {"16": "MasterCard"},
			   "6011": {"16": "Discover"},
			   "644": {"16": "Discover"},
			   "65": {"16": "Discover"}}
		      
      def perf_checks (self):
	  self.load_checkinfo ()
	  ccnum_len = len (self.ccnum)
	  if ((ccnum_len < 13) or (ccnum_len > 16)):
	     self.card_validity (False)
	  indtemp = self.ccnum [0:1]
	  if (indtemp not in self.MII_info.keys ()): 
	     self.card_validity (False)
	  else:
	     self.industry = self.MII_info [indtemp]
	  ccnum_len = str (ccnum_len)
	  for x in range (1, 5):
	      isstemp = self.ccnum [0:x]
	      if (isstemp in self.BIN_info.keys ()):
                 if (ccnum_len in self.BIN_info [isstemp].keys ()):
		    self.issuer = self.BIN_info [isstemp][ccnum_len]
	  if (self.issuer == ''):
	     self.card_validity (False)
	  self.acctno = self.ccnum [6:-1]
	  rev_ccnum = self.ccnum [::-1]
	  count = 1
	  result = 0
	  for i in rev_ccnum:
	      if (count % 2 != 0):
		 val = int (i) * 1
		 result = result + val
		 count += 1
	      else:
		 val = int (i) * 2
		 if (val > 10):
		    val = sum (map (int, str (val)))   
		 result = result + val
		 count += 1
	  if (result % 10 != 0):
	     self.card_validity (False)
	  self.card_validity (True) 

      def card_validity (self, valid_chk):
	  if (valid_chk):
	     self.validity = 'valid'
 	     with open (self.cc_file, 'a') as fa:
	          fa.write ("%s,%s,%s,%s,%s\n" % (self.ccnum, self.industry, self.issuer, self.acctno, self.validity))
	     print ("The system found the following information")
	     self.print_out ()
	  else:
	     print ("Provided card details are invalid")
	     exit ()

      def file_chk (self):
	  if (not os.path.isfile (self.cc_file)):
	     return ()
	  with open (self.cc_file, 'r') as fl:
	       for x in fl:
		   x = x.strip ()
		   if (re.search (self.ccnum, x)):
		      strarr = x.split (',')
		      self.industry = strarr [1]
		      self.issuer = strarr [2]
		      self.acctno = strarr [3]
		      self.validity = strarr [4]
	              print ("Card information accessed recently. Retrieving from stored data")
		      self.print_out ()

      def print_out (self):
	  print ("Industry: %s" % (self.industry)) 
	  print ("Issuer/brand: %s" % (self.issuer)) 
	  print ("user account: %s" % (self.acctno)) 
	  print ("card validity: %s" % (self.validity)) 
	  exit ()

      def run (self):
	  self.request_details ()

if (__name__ == '__main__'):
   obj = credit_valid ()
   obj.run ()
