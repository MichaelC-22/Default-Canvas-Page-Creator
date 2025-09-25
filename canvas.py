import time
import requests
import os
import json
import csv
import logging

class canvas:
    
    logging.basicConfig(level=logging.INFO, format="{asctime} - {levelname}: {message}", style="{",datefmt="%d-%m-%Y " "%H:%M", filename="Canvas Page Creator.log", encoding="utf-8",filemode="a",)
    
    def __init__(self, csvFilePath:str, courseSISID:str, sectionNum:str):
        self.courseID = ""
        self.courseName = ""
        self.location = ""
        self.teacher = ""
        self.email = ""
        self.courseSISID = courseSISID
        self.teacherID = ""
        self.access_token = ''
        self.baseUrl = ''
        self.csvFilePath = csvFilePath
        self.adminID = ""
        self.sectionNum = sectionNum
        
    # sets the courseSISID to the entered value
    # Parameters: courseSISID:str   
    def setCourseSISID(self, courseSISID:str):
        # sets the class courseSISID to the entered courseSISID
        self.courseSISID = courseSISID
    # sets the sectionNum to the entered value
    # Parameters: sectionNum:str   
    def setSecotionNum(self, sectionNum:str):
        # sets the class sectionNum to the entered sectionNum
        self.sectionNum = sectionNum    
    # this function gets the course storage report from canvas then writes it to a csv file            
    def getCourseReport(self):
        logging.info("Running CourseReport function.")
        # URL to start running the report
        url = self.baseUrl + "/api/v1/accounts/" + str(self.adminID) + "/reports/course_storage_csv"
        # authentication and what content is expected
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
                   "Content-Type": "multipart/form-data"
                   }
        # important information to send to canvas which allows canvas to know what to send back
        data = {
                "enrollment_term_id": "",
                "skip_message": True,
                "courses": True,
                "users": False,
                "enrollments": False
        }
        # the request
        info = requests.post(url=url, headers=headers, params=data)
        # converts the request into a json
        info = info.json()
        # checks if the status is created
        if(info["status"] == "created"):
            print("Course Report created...\n")
            # creates the same url but with the report's ID
            url = self.baseUrl + "/api/v1/accounts/" + str(self.adminID) + "/reports/course_storage_csv/" + str(info["id"])
            # starts the while loop
            running = True
            dots = 1
            while(running):
                # gets the status of the report
                info = requests.get(url=url, headers=headers)
                # converts it into json
                info = info.json()
                # checks if the status is complete
                if(info["status"] == "complete"):
                    # stops the while loop
                    running = False
                else:
                    # clears the terminal
                    os.system("clear")
                    # checks if dots is 3
                    if (dots == 3):
                        # prints message with 3 dots
                        print("Retrieving course report...\n")
                        # sets dots to 1
                        dots = 1
                    # checks if the dots is 2
                    elif (dots == 2):
                        # prints message with 2 dots
                        print("Retrieving course report..\n")
                        # adds 1 dot
                        dots = dots + 1
                    # checks if dots is 1
                    elif(dots == 1):
                        # print message with 1 dot
                        print("Retrieving course report.\n")
                        # adds one dot
                        dots = dots + 1
                # waits 2 seconds
                time.sleep(2)
                # lets the user know the course is being retrieved
            print("Downloading course report...\n")
            logging.info("Downloading Course Report.")
            # creates a temporary file with the information gotten from the provided URL
            tempFile = requests.get(url=info["attachment"]["url"])
            if(tempFile.status_code != 200):
                logging.critical("Could not download course report.\n\n" + str(tempFile.text))
            # creates a file to store the information
            with open("course_report.csv", "w+") as file:
                # writes to the newly created file
                 file.writelines(tempFile.text)
            print("Course Report downloaded.\n")
            logging.info("Downloaded Course Report.")
        else:
            # lets the user know the report failed
            print("Report failed.")
    # this function reads the information from the canvasInfo.txt file
    def readInfoFromCanvasFile(self):
        logging.info("Running Read Info From Canvas File function.")
        try:
            # opens the canvasInfo.txt file
            with open("canvasInfo.txt", "r") as file:
                # reads the lines
                file = file.readlines()
                # sets the base URL of the class to the second line in the file
                self.baseUrl = file[1]
                # sets the accessToken of the class to the first line in the file
                self.access_token = file[0].strip("\n")
        # runs if the file is not found
        except FileNotFoundError:
            logging.critical("Could not find Canvas Info file.")
            print("\n\nThe file containing all canvasInfo was not found.\n\n")
    # this function makes the home page for the entered canvas course based off a template
    def makeHomePage(self):
        logging.info("Running Make Home Page function.")
        print("Making home page.\n")
        # opens the template
        template = open("templates/").readlines()
        try:
            # creates a new file called HomePage.html
            file = open("HomePage.html", "x")
        except FileExistsError:
            # opens the HomePage.html in writing mode
            file = open("HomePage.html", "w")
        # goes though every line in the template
        for x in template:
            # checks if the current line in the template contains a "{"
            while(x.find("{") > 0):
                # finds the position of the left bracket
                leftBracket = x.find("{")
                # finds the position of the right bracket
                rightBracket = x.find("}")
                # checks if the string between the left and right bracket is logo_left_url
                if (str(x[leftBracket:rightBracket+1]) == "{" + "logo_left_url}"):
                    #replaces logo_left_url with the upload url of the image
                    x = x.replace("{" + "logo_left_url}", str(canvas.getImagesUrl(self,"")))
                # checks if the string between the left and right bracket is course_name
                elif (x[leftBracket:rightBracket+1] == "{" + "course_name}"):
                    # replaces course_name with the course's name
                    x = x.replace("{" + "course_name}",self.courseName)
                # checks if the string between the left and right bracket is location
                elif (x[leftBracket:rightBracket+1] == "{" + "location}"):
                    # replaces location with the course's location
                        x = x.replace("{" + "location}",self.location)
                # checks if the string between the left and right bracket is teacher_name
                elif (x[leftBracket:rightBracket+1] == "{" + "teacher_name}"):
                    # replaces teacher_name with the teacher's name
                    x = x.replace("{" + "teacher_name}",str(self.teacher))
                # checks if the string between the left and right bracket is logo_right_url
                elif (x[leftBracket:rightBracket+1] == "{" + "logo_right_url}"):
                    #replaces logo_right_url with the upload url of the image
                    x = x.replace("{" + "logo_right_url}", str(canvas.getImagesUrl(self, "")))
                # checks if the string between the left and right bracket is teacher_email
                elif (x[leftBracket:rightBracket+1] == "{" + "teacher_email}"):
                    # replaces teacher_email with the teacher's email
                    x = x.replace("{" + "teacher_email}",self.email)
                # checks if the string between the left and right bracket is assignments_url
                elif (x[leftBracket:rightBracket+1] == "{" + "assignments_url}"):
                    # replaces assignments_url with the course's assignments url
                    x = x.replace("{" + "assignments_url}",self.baseUrl + "/courses/" + self.courseID + "/assignments")
                # checks if the string between the left and right bracket is assignments_icon
                elif (x[leftBracket:rightBracket+1] == "{" + "assignments_icon}"):
                    #replaces assignments_icon with the upload url of the image
                    x = x.replace("{" + "assignments_icon}", str(canvas.getImagesUrl(self, "clipboard.png")))
                # checks if the string between the left and right bracket is announcements_url
                elif (x[leftBracket:rightBracket+1] == "{" + "announcements_url}"):
                    # replaces announcements_url with the course's announcements url
                    x = x.replace("{" + "announcements_url}",self.baseUrl + "/courses/" + self.courseID + "/announcements")
                # checks if the string between the left and right bracket is announcements_icon
                elif (x[leftBracket:rightBracket+1] == "{" + "announcements_icon}"):
                    #replaces announcements_icon with the upload url of the image
                    x = x.replace("{" + "announcements_icon}", str(canvas.getImagesUrl(self, "megaphone.png")))
                # checks if the string between the left and right bracket is modules_url
                elif (x[leftBracket:rightBracket+1] == "{" + "modules_url}"):
                    # replaces modules_url with the course's modules url
                    x = x.replace("{" + "modules_url}", self.baseUrl + "/courses/" + self.courseID + "/modules")
                # checks if the string between the left and right bracket is modules_icon
                elif (x[leftBracket:rightBracket+1] == "{" + "modules_icon}"):
                    #replaces modules_icon with the upload url of the image
                    x = x.replace("{" + "modules_icon}", str(canvas.getImagesUrl(self, "module.png")))
                # checks if the string between the left and right bracket is syllabus_url
                elif (x[leftBracket:rightBracket+1] == "{" + "syllabus_url}"):
                    # replaces syllabus_url with the course's syllabus url
                    x = x.replace("{" + "syllabus_url}",self.baseUrl + "/courses/" + self.courseID + "/syllabus")
                # checks if the string between the left and right bracket is syllabus_icon
                elif (x[leftBracket:rightBracket+1] == "{" + "syllabus_icon}"):
                    #replaces syllabus_icon with the upload url of the image
                    x = x.replace("{" + "syllabus_icon}", str(canvas.getImagesUrl(self, "open-book.png")))
            logging.info("Writing Home Page File.")
            # writes the current line to the HomePage.html file
            file.write(x)
    # This function uploads the HomePage.html to the canvas site    
    def uploadCanvasPage(self):
        logging.info("Running Upload Canvas Page Function.")
        print("Uploading Canvas page.\n")
        # creates the url to send the request to
        url = self.baseUrl + "/api/v1/courses/" + self.courseID + "/pages"
        # creates the header file used for authentication
        header = {"Authorization": "Bearer " + self.access_token}
        # opens the HomePage.html and reads it content
        with open("HomePage.html", "r") as file:
            # reads the content of the file
            body_content = file.read()
        # creates the data that will be sent to the canvas course containing information related to the HomePage.html
        data:dict[str, str | bool] = {"wiki_page[title]": self.courseName, "wiki_page[body]": body_content, "wiki_page[editing_roles]":"teachers", "wiki_page[published]": True,
                "wiki_page[front_page]": True}
        # sends the HomePage.html to the server
        r = requests.post(url=url, headers=header, data=data)
        if(r.status_code != 200):
            logging.critical("Could not Upload Canvas Page.\n\n" + str(r.text))
    # This function uploads the images used in the HomePage.html to the canvas course        
    def uploadImages(self):
        logging.info("Running Upload Images Function.")
        print("Uploading images.\n")
        # creates the URL used to send the first request
        URL = self.baseUrl + "/api/v1/courses/" + self.courseID + "/files"
        # creates a list of all the files in the image folder
        images = os.listdir("images")
        for x in images:
            # contains all the needed information about the file being uploaded
            data = {"name": x, "size": str(os.stat("images/" + x).st_size), "parent_folder_path": "", "content_type": "image/png"}
            # contains the authentication
            header = {"Authorization": "Bearer " + self.access_token}
            # sends the requests
            temp = requests.post(URL, data=data , headers=header)
            if(temp.status_code == 200):
                # creates a list of the requests results
                tempList = json.loads(temp.text)
                # sets url to the upload rul
                url = tempList["upload_url"]
                tempList["upload_params"]["filename"] = x
                tempList["upload_params"]["content_type"] = "image/png"
                # opens the current image and reads it
                file = {"file": (x, open("images/" + x, "rb").read(), "image/png")}
                # creates a header with everything in the tempList
                header = {"filename": tempList["upload_params"]["filename"], "content_type": tempList["upload_params"]["content_type"]}
                # sends a request to the canvas servers with the image
                temp = requests.post(url=url, data=header, files=file)
                # checks if the status code is one of the accepted stats codes
                if(temp.status_code >= 301 and temp.status_code <= 399 or temp.status_code == 201):
                    # creates a list from the request results
                    tempList = json.loads(temp.text)
                    # sets url to the location
                    url = tempList["location"]
                    # creates a header
                    header = {"Authorization": "Bearer " + self.access_token, "Content-Length": '0'}
                    # sends the request
                    temp = requests.post(url, headers=header)
                else:
                    logging.critical("Could not upload images.\n\n" + str(temp.text))
                    # tells the user the status code and the results from the request
                    print("Upload Images Failed.")
            else:
                logging.critical("Could not upload images.\n\n" + str(temp.text))
                # tells the user the status code and the results from the request
                print("Upload Images Failed")
    # This function gets the upload URL of a file from the canvas course
    # Parameters: image: string         
    def getImagesUrl(self, image:str):
        logging.info("Running get Images Url function.")
        # creates the url used to get all the folders the coruse has
        URL = self.baseUrl + "/api/v1/courses/" + self.courseID + "/folders"
        # creates the header file used for authentication
        header = {"Authorization": "Bearer " + self.access_token}
        # sets folderList to the response from canvas
        folderList = requests.get(url=URL, headers=header)
        # creates a list of all the folders the course has
        folderList = json.loads(folderList.text)
        # goes though the folderList
        for i in range(len(folderList)):
            # checks if the current folder's name is 
            if(folderList[i]["name"] == ""):
                # creates the URL to get the upload URL from the canvas course
                url = self.baseUrl + "/api/v1/" + "/folders/" + str(folderList[i]["id"]) + "/files"
                # sets fileList to the response from canvas
                fileList = requests.get(url=url, headers=header)
                # creates a list of all the files in the  folder
                fileList = json.loads(fileList.text)
                # goes though the fileList
                for i in range(len(fileList)):
                    # checks if the current file's name is equal to the image's name
                    if(fileList[i]["display_name"] == image):
                        # returns the file's upload url
                        return fileList[i]["url"]
    # This function gets the admin account's ID
    def getAdminAccount(self):
        logging.info("Running Get Admin Account Function")
        # creates the url
        url = self.baseUrl + "/api/v1/accounts"
        # sets the authentication to the access_token
        headers = {'Authorization': 'Bearer ' + self.access_token}
        # makes a request to the canvas server for the school's ID
        info = requests.get(url=url, headers=headers)
        # sets accountID to the school's ID
        self.adminID = str(info.json()[0]["id"]) # type: ignore   
    # matches info from both the Rediker csv and the canvas csv then assigns class variables to information from both files.
    def matchCourses(self):
        logging.info("Running Match Course Function")
        # opens the Rediker csv file
        RedikerFile = open(self.csvFilePath, newline="")
        # opens the canvas csv file
        canvasReport = open("", newline="")
        # reads the Rediker csv file
        RedikerFile = csv.reader(RedikerFile)
        # reads the canvas file
        canvasReport = csv.reader(canvasReport)
        # goes through the Rediker file looking for the courseID and section number that match
        # The ones entered into the class
        for red in RedikerFile:
            # checks if the current course ID and section number match the entered ones
            if(red[1] == self.courseSISID and red[2] == self.sectionNum):
                # sets the course name to the 17th column in the Rediker export
                self.courseName = red[14]
                # goes though the canvas csv file looking for the course ID and section number in the canvas SISID
                for can in canvasReport:
                    # removes the unneeded parts of the SISID 
                    code = can[1][can[1].find("-") + 1:]
                    # checks if the match the entered ones
                    if(code == str(self.courseSISID) + str(self.sectionNum)):
                        temp = ""
                        try:
                            # splits the teachers name
                            temp = red[5].split(" ")
                            # reverses the teacher's name
                            self.teacher = temp[1] + " " + temp[0]
                        except IndexError:
                            self.teacher = temp
                        except Exception as e:
                            logging.error(e)
                            return False
                         # the list of characters to remove from the teacher's name
                        charToRemove = ["!", "@", "#", "$", "%", "^", "&", "(", "*", ")", "_", "-", "+", "=", "{", '[', ";", "}", ']',":", "/", "?", ".", ">", "<", ",", "`", "~", "\\", "|",]
                        # goes through the charToRemove and check if there are in the teacher's name
                        for k in charToRemove:
                            # replaces the current charater with nothing in the teachers name
                            self.teacher = str(self.teacher).replace(k, "")
                        if(self.teacher[0] == " "):
                            str(self.teacher).replace(" ", "")
                        # sets the course location to Rediker's 5th column
                        self.location = red[4]
                        # sets the courseID to canvas's first column
                        self.courseID = can[0]
                        # sets the courseSISID to canvas's second column
                        self.courseSISID = can[1]
                        # stops the function
                        return True
    # This function change the settings of the canvas course
    def changeSettings(self):
        logging.info("Running Change Settings Function.")
        # tells the user the program is changing the settings on the canvas page
        print("Changing settings.\n")
        # creates the url used to upload the change to the course page
        url = self.baseUrl + '/api/v1/courses/' + (self.courseID) + '/settings'
        # the authentication method
        header = {'Authorization' : 'Bearer ' + self.access_token}
        # changes the two settings below to true
        payload = {"hide_final_grades": True, "hide_distribution_graphs": True}
        # sends the changes to the canvas page
        requests.put(url, headers = header, params= payload)
    # logs all variables
    def logEveryThing(self):
        logging.info("Course ID: " + str(self.courseID))
        logging.info("Course Name: " + str(self.courseName))
        logging.info("Location: " + str(self.location))
        logging.info("Teacher: " + str(self.teacher))
        logging.info("Email: " + str(self.email))
        logging.info("Course SISID: " + str(self.courseSISID))
        logging.info("Teacher ID: " + str(self.teacherID))
        logging.info("Access Token: " + str(self.access_token))
        logging.info("Base URL: " + str(self.baseUrl))
        logging.info("CSV File Path: " + str(self.csvFilePath))
        logging.info("Admin ID: " + str(self.adminID))
        logging.info("Section Number: " + str(self.sectionNum))
