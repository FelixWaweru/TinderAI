from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv, keyboard
from emoji import UNICODE_EMOJI

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://tinder.com')
loginUsername = "wawerufelix60@gmail.com"
loginPassword = "xil015weru3d"


def login():
    driver.get('https://tinder.com')

    time.sleep(15)

    fb_btn = driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/div[2]/button')
    fb_btn.click()

    # switch to login popup
    base_window = driver.window_handles[0]
    driver.switch_to.window(driver.window_handles[1])

    email_in = driver.find_element_by_xpath('//*[@id="email"]')
    email_in.send_keys(loginUsername)

    pw_in = driver.find_element_by_xpath('//*[@id="pass"]')
    pw_in.send_keys(loginPassword)

    login_btn = driver.find_element_by_xpath('//*[@id="u_0_0"]')
    login_btn.click()
    print("Logging in")

    driver.switch_to.window(base_window)
    time.sleep(5)

    popup_1 = driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
    popup_1.click()

    popup_2 = driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
    popup_2.click()


def filter(dataValue):
    if "kilometers" in dataValue:
        distanceVal = dataValue

    elif "kilometers" in dataValue:
        distanceVal = dataValue

    elif dataValue == "Woman":
        break

    elif "Lives" in dataValue:
        break
        
    elif "kilometers" in dataValue:
        distanceVal = dataValue

def get_info():
    time.sleep(10)
    print("Getting Information")
    # Click the more information button
    moreInfo = driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[6]/button')
    moreInfo.click()

    # get Name
    print("Getting name")
    name = driver.find_element_by_xpath \
        ('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div/h1')
    nameText = name.get_attribute('innerHTML')

    # get Bio
    print("Getting Bio")
    try:
        bio = driver.find_element_by_xpath \
            ('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]')
        bioText = bio.get_attribute('innerHTML')
    except:
        bioText = ""

    print("Getting Bio length")
    bioTextLength = len(str(bioText))

    print("Getting bio emojis")
    count = 0
    if UNICODE_EMOJI in bioText.split():
        bioTextEmoji = True
    else:
        bioTextEmoji = False

    # get Age
    print("Getting age")
    age = driver.find_element_by_xpath \
        ('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/span')
    ageText = age.get_attribute('innerHTML')



    # get Distance
    print("Getting distance")
    distance = driver.find_element_by_xpath \
        ('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div/div/div[2]/div[2]/div[2]')
    distanceText = distance.get_attribute('innerHTML')
    # get the numerical distance value
    for s in distanceText.split():
        if s.isdigit():
            distanceText = s

    # get Job
    print("Getting Job")
    job = driver.find_element_by_xpath \
        ('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]')
    jobText = job.get_attribute('innerHTML')
    if str(jobText) == "":
        jobText = False
    else:
        jobText = True

    # get School
    print("Getting school")
    school = driver.find_element_by_xpath \
        ('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]')
    schoolText = school.get_attribute('innerHTML')
    if str(schoolText) == "":
        schoolText = False
    else:
        schoolText = True


def like():
    like_btn = driver.find_element_by_xpath(
        '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[3]')
    like_btn.click()


def dislike():
    dislike_btn = driver.find_element_by_xpath(
        '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/button[1]')
    dislike_btn.click()


def start_swiping():
    login()
    print("Logged In")
    try:
        info = get_info()
        print("Begin button press")
        if keyboard.is_pressed(''):
            print("Like")
            like()
            swipeValue = "Like"
            csvFile = open('swipe_data.csv', 'w', newline='')
            object = csv.writer(csvFile)
            object.writerow((info.nameText, info.bioText, info.bioTextLength, info.bioTextEmoji,
                             info.ageText, info.distanceText, info.jobText, info.schoolText, swipeValue))
            csvFile.close()
            print("Data saved")

        elif keyboard.is_pressed(''):
            print("Dislike")
            dislike()
            swipeValue = "Dislike"
            csvFile = open('swipe_data.csv', 'w', newline='')
            object = csv.writer(csvFile)
            object.writerow((info.nameText, info.bioText, info.bioTextLength, info.bioTextEmoji,
                             info.ageText, info.distanceText, info.jobText, info.schoolText, swipeValue))
            csvFile.close()
            print("Data saved")
    except Exception as e:
        print(e)



start_swiping()

