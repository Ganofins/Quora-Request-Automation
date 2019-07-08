import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def send_requests(url="https://www.quora.com/partners", max_wait=10):

    """Function for sending requests to the writers for each question"""

    #for reading the email and password from credentials.json file and storing it in credentials variable
    cred_file = open("./credentials.json", "r")
    credentials = cred_file.read()
    credentials = json.loads(credentials)
    cred_file.close()

    #for maximizing the browser's window
    options = Options()
    options.add_argument("--start-maximized")
    #options.headless = True

    browser = webdriver.Chrome('./chromedriver', options=options)

    browser.get(url)

    #for login to the user's account
    email = browser.find_element_by_xpath("//div[@class='form_column']/input[@name='email']")
    email.send_keys(credentials["email"])
    pwd = browser.find_element_by_xpath("//div[@class='form_column'][2]/input[@name='password']")
    pwd.send_keys(credentials["password"])
    pwd.send_keys(Keys.ENTER)

    #fetching all the questions on the page before sending any request for the older questions
    try:
        all_questions = WebDriverWait(browser, max_wait).until(EC.presence_of_element_located((By.ID, "questions")))
    except TimeoutException:
        exit("Invalid Email or Password")
    all_questions = all_questions.find_element_by_css_selector("div.paged_list_wrapper").find_elements_by_css_selector("div.QuestionListItem")

    length = len(all_questions)
    each_question = -1

    while each_question < length:

        each_question += 1

        #for scrolling the browser's window vertically by 38
        browser.execute_script("window.scrollTo(0, 38)")

        #when the question will be last then it will fetch the older questions after waiting 5 seconds
        if each_question == (len(all_questions)-1):
            sleep(5)
            all_questions = browser.find_element_by_id("questions").find_element_by_css_selector("div.paged_list_wrapper").find_elements_by_css_selector("div.QuestionListItem")
            length = len(all_questions)

        
        #when the question is not merged with other question then there will be a request answer button else it will skip that question
        try:
            request_ans_btn = all_questions[each_question].find_element_by_css_selector("div.a2a_section").find_element_by_css_selector("span")
            request_ans_btn.click()
        except:
            continue

        #for requesting the answers from the writers
        try:
            sleep(4)
            all_writers = browser.find_element_by_css_selector("div.paged_list_wrapper").find_elements_by_css_selector("div.request_answers_list_item")
            for each_writer in range(25):
                sleep(0.5)
                send_request = all_writers[each_writer].find_element_by_css_selector("div.ui_layout_text").find_element_by_css_selector("div.button_wrapper")
                send_request.click()
                browser.execute_script("window.scrollTo(0, 3)")
        except:
            print("Answer limit reached or Question is a sensitive question, and for that you have to manually request for answers")
            pass

        sleep(0.6)
        try:
            done_btn = browser.find_element_by_css_selector("div.modal_overlay:not(.hidden)").find_element_by_css_selector("div.modal_wrapper.normal:not(.hidden)").find_element_by_css_selector("div.modal_actions").find_element_by_css_selector("a.submit_button")
            done_btn.click()
        except:
            continue
        sleep(0.5)

    return browser.quit()

send_requests(max_wait=10)