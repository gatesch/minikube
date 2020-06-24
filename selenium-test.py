#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True
driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver',options=options)
#
#open connection
driver.get('http://php.tesch.loc')
get_title = driver.title
print("The website is running, the title is: ")
print(get_title)
if driver.title == "HPE CD Pipeline Demo":
        print("This is the wrong website title - test failed")
        driver.close()
	exit (32)
else:
        print("functional test passed")
        driver.close()
	exit (0)
