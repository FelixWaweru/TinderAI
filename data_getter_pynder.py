import datetime, requests, secrets, tkinter, json, csv, keyboard, urllib, io, PIL, time
from emoji import UNICODE_EMOJI
from PIL import ImageTk
import PIL.Image
from tkinter import *
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

    # Get instances of emojis in Bio
    if UNICODE_EMOJI in bio.split():
        bioTextEmoji = True
    else:
        bioTextEmoji = False

    # Get the user distance
    distance = str(int(data["distance_mi"])*1.609) # Change distance to km

    # Get the user age
    try:
        # Get first four digits(Year) in Json birthdate
        birth_date = data['user']["birth_date"][:4]
        age = str(2020 - int(birth_date))
    except:
        age = "0"

    # Use Images in future AI
    # images = list(map(lambda photo: photo["url"], data.get("photos", [])))

    # Get the user Job
    try:
        jobTitle = data['user']['jobs']['title']['name']

    except:
        jobTitle = ""

    if str(jobTitle) == "":
        job = False
    else:
        job = True

    # Get the user School
    try:
     schoolTitle = data['user']['schools']['name']
    except:
        schoolTitle = ""

    if str(schoolTitle) == "":
        school = False
    else:
        school = True

    csvFile = open('swipe_data.csv', 'a', newline='')
    object = csv.writer(csvFile)
    object.writerow((id, name, age, bio.encode("utf-8"), bioTextEmoji, bioTextLength, distance, job, school, swipeValue))
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

        data = requests.get(TINDER_URL + TINDER_PROFILES_URL, headers={"X-Auth-Token": tinderToken}).json()
        try:
            print("Connected successfully")
            for user in data['data']['results']:

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
                print(user['user']['name'])
                print(user['user']["bio"])
                print(age)
                print(str(user["distance_mi"]))
                try:
                    print(user['user']['jobs']['company']['name'])
                except:
                    print("No Job Company")
                try:
                    print(user['user']['jobs']['title']['name'])
                except:
                    print("No Job Name")
                try:
                    print(user['user']['schools']['name'])
                except:
                    print("No School Name")

                # Get the user keypress. Q for dislike and E for like
                choice = input("Begin button press: ")
                if choice == 'e':
                    like(user)
                    print("Like")
                elif choice == 'q':
                    dislike(user)
                    print("Dislike")

        except Exception as e:
            print(str(e) + " Connection failed. Idk why")

    except Exception as e:
        print(str(e) + " Connection failure")

startSwiping()
