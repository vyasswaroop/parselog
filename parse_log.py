import re
import sys
import itertools
import numpy
from datetime import datetime


def matchDate(line):
    matchThis = ""
    matched = re.match(r'\d\d\d\d/\d\d/\d\d\ \d\d:\d\d:\d\d',line)
    if matched:
        matchThis = matched.group()
    else:
        matchThis = "NONE"
    return matchThis

def generateDicts(logfile):
    currentDict = {}
    for line in logfile:
        if line.startswith(matchDate(line)):
            if currentDict:
                yield currentDict
            currentDict = {
                "date": datetime.strptime(" ".join(line.split(" ")[:2]), "%Y/%m/%d %H:%M:%S"),
                "type": line.split(" ")[-2].strip("[]"),
                "duration": line.split(" ")[-5].strip("[]ms"),
                "url": line.split(" ")[-1],
                "text": ""
            }
        else:
            currentDict["text"] += line
    yield currentDict

def parsLogFile(logfile, fromDate, toDate):
    successList = []
    errorList = []
    with open(logfile) as logfile:
        logList= generateDicts(logfile)
        for log in logList:
            if log["date"] >= fromDate and log["date"] <= toDate:
                if log["type"] == "ERROR":
                    errorList.append(log)
                else:
                    successList.append(log)
    return (errorList, successList)


if __name__=='__main__':
    if len(sys.argv) > 1:
        logfile = sys.argv[1]
    else:
        logfile = 'logfile.log'
    print("Enter the Time Period")
    inputFromDate = input("From Time: ")
    fromDate = datetime.strptime(inputFromDate, "%Y/%m/%d %H:%M:%S")
    inputToDate = input("To Time: ")
    toDate = datetime.strptime(inputToDate, "%Y/%m/%d %H:%M:%S")
    (errorList, successList) = parsLogFile(logfile, fromDate, toDate)
    print("Error counts per minute")
    for date, group in itertools.groupby(errorList, key=lambda x:x['date'].strftime("%Y/%m/%d %H:%M")):
        print("{0} - {1}".format(date, len(list(group))))
    durationList = [int(log["duration"]) for log in successList]
    print("Response time stats for successfull hits")
    print("50 percentile - {}".format(numpy.percentile(durationList, 50)))
    print("90 percentile - {}".format(numpy.percentile(durationList, 90)))
    print("95 percentile - {}".format(numpy.percentile(durationList, 95)))
