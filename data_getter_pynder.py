import datetime, requests, secrets, tkinter, json, csv, keyboard
from emoji import UNICODE_EMOJI
from PIL import Image

tinderToken = secrets.AUTH_TOKEN
TINDER_URL = "https://api.gotinder.com"
TINDER_AUTH_URL = "/v2/auth/login/facebook"
TINDER_PROFILES_URL = "/v2/recs/core"


def get_info(data, swipeValue):
    id = data['user']["_id"]
    name = data.get("name", "Unknown")

    bio = data.get("bio", "")
    bioTextLength = len(str(bio))
    if UNICODE_EMOJI in bio.split():
        bioTextEmoji = True
    else:
        bioTextEmoji = False

    distance = data.get("distance_mi", 0)*1.609 # Change distance to km

    birth_date = datetime.datetime.strptime(data["birth_date"], '%Y-%m-%dT%H:%M:%S.%fZ') if data.get(
        "birth_date", False) else None
    gender = ["Male", "Female", "Unknown"][data.get("gender", 2)]

    images = list(map(lambda photo: photo["url"], data.get("photos", [])))

    jobTitle = list(
        map(lambda job: {"title": job.get("title", {}).get("name"), "company": job.get("company", {}).get("name")},
            data.get("jobs", [])))
    if jobTitle == "":
        job = False
    else:
        job = True

    schoolTitle = list(map(lambda school: school["name"], data.get("schools", [])))
    if schoolTitle == "":
        school = False
    else:
        school = True

    csvFile = open('swipe_data.csv', 'w', newline='')
    object = csv.writer(csvFile)
    object.writerow((id, name, bio, bioTextEmoji, bioTextLength, distance, job, school, swipeValue))
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
                for image in user['user']['photos'][0]['processedFiles']:
                    print(image['url'])
                    load = Image.open(image['url'])

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
