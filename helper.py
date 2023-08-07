import requests
from bs4 import BeautifulSoup
import re


def spotcheck(level, sess, subject, cournum, classnum):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'level': level,
        'sess': sess,
        'subject': subject,
        'cournum': cournum,
    }

    response = requests.post('https://classes.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl', headers=headers, data=data, verify=False)

    if response != None:
        html = "" + response.text

        soup = BeautifulSoup(html, 'html.parser')

        datalist = []

        for data in soup.find_all('td'):
            if data.string is not None:
                t = re.sub('[^0-9a-zA-Z]+', '', data.string)
                if t != '':
                    datalist.append(t)

        wanti = datalist.index(classnum)
        if datalist[wanti + 7] < datalist[wanti + 6]:
            return True, "There is an open spot for " + subject + " " + cournum + " (" + classnum + ")"
        return False, ""
    return False, ""
