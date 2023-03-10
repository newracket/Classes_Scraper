import json
import re

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://act.ucsd.edu/scheduleOfClasses/scheduleOfClassesStudentResult.htm"
# URL = "https://act.ucsd.edu/scheduleOfClasses/scheduleOfClassesStudentResult.htm?selectedTerm=WI23&xsoc_term=&loggedIn=false&tabNum=&selectedSubjects=AIP+&selectedSubjects=AAS+&selectedSubjects=AWP+&selectedSubjects=ANES&selectedSubjects=ANBI&selectedSubjects=ANAR&selectedSubjects=ANTH&selectedSubjects=ANSC&selectedSubjects=AESE&selectedSubjects=AAPI&selectedSubjects=AUD+&selectedSubjects=BENG&selectedSubjects=BNFO&selectedSubjects=BIEB&selectedSubjects=BICD&selectedSubjects=BIPN&selectedSubjects=BIBC&selectedSubjects=BGGN&selectedSubjects=BGJC&selectedSubjects=BGRD&selectedSubjects=BGSE&selectedSubjects=BILD&selectedSubjects=BIMM&selectedSubjects=BISP&selectedSubjects=BIOM&selectedSubjects=CMM+&selectedSubjects=CENG&selectedSubjects=CHEM&selectedSubjects=CHIN&selectedSubjects=CLAS&selectedSubjects=CCS+&selectedSubjects=CLIN&selectedSubjects=CLRE&selectedSubjects=COGS&selectedSubjects=COMM&selectedSubjects=COGR&selectedSubjects=CSS+&selectedSubjects=CSE+&selectedSubjects=CGS+&selectedSubjects=CAT+&selectedSubjects=TDDM&selectedSubjects=TDHD&selectedSubjects=TDMV&selectedSubjects=TDPF&selectedSubjects=TDTR&selectedSubjects=DSC+&selectedSubjects=DSE+&selectedSubjects=DERM&selectedSubjects=DSGN&selectedSubjects=DOC+&selectedSubjects=DDPM&selectedSubjects=ECON&selectedSubjects=EDS+&selectedSubjects=ERC+&selectedSubjects=ECE+&selectedSubjects=EMED&selectedSubjects=ENG+&selectedSubjects=ENVR&selectedSubjects=ESYS&selectedSubjects=ETIM&selectedSubjects=ETHN&selectedSubjects=EXPR&selectedSubjects=FMPH&selectedSubjects=FPM+&selectedSubjects=FILM&selectedSubjects=GPCO&selectedSubjects=GPEC&selectedSubjects=GPGN&selectedSubjects=GPIM&selectedSubjects=GPLA&selectedSubjects=GPPA&selectedSubjects=GPPS&selectedSubjects=GLBH&selectedSubjects=GSS+&selectedSubjects=HITO&selectedSubjects=HIAF&selectedSubjects=HIEA&selectedSubjects=HIEU&selectedSubjects=HILA&selectedSubjects=HISC&selectedSubjects=HINE&selectedSubjects=HIUS&selectedSubjects=HIGR&selectedSubjects=HILD&selectedSubjects=HDS+&selectedSubjects=HMNR&selectedSubjects=HUM+&selectedSubjects=INTL&selectedSubjects=JAPN&selectedSubjects=JWSP&selectedSubjects=LATI&selectedSubjects=LHCO&selectedSubjects=LISL&selectedSubjects=LIAB&selectedSubjects=LIDS&selectedSubjects=LIFR&selectedSubjects=LIGN&selectedSubjects=LIGM&selectedSubjects=LIHL&selectedSubjects=LIIT&selectedSubjects=LIPO&selectedSubjects=LISP&selectedSubjects=LTAF&selectedSubjects=LTCH&selectedSubjects=LTCO&selectedSubjects=LTCS&selectedSubjects=LTEU&selectedSubjects=LTFR&selectedSubjects=LTGM&selectedSubjects=LTGK&selectedSubjects=LTIT&selectedSubjects=LTKO&selectedSubjects=LTLA&selectedSubjects=LTRU&selectedSubjects=LTSP&selectedSubjects=LTTH&selectedSubjects=LTWR&selectedSubjects=LTEN&selectedSubjects=LTWL&selectedSubjects=LTEA&selectedSubjects=MMW+&selectedSubjects=MBC+&selectedSubjects=MATS&selectedSubjects=MATH&selectedSubjects=MSED&selectedSubjects=MAE+&selectedSubjects=MED+&selectedSubjects=MCWP&selectedSubjects=MUS+&selectedSubjects=NANO&selectedSubjects=NEU+&selectedSubjects=NEUG&selectedSubjects=OBG+&selectedSubjects=OPTH&selectedSubjects=ORTH&selectedSubjects=PATH&selectedSubjects=PEDS&selectedSubjects=PHAR&selectedSubjects=SPPS&selectedSubjects=PHIL&selectedSubjects=PHYS&selectedSubjects=PHYA&selectedSubjects=POLI&selectedSubjects=PSY+&selectedSubjects=PSYC&selectedSubjects=RMAS&selectedSubjects=RAD+&selectedSubjects=MGTF&selectedSubjects=MGT+&selectedSubjects=MGTA&selectedSubjects=MGTP&selectedSubjects=RELI&selectedSubjects=RMED&selectedSubjects=REV+&selectedSubjects=SPPH&selectedSubjects=SOMI&selectedSubjects=SOMC&selectedSubjects=SIOC&selectedSubjects=SIOG&selectedSubjects=SIOB&selectedSubjects=SIO+&selectedSubjects=SEV+&selectedSubjects=SOCG&selectedSubjects=SOCE&selectedSubjects=SOCI&selectedSubjects=SE++&selectedSubjects=SURG&selectedSubjects=SYN+&selectedSubjects=TDAC&selectedSubjects=TDDE&selectedSubjects=TDDR&selectedSubjects=TDGE&selectedSubjects=TDGR&selectedSubjects=TDHT&selectedSubjects=TDPW&selectedSubjects=TDPR&selectedSubjects=TMC+&selectedSubjects=USP+&selectedSubjects=UROL&selectedSubjects=VIS+&selectedSubjects=WARR&selectedSubjects=WCWP&selectedSubjects=WES+&_selectedSubjects=1&schedOption1=true&_schedOption1=on&_schedOption11=on&_schedOption12=on&schedOption2=true&_schedOption2=on&_schedOption4=on&_schedOption5=on&_schedOption3=on&_schedOption7=on&_schedOption8=on&_schedOption13=on&_schedOption10=on&_schedOption9=on&schDay=M&_schDay=on&schDay=T&_schDay=on&schDay=W&_schDay=on&schDay=R&_schDay=on&schDay=F&_schDay=on&schDay=S&_schDay=on&schStartTime=12%3A00&schStartAmPm=0&schEndTime=12%3A00&schEndAmPm=0&_selectedDepartments=1&schedOption1Dept=true&_schedOption1Dept=on&_schedOption11Dept=on&_schedOption12Dept=on&schedOption2Dept=true&_schedOption2Dept=on&_schedOption4Dept=on&_schedOption5Dept=on&_schedOption3Dept=on&_schedOption7Dept=on&_schedOption8Dept=on&_schedOption13Dept=on&_schedOption10Dept=on&_schedOption9Dept=on&schDayDept=M&_schDayDept=on&schDayDept=T&_schDayDept=on&schDayDept=W&_schDayDept=on&schDayDept=R&_schDayDept=on&schDayDept=F&_schDayDept=on&schDayDept=S&_schDayDept=on&schStartTimeDept=12%3A00&schStartAmPmDept=0&schEndTimeDept=12%3A00&schEndAmPmDept=0&courses=&sections=&instructorType=begin&instructor=&titleType=contain&title=&_hideFullSec=on&_showPopup=on"
# URL = "https://act.ucsd.edu/scheduleOfClasses/scheduleOfClassesStudentResult.htm?selectedTerm=SP23&xsoc_term=&loggedIn=false&tabNum=&selectedSubjects=CSE&schedOption1=true&_schedOption1=on&_schedOption11=on&_schedOption12=on&schedOption2=true&_schedOption2=on&_schedOption4=on&_schedOption5=on&_schedOption3=on&_schedOption7=on&_schedOption8=on&_schedOption13=on&_schedOption10=on&_schedOption9=on&schDay=M&_schDay=on&schDay=T&_schDay=on&schDay=W&_schDay=on&schDay=R&_schDay=on&schDay=F&_schDay=on&schDay=S&_schDay=on&schStartTime=12%3A00&schStartAmPm=0&schEndTime=12%3A00&schEndAmPm=0&_selectedDepartments=1&schedOption1Dept=true&_schedOption1Dept=on&_schedOption11Dept=on&_schedOption12Dept=on&schedOption2Dept=true&_schedOption2Dept=on&_schedOption4Dept=on&_schedOption5Dept=on&_schedOption3Dept=on&_schedOption7Dept=on&_schedOption8Dept=on&_schedOption13Dept=on&_schedOption10Dept=on&_schedOption9Dept=on&schDayDept=M&_schDayDept=on&schDayDept=T&_schDayDept=on&schDayDept=W&_schDayDept=on&schDayDept=R&_schDayDept=on&schDayDept=F&_schDayDept=on&schDayDept=S&_schDayDept=on&schStartTimeDept=12%3A00&schStartAmPmDept=0&schEndTimeDept=12%3A00&schEndAmPmDept=0&courses=&sections=&instructorType=begin&instructor=&titleType=contain&title=&_hideFullSec=on&_showPopup=on"
FILE = "data/sp23.json"
options = Options()
options.add_argument("--headless")
options.add_experimental_option("detach", True)


def open_browser():
    # Open URL
    driver = webdriver.Chrome(
        options=options, service=Service(ChromeDriverManager().install())
    )
    driver.get(URL)

    # Selects all departments in search
    select = Select(driver.find_element(By.ID, "selectedSubjects"))
    for optionElement in select.options:
        select.select_by_value(optionElement.get_attribute("value"))

    # Clicks the search button
    submitButton = driver.find_element(By.ID, "socFacSubmit")
    submitButton.click()

    # Gets the current page and total pages
    tdElements = driver.find_elements(By.XPATH, '//td[@align="right"]')
    if len(tdElements) == 0:
        print("No classes found")
        return

    pagesText = tdElements[0].text
    [currentPage, totalPages] = \
        re.findall(r"Page \((\d+) of (\d+)\)", pagesText)[0]

    # Goes through all rows in the table
    data = Data()
    department = ""
    courseName = ""
    while int(currentPage) <= int(totalPages):
        tableElement = driver.find_element(By.XPATH, '//table[@class="tbrdr"]')
        rows = tableElement.find_element(By.TAG_NAME, "tbody").find_elements(
            By.TAG_NAME, "tr"
        )

        for row in rows:
            # Checks if the row contains the department
            try:
                sectionRow = row.find_element(By.XPATH, './td[@colspan="13"]')
                possibleDepartments = re.findall(r"\(([A-Z ]{4,5})\)",
                                                 sectionRow.text)

                if len(possibleDepartments) > 0:
                    department = possibleDepartments[0].strip()
                    print(department)
                    data.addDepartment(Department(department))
            except NoSuchElementException:
                pass

            # Check if row contains the class name
            try:
                possibleCourseNames = lastRow.find_elements(
                    By.XPATH, './td[@class="crsheader"]'
                )
                if len(possibleCourseNames) > 1:
                    courseName = possibleCourseNames[1].text
                    data.getDepartment(department).addCourse(Course(courseName))
            except:
                pass

            # Checks if the row contains the class
            if "sectxt" in row.get_attribute("class"):
                usefulElements = row.find_elements(By.TAG_NAME, "td")
                if len(usefulElements) < 12:
                    continue

                sectionType = usefulElements[3].text
                days = usefulElements[5].text
                times = usefulElements[6].text
                buildingName = usefulElements[7].text
                roomNumber = usefulElements[8].text
                professor = usefulElements[9].text
                seatsRemainingText = usefulElements[10].text
                spaces = usefulElements[11].text
                waitlistMatched = re.findall(r"Waitlist\((\d+)\)",
                                             seatsRemainingText)
                seatsRemaining = (
                    "-" + waitlistMatched[0]
                    if len(waitlistMatched) > 0
                    else seatsRemainingText
                )

                print(courseName)
                data.getDepartment(department).getCourse(courseName).addSection(
                    Section(
                        sectionType,
                        days,
                        times,
                        buildingName,
                        roomNumber,
                        professor,
                        seatsRemaining,
                        spaces,
                    )
                )
            lastRow = row

        # print(data.getData())
        uploadData(data, FILE)

        # Gets next page
        # Change to ?page= for general URL, &page= for specific URL
        driver.get(URL + "?page=" + str(int(currentPage) + 1))
        tdElements = driver.find_elements(By.XPATH, '//td[@align="right"]')
        if len(tdElements) == 0:
            print("No classes found")
            return

        pagesText = tdElements[0].text
        [currentPage, totalPages] = \
            re.findall(r"Page \((\d+) of (\d+)\)", pagesText)[0]

    wait = WebDriverWait(driver, 600)
    element = wait.until(
        expected_conditions.title_contains("Student/Class Info Temp"))

    print("Done")


def uploadData(data, file):
    dataJSON = data.getData()

    with open(file, "w") as outfile:
        json.dump(dataJSON, outfile)


class Data:
    def __init__(self):
        self.departments = {}

    def addDepartment(self, department):
        if department.name not in self.departments:
            self.departments[department.name] = department

    def getDepartment(self, departmentName):
        return self.departments[departmentName]

    def getData(self):
        data = {}
        for department in self.departments:
            data[department] = self.getDepartment(department).getData()

        return data

    def __str__(self):
        output = ""
        for department in self.departments:
            output += str(self.getDepartment(department))

        return output


class Department:
    def __init__(self, name):
        self.name = name
        self.courses = {}

    def addCourse(self, courseObject):
        if courseObject.name not in self.courses:
            self.courses[courseObject.name] = courseObject

    def getCourse(self, courseName):
        return self.courses[courseName]

    def getData(self):
        data = {}
        for course in self.courses:
            data[course] = self.getCourse(course).getData()

        return data

    def __str__(self):
        output = self.name.strip() + " Department \n"
        for course in self.courses:
            output += str(self.getCourse(course))

        return output


class Course:
    def __init__(self, name):
        self.name = name
        self.sections = []

    def addSection(self, section):
        self.sections.append(section)

    def getData(self):
        data = []
        for section in self.sections:
            data.append(section.getData())

        return data

    def __str__(self):
        return self.name + "\n" + "\n".join(
            [str(e) for e in self.sections]) + "\n"


class Section:
    def __init__(
            self,
            sectionType,
            days,
            times,
            buildingName,
            roomNumber,
            professor,
            seatsRemaining,
            spaces,
    ):
        self.sectionType = sectionType
        self.days = days
        self.times = times
        self.buildingName = buildingName
        self.roomNumber = roomNumber
        self.professor = professor
        self.seatsRemaining = seatsRemaining
        self.spaces = spaces

    def getData(self):
        return {
            "sectionType": self.sectionType,
            "days": self.days,
            "times": self.times,
            "buildingName": self.buildingName,
            "roomNumber": self.roomNumber,
            "professor": self.professor,
            "seatsRemaining": self.seatsRemaining,
            "spaces": self.spaces,
        }

    def __str__(self):
        return (
                self.sectionType
                + " "
                + self.days
                + " "
                + self.times
                + " "
                + self.buildingName
                + " "
                + self.roomNumber
                + " "
                + self.professor
                + " "
                + self.seatsRemaining
                + " "
                + self.spaces
        )


open_browser()
