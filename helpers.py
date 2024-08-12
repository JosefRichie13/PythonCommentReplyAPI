import shortuuid
import html
import re
import time

# Generates a UUID, which is used as an ID for all comments and replies
def generateID():
    return shortuuid.uuid()


# Sanitizes the string to avoid XSS vulnerabilities
# Also removes any double spaces in between the strings
def sanitizeString(inputString):
    santizedString = html.escape(inputString)
    santizedString = re.sub(' +', ' ', santizedString)
    return santizedString


# Generates the current time in Epoch
def currentEpochTime():
    return int(time.time())
