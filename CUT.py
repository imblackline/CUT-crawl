import Base
import requests
from bs4 import BeautifulSoup
import logging
import json

from multiprocessing.connection import wait
from selenium import webdriver


logger = logging.getLogger('__main__')


class UCB(Base.BaseCrawler):
    Course_Page_Url = "https://student.portal.chalmers.se/en/chalmersstudies/courseinformation/Pages/SearchCourse.aspx"
    University = "Chalmers University of Technology"
    Abbreviation = "CUT"
    University_Homepage = "https://www.chalmers.se"
    # Below fields didn't find in the website
    References = None
    Scores = None
    Projects = None
    PATH = 'https://student.portal.chalmers.se/en/chalmersstudies/courseinformation/Pages/SearchCourse.aspx?flag=1&query_start=1&batch_size=13&sortorder=CODE&search_ac_year=2021/2022&parsergrp=0'
    driver = webdriver.Chrome('./chromedriver.exe')
    driver.get(PATH)

    def get_courses_of_department(self):    
        courses=[]
        rows = self.driver.find_elements_by_xpath("//*[@id='ctl00_m_g_e5a73096_eb61_4444_8e90_3fb9615aec2f']/div/div/table[3]/tbody/tr")[2:]
        for idx,row in enumerate(rows):
            tds = row.find_elements_by_xpath(".//child::td")
            courses.append({
                    'id': tds[0].text,
                    'name':tds[1].text,
                    'department_id':tds[3].text,
                    'course_link':tds[4].find_element_by_xpath(".//a").get_attribute('href'),
                    'course_homepage':tds[5].find_element_by_xpath(".//a").get_attribute('href')
            })
            # print(idx)

        return courses

    def get_course_data(self, course):
        self.driver.get(course['course_link'])
        department_name = self.driver.find_element_by_xpath("//*[@id='ctl00_m_g_e5a73096_eb61_4444_8e90_3fb9615aec2f']/div/table[1]/tbody/tr[11]/td").text.split(' - ')[1]
        Professor_name = self.driver.find_element_by_xpath("//*[text() = 'Examiner:']/following-sibling::a").text
        Professor_Homepage = self.driver.find_element_by_xpath("//*[text() = 'Examiner:']/following-sibling::a").get_attribute('href')
        ######### problem ##########
        try:
            Description = self.driver.find_element_by_xpath("//*[text() = 'Content']/following-sibling::*").text
        except:
            Description = ""
        # requirments = self.driver.find_element_by_xpath("//*[text() = 'Specific entry requirements']/following-sibling::*").text
        # prerequisites = self.driver.find_element_by_xpath("//*[text() = 'Course specific prerequisites']/following-sibling::*").text
        # Objective = self.driver.find_element_by_xpath("//*[text() = 'Aim']/following-sibling::*").text
        # outcomes = self.driver.find_elements_by_xpath("//*[text() = 'Learning outcomes ']/following-sibling::li")
        # for outcome in outcomes:
        #     print(outcome.text)
        print(Description)
        return department_name,Professor_name,Professor_Homepage,Description

    def handler(self):
        ########################## departments with beautifulsoup #################################
        # html_content = requests.get(self.Course_Page_Url).text
        # soup = BeautifulSoup(html_content, 'html.parser')
        # departmentSelects = soup.find_all("select")[2].text.splitlines()[1:]
        # departments = []
        # for dep in departmentSelects:
        #     departments.append({
        #         'id': dep.split(' - ')[0],
        #         'name':dep.split(' - ')[1]
        #     })
            


       ############################## departments with selenium ###################################
        # departments = []
        # options = self.driver.find_element_by_name('field_search_dept').find_elements_by_xpath(".//child::option")[1:]
        # for option in options:
        #     # print(option.text)
        #     departments.append({
        #         'id': option.text.split(' - ')[0],
        #         'name':option.text.split(' - ')[1]
        #     })
        # print(departments)


       ############################## get courses with selenium ###################################
        courses = self.get_courses_of_department()
        # print(courses)
        for course in courses:
            print(course['course_homepage'])
            department_name,Professor_name,Professor_Homepage,Description = self.get_course_data(course)
            # self.save_course_data(
            #     self.University, self.Abbreviation, department_name, course['name'], 20,
            #     Professor_name, 'Objective*',' self.Prerequisite*', 'Required_Skills*', 'Outcome*', 'self.References', 'self.Scores',
            #     Description, 'self.Projects', self.University_Homepage, course['course_homepage'], Professor_Homepage
            # )

        logger.info(f"{self.Abbreviation}: Total {self.course_count} courses were crawled successfully.")

ucb = UCB()
ucb.handler()


while(True):
       pass