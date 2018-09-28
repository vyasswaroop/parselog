# Parse Log

A simple python script to parse a log file and for a given time period:
#. gives errors per minute
#. gives 50, 90, 95 percentile of the successful response time

Requires python3

Approach
========
#. Read the log file and get list of error and success log within the particular time period separately.
#. Group the error log per minute and print the count
#. Separate out the response time from success log list and take percentile


Run time performance
====================
#. Made use of generators to read line by line of logfile so that whole logfile wont be loaded at one go
#. If the file is too large it will take more time to process.

Improvement
===========
#. Since the logfile comes with sorted timestamp, the reading of logfile could be stopped after the time period specified ends.
#. Error and Exception handling
