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
    qdate = None
    sdate = None
    edate = None
    status = None
    j = None
    r.append(['VM Name', 'Backup Time', 'Queued', 'Started', 'Ended', 'Status'])
    for file in archive_logs:
        for line in open(file):
            if line.startswith('vmname'):
                vmname = line.split('=')[1].strip()
            if line.startswith('timestamp'):
                t = line.split('=')[1].strip()
                timestamp = datetime.fromtimestamp(int(t)).strftime('%c')
            if line.startswith('qdate'):
                q = line.split('=')[1].strip()
                qdate = datetime.fromtimestamp(int(q)).strftime('%c')
            if line.startswith('sdate'):
                s = line.split('=')[1].strip()
                sdate = datetime.fromtimestamp(int(s)).strftime('%c')
            if line.startswith('edate'):
                e = line.split('=')[1].strip()
                edate = datetime.fromtimestamp(int(e)).strftime('%c')
            if line.startswith('status'):
                status = line.split('=')[1].strip()
            j = [vmname, timestamp, qdate, sdate, edate, status]
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
    message.Html = body
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
        default='Archive VBA Report On %s' %(host))

    parser.add_argument('-a', '--reportsage',
        help='Age in days before now of archive logs to report on.',
        default=1)

    parser.add_argument('-d', '--reportdir',
        help='Location of archive history files',
        default='/dd/archive_history')

    """Create variables from argparse."""
    args = parser.parse_args()

    now = time.time()
    age = now - 60*60*24*int(args.reportsage)
    
    try:
        archive_logs = return_archive_logs(args.reportdir, age)
        report = report_gen(archive_logs)
        body = ''.join(html_table(report))
        relay_email(args.smtpserver, args.smtprecipient, args.smtpsender, args.smtpsubject, body)
    except Exception as e:
        try:
            raise
        finally:
            return 1


if __name__ == '__main__':
    sys.exit(main())
