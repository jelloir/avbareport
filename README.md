avbareport
==========

PHD Virtual Archive VBA Email Report Generator

Usage
-----

    usage: avbareport.py [-h] [-e SMTPSENDER] [-r SMTPRECIPIENT] [-t SMTPSERVER]
                         [-s SMTPSUBJECT] [-a REPORTSAGE] [-d REPORTDIR]
    
    optional arguments:
      -h, --help            show this help message and exit
      -e SMTPSENDER, --smtpsender SMTPSENDER
                            Sender email address (default: root@phdvb)
      -r SMTPRECIPIENT, --smtprecipient SMTPRECIPIENT
                            Recipient email address (default: root)
      -t SMTPSERVER, --smtpserver SMTPSERVER
                            SMTP server address (default: localhost)
      -s SMTPSUBJECT, --smtpsubject SMTPSUBJECT
                            Email Subject (default: Archive VBA Report On phdvb)
      -a REPORTSAGE, --reportsage REPORTSAGE
                            Age in days before now of archive logs to report on.
                            (default: 1)
      -d REPORTDIR, --reportdir REPORTDIR
                            Location of archive history files (default:
                            /dd/archive_history)

