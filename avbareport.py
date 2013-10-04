#!/usr/bin/env python

import os
import sys
import time
import platform
import getpass
import argparse
from mailer import Mailer
from mailer import Message
from datetime import datetime


def return_archive_logs(reportdir, age):
    p = [ os.path.join(reportdir,''.join(q)) for q in os.listdir(reportdir) ]
    return [ f for f in p if os.path.getctime(f) > age ]


def report_gen(archive_logs):
    r = []
    vmname = None
    timestamp = None
    date = None
    status = None
    j = None
    r.append(['vmname', 'date', 'status'])
    for file in archive_logs:
        for line in open(file):
            if line.startswith('vmname'):
                vmname = line.split('=')[1].strip()
            if line.startswith('timestamp'):
                timestamp = line.split('=')[1].strip()
                date = datetime.fromtimestamp(int(timestamp)).strftime('%c')
            if line.startswith('status'):
                status = line.split('=')[1].strip()
            j = [vmname, date, status]
        r.append(j)
    return r


def html_table(logfiles):
      yield '<table border="1">'
      for sublist in logfiles:
            yield '<tr><td>'
            yield '</td><td>'.join(sublist)
            yield '</td></tr>'
      yield '</table>'

def relay_email(smtpserver, smtprecipient, smtpsender, smtpsubject, body):
    message = Message(From=smtpsender, To=smtprecipient, Subject=smtpsubject)
    message.Body = body
    sender = Mailer(smtpserver)
    sender.send(message)

def main():

    """Setup argparse."""
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    whoatnode = getpass.getuser() + '@' + platform.node()
    parser.add_argument('-e', '--smtpsender',
        help='Sender email address',
        default=whoatnode)

    who = getpass.getuser()
    parser.add_argument('-r', '--smtprecipient',
        help='Recipient email address',
        default=who)

    parser.add_argument('-t', '--smtpserver',
        help='SMTP server address',
        default='localhost')

    host = platform.node()
    parser.add_argument('-s', '--smtpsubject',
        help='Email Subject',
        default='avbareport on %s' %(host))

    parser.add_argument('-a', '--reportsage',
        help='Time in past from now to use logs files',
        default=1)

    parser.add_argument('-d', '--reportdir',
        help='Location of archive history files',
        default='/mnt/backup/VBABACKUPS/archive_history')

    """Create variables from argparse."""
    args = parser.parse_args()

    now = time.time()
    age = now - 60*60*24*int(reportsage)
    
    try:
        archive_logs = return_archive_logs(reportdir, age)
        report = report_gen(archive_logs)
        body = ''.join(html_table(report))
        relay_email(smtpserver, smtprecipient, smtpsender, smtpsubject, body)
    except Exception as e:
       return 1 

if __name__ == '__main__':
    sys.exit(main())
