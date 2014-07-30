#!/usr/bin/python

import sys, os, string, molecular, cgi

cgiurl = "/cgi-bin/mnames.cgi"

def styleme():
    print "<style>"
    print "body, table    { font-family: verdana, arial, helvetica;"
    print "                 font-size: 12px; }"
    print "a:link         { text-decoration: none; color: black; }"
    print "a:visited      { text-decoration: none; color: black; }"
    print "a:hover        { text-decoration: none; color: blue; }"
    print "a:active       { text-decoration: none; color: blue; }"
    print "</style>"

try:
    query = os.environ["QUERY_STRING"]
except:
    query = ""

directory = {}
names = []

fp = open(molecular.NAMEDIR + "/.directory", "r")

for line in fp.readlines():
    lst = string.split(line)
    names.append(lst[0])
    directory[lst[0]] = string.join(lst[1:], " ")

fp.close()
    
if query == "":
    print "Content-type: text/html\n"
    print "<html>\n<head>\n<title>Name Files</title>"
    styleme()
    print "</head>\n"
    print "<body bgcolor=white>"
    print "<h1>Molecular Name Generator</h1>"

    print "<form method=get action='%s'>" % cgiurl
    print "<p>\n<input type=submit value='Go!'>"
    print "<input type=reset value='Clear'>\n<p>"

    for name in names:
        print "&nbsp;<input type=checkbox name=query value='%s'>" % name
        print directory[name] + "<br>"

    print "<p>\n<input type=submit value='Go!'>"
    print "<input type=reset value='Clear'>\n<p>"
    print "</form>\n\n</body>\n</html>"

else:

    form = cgi.FieldStorage()
    query = form["query"]

    if type(query) is type([]):
        query = map(lambda x: x.value, query)
    else:
        query = [ query.value ]

    print "Content-type: text/html\n"

    print "<html>\n<head>\n<title>Molecular Name Generator</title>"
    styleme()
    print "</head>\n"
    print "<body bgcolor=white>"
    print "<font face='verdana,arial,helvetica'>"
    print "<h1>Molecular Name Generator</h1>"
    print "</ul><p>"
    print "<li><a href='%s'>" % cgiurl
    print "<b>Back to Molecular Name Generator</b></a>"
    qstr = string.join(map(lambda x: "query=" + x, query), "&")
    print "<li><a href='%s?%s'>" % (cgiurl, qstr)
    print "<b>Re-Run this list</b></a>"
    print "</ul><p>"
    for q in query:
        print directory[q] + "<br>"
    print "<p>\n<table cellspacing=0 border=1 width=500>"

    col = 1

    name = molecular.Molecule()

    for q in query:
        name.load(q)

    for i in range(32):

        line = name.name()

        if col == 1:
            print "<tr>"

        print "<td width=25%>" + line + "</td>"

        col = col + 1

        if col > 4:
            print "</tr>"
            col = 1

    print "</table>\n<p>"
    print "<p>"
    for i in name.nametbl["notes"]:
        print i, "<br>"
    print "<p>"
    print "Molecular Copyright &copy; 2000 Chris Gonnerman<br>"
    print "\n</font>\n</body>\n</html>"

