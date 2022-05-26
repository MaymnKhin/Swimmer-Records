from Swimmer import Swimmer
import pandas as pd
from datetime import date
import csv

# display menu
def menu():
    print("\nMenu -")
    print("1. Register swimmer") 
    print("2. Remove swimmer") 
    print("3. Record swimmers' timings") 
    print("4. Enquire swimmers' timings") 
    print("5. Display swimmers' timings for submission (on screen)")
    print("6. Get Swimmers from File")
    print("7. Save Registered Swimmers to new File(No Record):")
    print("8. Save Swimmers Records and Infomation to new File")
    print("9. End Program")

# check if swimmer already exist in people{}
def hasRegistered(name):
    registered = False
    if name in people:
        registered = True
    return registered

# get event from user and check if it is valid
def getValidEvent():

    validEvents = {"freestyle" : [50, 100, 200, 400, 800, 1500], "backstroke" : [50, 100, 200],
    "breaststroke" : [50, 100, 200], "butterfly": [50, 100, 200], "individual medley" : [100, 200, 400] }

    while True:
        try:
            event = input("Enter the type of event with its distance (eg.freestyle 50):").lower()
            style, distance = event.rsplit(" ",1)
                
            if style in validEvents:
                if int(distance) in validEvents.get(style):
                    break
            print("The Event is invalid. Try another one.")
        except:
            print("Invalid Input. Try Again.")
    return event


def registerSwimmer(swimmerName):
    # check if swimmer exists 
    if swimmerName in people:
        if people[swimmerName].getStatus() == "inactive": # check the status of swimmer object
            people[swimmerName].setStatus("active")
            print("Swimmer's status has changed to 'active'")
        else:
            print("The user is already active")
    
    else:
        # get gender from user
        while True:
            genderInput = input("Choose gender (Enter F or M):").upper()
            if genderInput == "F":
                gender = "female"
                break
            elif genderInput == "M":
                gender = "male"
                break
            else:
                print("Invalid Input. Try again.")

        # get date of birth from user
        while True:
            dateOfBirth = input("Enter the date of birth in following format, YYYY-MM-DD : ")
            try:
                year, month, day = dateOfBirth.split("-")
                year = int(year)
                month = int(month)
                day = int(day)

                if (month > 0 and month <= 12) and (day > 0 and day < 32): # check valid months and days
                    currentDate = date.today() 
                    age = currentDate.year - int(year)
                    if age <= 0 or age > 100:             # check if age is possible
                        print("Invalid Input. Try again")
                        continue
                    elif currentDate.month < month:
                        age -= 1
                    elif currentDate.month == month and currentDate.day < day: 
                        age -= 1
                    break
                else:
                    print("Invalid Input.Try again")

            except ValueError:
                print("Invalid Input.Try again")
    
        newSwimmer = Swimmer(swimmerName, gender, age, "active")
        people[newSwimmer.getName()] = newSwimmer
        print("Registeration Successful!")
        

def selectFeature():
    while True:
        menu()
        try:
            action = int(input("Enter the number of feature to process: "))
        except ValueError:
            print("Invalid Input. Please try again.")
            continue
        if action > 9 or action < 1:
            print("Invalid Input, Please try again.")
            continue
        else:
            break
    return action

people = {}         # store swimmer objects with their name as key and object as value

moreAction = True

# repeatedly perform the features
while moreAction:
    feature = selectFeature()

    # repeatedly register the swimmer 
    if feature == 1:
        registerMore = "yes"
        while registerMore == "yes":
            name = input("Type swimmer's name: ")
            registerSwimmer(name)
            while  True:
                registerMore = input("Continue to register? (Enter yes or no):")
                if registerMore == "yes" or registerMore == "no":
                    break

    # Change specified active swimmer to inactive
    elif feature == 2:
        nameRM = input("Enter name to remove:")
        if nameRM in people:
            if people[nameRM].getStatus() == "active":
                people[nameRM].setStatus("inactive")
                print("Swimmer's status has changed to 'inactive'.")
            else:
                print("Swimmer is already inactive.")
        else:
            print(nameRM, "can't be found")
        
    # Record the timing of swimmers
    elif feature == 3:
        nameRec = input("Enter Swimmer's name: ")
        registered = False

        # Register swimmer if swimmer doesn't exist in people {}
        if not nameRec in people:
            print("\nThe swimmer has not been registered yet.")
            decision = ""
            while True:
                decision = input("Register the swimmer? (Enter yes or no) :").lower()

                if decision == "yes":   # register
                    registerSwimmer(nameRec)
                    print("Proceed to record timing.")
                    registered = True
                    break
                elif decision == "no":   #not register
                    registered = False
                    break
        
        # get respective information if registered
        if nameRec in people or registered:
            
            event = getValidEvent()
            
            timing = input("Enter the timing (min:sec) : ")

            meet = input("Where is the record achieved: ")
            
            people[nameRec].addRecord(event, timing, meet,"unposted")
            print("\nTiming for", nameRec, "has been successfully recorded.\n")
        
        else:
            print("\nUnable to record the timing of unregistered swimmer.\n")

    # Display Filtered Timings
    elif feature == 4:
        print("1. Enquire Swimmers' timings by name")
        print("2. Enquire Swimmers' timing by name and event")
        
        # Input validation
        while True:
            try:
                enquiry = int(input("Choose the filtered option (Enter 1 or 2): "))
                if enquiry == 1 or enquiry == 2:
                    break
                else:
                    print("Invalid Input. Please try again.")
        
            except ValueError:
                print("Invalid Input. Please try again.")

        names = []                  # Store multiple names to filter
        addMoreName = "yes"
        while addMoreName == "yes":
            name = input("Enter the name of swimmer: ")
            if hasRegistered(name) and (not name in names) :
                names.append(name)
            elif name in names:
                print("Already typed the swimmer name")
            else:
                print("There's no swimmer named", name)

            addMoreName = input("Would you like to add another name? (Enter yes or no) : ").lower()
        
        if enquiry == 2:
            events = []             # Store multiple events to filter
            addMoreEvent = "yes"
            while addMoreEvent == "yes":
                event = getValidEvent()
                if not event in events:
                    events.append(event)
                addMoreEvent = input("Would you like to add another event? (Enter yes or no): ").lower()
            
        filtered_Records = {"Name" : [], "Event" :[], "Time" :[], "Meet":[]}
        for swimmer in names:                                           # Get all records of a swimmer
            if enquiry == 1:
                swimmerRec = people.get(swimmer).getAllTimingRec()
                
            else: 
                # Get records of each respective events of a swimmer
                swimmerRec = {"Event" : [], "Time" : [], "Meet" : []}
                for event in events:                                     
                    individual_EventRec = people.get(swimmer).getFilteredTiming(event)
                    for key in swimmerRec.keys():
                        swimmerRec.get(key).extend(individual_EventRec.get(key)) 

            # Put the recoreds in filtered_Records Dictionary to combine with other swimmers that is specified    
            total_events = len(swimmerRec.get("Event"))
            nameList = [swimmer] * total_events     # create a list of a swimmer name 
            filtered_Records.get("Name").extend(nameList)
            filtered_Records.get("Event").extend(swimmerRec.get("Event"))
            filtered_Records.get("Time").extend(swimmerRec.get("Time"))
            filtered_Records.get("Meet").extend(swimmerRec.get("Meet"))

        # Change filtered_Records into a dataframe
        filtered_data = pd.DataFrame(filtered_Records)
        if filtered_data.empty:
            print("No record found")
        else:
            filtered_data.index = filtered_data.index + 1
            print(filtered_data)  

    # Find unposted record of each active swimmer in people{} and post timings
    elif feature == 5:
        active_unpostedRec = {"Name" : [], "Gender" :[], "Event" :[], "Time" :[], "Meet":[], "Age":[]}
        unpostedRec_position = {}
        
        for swimmer in people.keys():
            unpostedRec_position[swimmer] = []
            swimmerInfo = people[swimmer] # Get Swimmer object
            if swimmerInfo.getStatus() == "active":
                swimmerRec = swimmerInfo.getRecord()
                rec_statusList = swimmerRec.get("RecStatus")
                # Get record of unposted timings
                for index in range(len(rec_statusList)):
                    if rec_statusList[index] == "unposted":
                        unpostedRec_position[swimmer].append(index)   # Store the index of unposted records  of a swimmer to change them later
                        active_unpostedRec.get("Name").append(swimmer)
                        active_unpostedRec.get("Gender").append(swimmerInfo.getGender())
                        active_unpostedRec.get("Age").append(swimmerInfo.getAge())
                        active_unpostedRec.get("Event").append(swimmerRec["Event"][index])
                        active_unpostedRec.get("Time").append(swimmerRec["Time"][index])
                        active_unpostedRec.get("Meet").append(swimmerRec["Meet"][index])
                    
        
        active_unpostedData = pd.DataFrame(active_unpostedRec)
        if active_unpostedData.empty:
            print("All swinners' timings have been posted")
        else:
            active_unpostedData.index = active_unpostedData.index + 1 # shift the index
            print(active_unpostedData)
            # Change the timing records to posted if user agrees
            while True:
                posted = input("Update these timings to Posted? (Enter yes or no):").lower()                
                if posted == "yes":
                    for name, unposted_RecIndex in unpostedRec_position.items():
                        swimmerRec = people[name].getRecord()
                        for index in unposted_RecIndex:
                            swimmerRec.get("RecStatus")[index] = "posted"
                    print("Swimmers' records have been posted")
                    break
                elif posted == "no":
                    print("Unable to post swimmers' records")
                    break
        
    elif feature == 6:                                   #Load swimmer information from file
        file = open("swimmerRecords.csv", mode = "r")
        swimmersFile = csv.DictReader(file)
        for line in swimmersFile:
            name = line.get("Name")

            if name in people:
                people.get(name).addRecord(line.get("Event"), line.get("Time"), line.get("Meet"), line.get("Rec_Status"))
            else:
                newSwimmer = Swimmer(line.get("Name"), line.get("Gender"), line.get("Age"), line.get("Status"))
                newSwimmer.addRecord(line.get("Event"), line.get("Time"), line.get("Meet"), line.get("Rec_Status"))
                people[name] = newSwimmer
        file.close()
        print("Reading Data from File Successful!")

    # Save swimmer information to file
    elif feature == 7:
        outfile = open("newRegisteredSwimmer.csv", mode = "w")
        for swimmer in people.values():
            outfile.write(swimmer.getSwimmerInfo())
        outfile.close()
        print("Successful!Data saved to a file.")

    # Save swimmer information to file with all the records
    elif feature == 8:
        columnHeader = ["Name", "Gender", "Event", "Time", "Meet", "Age", "Status", "Rec_Status"]
        swimmerOutput = {"Name" : [], "Gender" : [], "Event": [], "Time": [], "Meet": [], "Age": [], "Status": [], "Rec_Status" : []}
        for swimmer in people:
            swimmerObj = people[swimmer]
            record = swimmerObj.getRecord()
            totalEvent = len(record.get("Event"))
            for index in range(totalEvent):                                   # Put the respective information into the dictionary
                swimmerOutput["Name"].append(swimmerObj.getName())
                swimmerOutput["Gender"].append(swimmerObj.getGender())
                swimmerOutput["Event"].append(record.get("Event")[index])
                swimmerOutput["Time"].append(record.get("Time")[index])
                swimmerOutput["Meet"].append(record.get("Meet")[index])
                swimmerOutput["Rec_Status"].append(record.get("RecStatus")[index])
                swimmerOutput["Status"].append(swimmerObj.getStatus())
                swimmerOutput["Age"].append(swimmerObj.getAge())

        dataOutput = pd.DataFrame(swimmerOutput)
        dataOutput.to_csv("swimmerRecords.csv", sep=',', index = False)
        print("Successful!Data saved to a file.")


    else:
        moreAction = False
        print("\nProgram End.")
    


        
        

    
    
