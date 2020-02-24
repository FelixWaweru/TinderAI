import requests, secrets, tkinter, csv, urllib, io, PIL, keras
from PIL import ImageTk
import PIL.Image
import numpy as np
from tkinter import *
from keras.models import load_model

# TODO: Update Gist with updated code

tinderToken = secrets.AUTH_TOKEN
TINDER_URL = "https://api.gotinder.com"
TINDER_AUTH_URL = "/v2/auth/login/facebook"
TINDER_PROFILES_URL = "/v2/recs/core"


def get_info(data, swipeValue):
    # Get the user ID
    id = data['user']["_id"]

    # Get the user name
    name = data['user']['name']

    # Get the user Bio
    bio = data['user']['bio']

    # Get the Bio length
    bioTextLength = len(str(bio))

    # Get the user distance
    distance = str(int(data["distance_mi"])*1.609) # Change distance to km

    # Get the user age
    try:
        # Get first four digits(Year) in Json birthdate
        birth_date = data['user']["birth_date"][:4]
        age = str(2020 - int(birth_date))
    except:
        age = "0"

    numberOfPhotos = len(data['user']['photos'])

    # Use Images in future AI
    # images = list(map(lambda photo: photo["url"], data.get("photos", [])))

    # Get the user Job
    try:
        jobTitle = data['user']['jobs']

    except:
        jobTitle = "[]"

    if str(jobTitle) == "[]":
        job = False
    else:
        job = True

    # Get the user School
    try:
     schoolTitle = data['user']['schools']
    except:
        schoolTitle = "[]"

    if str(schoolTitle) == "[]":
        school = False
    else:
        school = True

    csvFile = open('swipe_data.csv', 'a', newline='')
    object = csv.writer(csvFile)
    object.writerow((id, name, bio.encode("utf-8"), age, numberOfPhotos, bioTextLength, distance, job, school, swipeValue))
    csvFile.close()
    print( str(name) + "'s Data saved")

def like(data):
    user_id = data['user']["_id"]
    liked = requests.get(TINDER_URL + f"/like/{user_id}", headers={"X-Auth-Token": tinderToken}).json()
    print("Liked")
    get_info(data, "Like")

def dislike(data):
    user_id = data['user']["_id"]
    liked = requests.get(TINDER_URL + f"/pass/{user_id}", headers={"X-Auth-Token": tinderToken}).json()
    print("Disliked")
    get_info(data, "Dislike")

def startSwiping():
    try:
        print("Connecting to Tinder API")
        print("Getting Nearby Users")
        # get user profile info of people near me
        data = requests.get(TINDER_URL + TINDER_PROFILES_URL, headers={"X-Auth-Token": tinderToken}).json()
        try:
            print("Connected successfully")
            for user in data['data']['results']:
                print(len(user['user']['photos']))
                # Display the user pictures
                for image in user['user']['photos']:
                    mainWindow = tkinter.Tk()
                    mainWindow.title("Profile Pictures")
                    raw_data = urllib.request.urlopen(image['url']).read()
                    im = PIL.Image.open(io.BytesIO(raw_data))
                    image = ImageTk.PhotoImage(im.resize((400, 400)))
                    label = Label(mainWindow, image=image)
                    closeButton = Button(mainWindow, text = "Next" , command = mainWindow.destroy)
                    label.pack()
                    closeButton.pack()
                    mainWindow.mainloop()

                # Get first four digits(Year) in Json birthdate
                birth_date = str(user['user']["birth_date"])[:4]
                age = str(2020 - int(birth_date))

                # Show user info in the terminal
                print(user['user']['name'])
                print("Bio: " + user['user']["bio"])
                print("Age: " + age)
                print("Distance: " + str(user["distance_mi"]))
                print("Company: " + str(user['user']['jobs']))
                print("School: " + str(user['user']['schools']))

                # Get the user keypress. Q for dislike and E for like
                choice = input("Begin button press: ")
                if choice == 'e':
                    like(user)
                    print("Like")
                elif choice == 'q':
                    dislike(user)
                    print("Dislike")
                else:
                    print("Invalid input")

        except Exception as e:
            print(str(e) + " Connection terminated. There's an error in the function.")

    except Exception as e:
        print(str(e) + " Connection failure")



def TinderAI(school, age, numberOfPhotos, bioTextLength, distance, job):
    classifier = load_model('TinderAIModel.h5')
    # Single user Tinder prediction
    swipePrediction = classifier.predict(np.array([[school, age, numberOfPhotos, bioTextLength, distance, job]]))
    swipePrediction = (swipePrediction > 0.5)

    return swipePrediction


def AI_Swiper():
    try:
        print("Connecting to Tinder API")
        print("Getting Nearby Users")
        # get user profile info of people near me
        data = requests.get(TINDER_URL + TINDER_PROFILES_URL, headers={"X-Auth-Token": tinderToken}).json()
        try:
            print("Connected successfully")
            for user in data['data']['results']:

                # Get first four digits(Year) in Json birthdate
                birth_date = str(user['user']["birth_date"])[:4]
                age = str(2020 - int(birth_date))

                # Show user info in the terminal
                print(user['user']['name'])
                print("Bio: " + user['user']["bio"])
                print("Age: " + age)
                print("Distance: " + str(user["distance_mi"]))
                print("Company: " + str(user['user']['jobs']))
                print("School: " + str(user['user']['schools']))

                # Get the user School
                try:
                    schoolTitle = user['user']['schools']
                except:
                    schoolTitle = "[]"

                if str(schoolTitle) == "[]":
                    school = 0
                else:
                    school = 1

                # Get the user Bio
                bio = user['user']['bio']

                # Get the Bio length
                bioTextLength = int(len(str(bio)))

                # Get the user distance
                distance = int(int(user["distance_mi"]) * 1.609)  # Change distance to km

                # Get the user age
                try:
                    # Get first four digits(Year) in Json birthdate
                    birth_date = user['user']["birth_date"][:4]
                    age = int(2020 - int(birth_date))
                except:
                    age = 0

                numberOfPhotos = len(user['user']['photos'])

                # Use Images in future AI
                # images = list(map(lambda photo: photo["url"], data.get("photos", [])))

                # Get the user Job
                try:
                    jobTitle = user['user']['jobs']

                except:
                    jobTitle = "[]"

                if str(jobTitle) == "[]":
                    job = 0
                else:
                    job = 1
                
                choice = TinderAI(school, age, numberOfPhotos, bioTextLength, distance, job)
                print(str(choice))
                if str(choice) == '[[False]]':
                    dislike(user)
                    print("Dislike")
                elif str(choice) == '[[ True]]':
                    like(user)
                    print("Like")
                else:
                    print("Invalid input")

        except Exception as e:
            print(str(e) + " Connection terminated. There's an error in the function.")

    except Exception as e:
        print(str(e) + " Connection failure")

AI_Swiper()
