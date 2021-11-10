import datetime

def infoValidity(data, dates, countries, region, key):
    for i in [data, dates, countries, region, key]:
        if not i[0]:
            return [False,i[1]]
    return [True, []]

def locationQuery(location):
    if len(location) < 1:
        return [True, []]
    newLocations = []
    for i in location:
        newLocations.append(i.replace("_", " "))
    return [True, newLocations]

def dateQuery(dateStart, dateEnd, dateSpecific):
    if dateStart == [] and dateEnd == []:
        if len(dateSpecific) == 1:
            #do cleansing of dateSpecific
            cleanDates = checkDates(dateSpecific)
            if(cleanDates[0]):
                return [True, dateSpecific]
            else:
                return [False, cleanDates[1] + " is an incorrect data format, should be YYYY-MM-DD"]
        elif len(dateSpecific) == 0:
            # because no dates were specified
            return [True, []] 
        else:
            return [False, "Only 1 specific date can be queried at a time!"]
    elif dateSpecific == []:
        #this means dateStart or dateEnd both have queries and we will clean the duration
        if (len(dateStart) == 1 and len(dateEnd) == 1):
            cleanDates = checkDates([dateStart[0], dateEnd[0]])
            print(cleanDates)
            if(cleanDates[0]):
                #since dates are in iso format we can do direct comparison
                if cleanDates[1][0] < cleanDates[1][1]:
                    return [True, [dateStart[0], dateEnd[0]]]
                else:
                    return [False, "The start date needs to have occured before entered the end date"]
            else:
                return [False, cleanDates[1] + " is an incorrect data format, should be YYYY-MM-DD"]
        else:
            return [False, "Incorrect amount of dates entered for dateStart/dateEnd, Or missing date for one of those parameters!"]
    else:
        return [False, "Only 1 specific date Or 1 duration of two dates can be queried at a time!"]

def checkDates(dates):
    for i in dates:
        if not checkValidDate(i):
            return [False, i]
    return [True, dates]

def checkValidDate(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return True
    except:
        return False # "Incorrect data format, should be YYYY-MM-DD"]

def dataQuery(data):
    #get rid of repeated data queries
    data = list(set(data))
    length = len(data)
    #return null if data contains illegal queries
    legal = ['deaths', 'confirmed', 'active', 'recovered']
    illegal = []
    

    for i in range(length):
        data[i] = data[i].strip().lower()
        if data[i] not in legal:
            illegal.append(data[i])
    

    if len(illegal) > 0:
        illegalQuery = ", ".join(illegal)
        return [False, "Illegal data queries entered : "+ illegalQuery]
    elif len(data)<1:
        return [False, []]
    return [True, data]

