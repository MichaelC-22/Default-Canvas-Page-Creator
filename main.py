import csv
import canvas
import os
# clears the terminal
os.system("clear")
# welcomes the user to the program and tells them what the program does
print("Welcome to the canvas home page creator.\n")
print("This program will have you enter some information about the canvas course then it will create a home page.\n")
print("It will then upload the home page and the related images to the canvas course.\n\n")
# checks if the canvasInfo.txt file is found
if(os.path.exists("canvasInfo.txt") == False):
    # runs until the user enters the canvas API key
    while(True):
        #ask the user for the API key
        CANVAS_API = input("\nPlease enter the API key for canvas: ")
        # checks to make sure the user's input is not blank
        if(CANVAS_API != ""):
            # stops the loop
            break
        # runs if the user's input is blank
        else:
            # tells the user to enter the canvas API key
            print("\n\nPlease make sure you entered something.\n\n")
    # runs until the user enters the the Canvas url        
    while(True):
        CANVAS_URL = input("\nPlease enter the Canvas URL for your institution: ")
        if(CANVAS_URL != ""):
            break
        else:
            print("\n\nPlease make sure you entered something.\n\n")
    # creates the canvasInfo file
    canvasFile = open("canvasInfo.txt", "x")
    # writes the API key to the file
    canvasFile.write(CANVAS_API + "\n")
    # writes the url to the file
    canvasFile.write(CANVAS_URL)
    # closes the file
    canvasFile.close()
# runs the canvas create homepage section
while(True):
    # asks the user if they want to change the homepage on multiple canvas pages
     user = input("\nDo you want to change the homepage on multiple Canvas pages? ")
     # converts the user's input to lower case
     user = user.lower()
     # checks if the user's input is yes
     if(user == "yes" or user == "y"):
         # tells the user that they need to create a csv file and what to include in it
         print("\nTo modify multiple courses please make a csv file with the first column containing the courseIDs and the second column containing the section numbers.")
         print("\nexample: ")
         print("""
               courseID | section number
                 1234   |   01
               """)
        # runs until the user enters the path to the newly creates csv file
         while(True):
            # asks the for the path to the csv file
            courseCSV = input("\nPlease enter the path to the csv file: ")
            # checks if the user's input is blank
            if(courseCSV != ""):
                # stops the loop
                break
            # runs if the user's input is blank
            else:
                print("\n\nPlease make sure you entered something\n\n")
        # tells the user to export the section export from (blank)
         print("\nNow please export the section export in (blank)")
         # runs until the user enters the path to the csv file from (blank)
         while(True):
             (blank)File = input("\nPlease enter the path csv file from (blank):")
             # checks if the user's input is not blank
             if((blank)File != ""):
                # stops the loop
                break
             # runs if the user's input is blank
             else:
                print("\n\nPlease make sure you entered something.\n\n")
         # creates a canvas class object named can
         can = canvas.canvas((blank)File, "", "")
         # reads the information from the canvasInfo.txt file
         can.readInfoFromCanvasFile()
         # gets the canvas admin account 
         can.getAdminAccount()
         # gets a report of all the courses canvas has
         can.getCourseReport()
         # opens the user's csv file as courses
         with open (courseCSV, newline="") as courses:
             # reads the csv file
             courses = csv.reader(courses)
             # goes through every row in the csv file
             for row in courses:
                try:
                    # checks if both items can be converted to ints
                    if(int(row[0]) >= 0 and int(row[1]) >=0):
                        # checks if the item in the second colunm is less then 9 and does not have a 0
                        if(int(row[1]) <= 9 and row[1].find("0") == -1):
                            # adds a zero to the item which helps with identifying the course
                            row[1] = "0" + str(row[1])
                        # sets the course SISID to the item in the first column
                        can.setCourseSISID(row[0])
                        # sets the section number to the item in the second column
                        can.setSecotionNum(row[1])
                        # matches the courses between the (blank) file and the canvas report
                        worked = can.matchCourses()
                        if(worked):
                            # creates the homepage
                            can.makeHomePage()
                            # uploads the home page
                            can.uploadCanvasPage()
                            # uploads the images the home page uses
                            can.uploadImages()
                            # changes two specific settings in the course
                            can.changeSettings()
                            # logs the values of the all variables for the can class
                            can.logEveryThing()
                        else:
                            can.logEveryThing()
                            pass
                    # runs if the items are less then zero
                    else:
                      pass  
                # runs if the items cant be converted to ints
                except ValueError:
                    pass
             # removes the  file
             os.remove("")
             # removes the HomePage.html file
             os.remove("HomePage.html")
             # stops the loop
             break
     # checks if the user said no    
     elif(user == "no" or user =="n"):
         # runs until the user enters the courseID from (blank) of the course they want to upload a home page to
         while(True):
             courseID = input("\nPlease enter the courseID from (blank) for the course you want to upload a home page to: ")
             # checks if the user's input is not blank
             if(courseID != ""):
                 # breaks the loop
                break
             # runs if the user's input is blank
             else:
                print("\nPlease make sure you enter something.")
        # runs until the user enters the section number of the course they want to upload a home page to
         while(True):
             # ask the user for the section number from (blank)
             sectionNumber = input("\nPlease enter the section number from (blank) for the course you want to upload a home page to: ")
             # checks if the user's input is not blank
             if(sectionNumber != ""):
                 try:
                    # converts the user's input to an int and checks if it is less then 9
                     if(int(sectionNumber) <= 9 and sectionNumber.find("0") == -1):
                         # adds a zero to the section number
                        sectionNumber = "0" + sectionNumber
                        # stops the loop
                        break
                # runs if the user's input could not be converted to an int
                 except ValueError:
                     pass
            # tells the user to 
             else:
                print("\n\nPlease make sure you enter a number.\n\n")
         # runs until the user enters the path to the (blank) csv file
         while(True):
             # ask the user for the (blank) csv file
             (blank)File = input("Please enter the path csv file from (blank):")
             # checks if the user's input is blank
             if((blank)File != ""):
                 # stops the loop
                break
            # runs if the user's input is blank
             else:
                print("\n\nPlease make sure you entered something.\n\n")
         # creates a canvas class object called can 
         can = canvas.canvas((blank)File, courseID, sectionNumber)
         # reads the canvasInfo.txt file
         can.readInfoFromCanvasFile()
         # gets the canvas admin account
         can.getAdminAccount()
         # gets a report containing all course canvas has
         can.getCourseReport()
         # matches the courses between the (blank) file and the canvas report
         can.matchCourses()
         # creates the homepage
         can.makeHomePage()
         # uploads the home page
         can.uploadCanvasPage()
         # uploads the images the home page uses
         can.uploadImages()
         # changes two specific settings in the course
         can.changeSettings()
         # logs the values of the all variables for the can class
         can.logEveryThing()
         # removes the  file
         os.remove("")
         # removes the HomePage.html file
         os.remove("HomePage.html")
         # stops the loop
         break
