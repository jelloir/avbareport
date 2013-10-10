avbareport
==========

PHD Virtual Archive VBA Email Report Generator.

Generates an HTML email report of a PHD Virtual Archive VBA report history.

Provides:

* VM Name
* Backup Time
* Queued
* Started
* Ended
* Status

Prerequisites
-------------

The python mailer module:

Can be installed on Debian based systems (i.e. VBA's) with:

    apt-get update
    apt-get install python-mailer

Usage
-----

    usage: avbareport.py [-h] [-e SMTPSENDER] [-r SMTPRECIPIENT] [-t SMTPSERVER]
                         [-s SMTPSUBJECT] [-a REPORTSAGE] [-d REPORTDIR]
    
    optional arguments:
      -h, --help            show this help message and exit
      -e SMTPSENDER, --smtpsender SMTPSENDER
                            Sender email address (default:
                            root@nfsserver.example.local)
      -r SMTPRECIPIENT, --smtprecipient SMTPRECIPIENT
                            Recipient email address, separate multiple recipients
                            with a comma (default: root)
      -t SMTPSERVER, --smtpserver SMTPSERVER
                            SMTP server address (default: localhost)
      -s SMTPSUBJECT, --smtpsubject SMTPSUBJECT
                            Email Subject (default: Archive VBA Report On
                            nfsserver.example.local)
      -a REPORTSAGE, --reportsage REPORTSAGE
                            Age in days before now of archive logs to report on.
                            (default: 1)
      -d REPORTDIR, --reportdir REPORTDIR
                            Location of archive history files (default:
                            /dd/archive_history)
