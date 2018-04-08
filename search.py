#!/usr/bin/env python

import pypff
import sys

from email.utils import parseaddr


if len(sys.argv) != 3:
    print "Need to have 2 arguments: <pst file> <search term>"
    sys.exit(1)

pst_file = sys.argv[1]
search_term = sys.argv[2]

print "PST file:", pst_file
print "Search term:", search_term

pst = pypff.file()
pst.open(pst_file)

print "Size:", pst.get_size()
print

msg_counter = 0

def search_dir(d,path):
    if not d: return

    if d.get_name():
        new_path = path + u"/" + unicode(d.get_name())
    else:
        new_path = path

    print "Searching ", new_path

    for i in range(0, d.get_number_of_sub_messages()):
        msg = d.get_sub_message(i)
        try:
            #if search_term in msg.get_plain_text_body():
            #if search_term.lower() in msg.get_sender_name().lower():
            #if search_term in msg.get_plain_text_body():

            email = parseaddr("".join([l for l in msg.get_transport_headers().split() if "@" in l and ".com" in l]))[1] #FIX: this .com is a quick hack to cut down on some of the bad headers

            if search_term.lower() in email.lower():
                write_to_file(msg)

        except TypeError:
            pass

    for i in range(0, d.get_number_of_sub_folders()):
        search_dir(d.get_sub_folder(i), new_path)

def write_to_file(msg, output="screen"):
    global msg_counter

    if "screen" in output:
        print "Found: ", msg.get_subject()
        txt = msg.get_plain_text_body()
        print txt
    else:
        with open("msgs/" + str(msg_counter) + ".txt","wb") as f:
            f.write("Subject: ")
            f.write(msg.get_subject())
            f.write("\n\n")
            f.write(msg.get_plain_text_body())
            f.close()

        msg_counter = msg_counter + 1

search_dir(pst.get_root_folder(),u"")
