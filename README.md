# TinderAI
The Origin
My first encounter with online dating came across during my end of semester break in the middle of my fourth year in university.
I had been single for about two years (insert long story) when I decided to install Tinder, an online dating application, out of boredom and a maybe a little curiosity about what lay in wait for me within the world of online dating.
What followed was a two year cycle of swiping, matching, chatting and loss of interest in online dating after getting preoccupied with other things in my life.
“This would be so much easier if I had an AI wing man getting dates on my behalf.”
That was my catchphrase every time I started the cycle again but little did I know that soon, to Elon Musk’s disapproval, my dreams of having an Artificial Intelligence controlling my love life would come true. Sort of.
Earlier last year, I started an online course on Udemy centered around Artificial Neural Networks and as soon as I had completed the first chapter on creating Artificial Neural Networks(ANNs), I took everything I had learnt so far and decided to apply it to Tinder. The main aim was to make online dating as easy as possible for myself and also to identify any hidden patterns that lay within my online dating data. As the wise ancestors of computing used to say, you truly aren’t a programmer until you’ve tried automating every aspect of your life.
The first step of the project entailed collecting all of my Tinder data by downloading it directly from the source. I navigated to https://account.gotinder.com/data and once I logged into my account I received all my data via email within a day or so.

Now for the juicy bits.
Getting the data
The data came in a zip folder containing a JSON and a html file that allowed me to view my data in a nicely categorized view.

It contained my swiping history, user profile information, messaging history and even information regarding linked Spotify and Instagram profiles. Unfortunately, the data did not contain any information regarding the profiles I had interacted with.
This was a problem.
In order to properly train my ANN model I would require the profile information of the people I had interacted with and this meant I had to roll up my sleeves and look for a way to get it myself. I decided to do so by accessing Tinder, collecting the data of the user profiles I interacted with and saving it in an Excel spreadsheet that I would later use to train my model.
Tinder doesn’t have an open source API and thus I had to collect the data I would need by interacting with Tinder’s endpoints. An endpoint is basically a designated URL that is used by web applications such as Tinder to send and receive data using requests.
Lucky for me, the rest of the internet had already taken notice of this API vacuum and with some quick Google searches, I was able to find a list of several endpoints that would allow me to get the information of users near me and even like or dislike their profiles.
First things first, I needed to get access to my Tinder account. More specifically, I needed to get a unique authorization token that would identify my requests as coming from Felix’s profile and allow me send and receive those requests. Think of it as Tinder being a wedding and the authorization token as being my invite. As long as I had the invite I could freely go in and out of the wedding reception for some cake.

I was able to quickly find it in the Networks tab of my Google Chrome Page Inspector, within the header of a HTTP request sent by the browser. After importing the authorization token into my Python file, I created four primary functions that I would use to get my data and interact with other profiles.
The first function, ‘get_info’ is used to get a person’s details from their Tinder profile and sets them as plain text or boolean (True or False) values.

The second function is the ‘like’ function that is used to swipe right on the user profile i.e like the user and the third function is the ‘dislike’ function that is used to swipe left on the user profile i.e dislike the user.

Last is the ‘startSwiping’ function that would allow me to interact with the user profiles. The Pillow library allowed me see their profile pictures in a popup window and I was able to view their names, ages, bios and other details within the terminal. The function also received keyboard inputs in the terminal giving me the ability to ‘swipe left’ and ‘swipe right’ i.e like and dislike a user.
I assigned the keyboard character “E” to activate the ‘swipe right’ or ‘like’ function and “Q” to activate the ‘swipe left’ or ‘dislike’ function.


The popup window that allowed me to see a user’s profile pictures.

The terminal through which I can see the user’s information and interact with the code.
Making the Artificial Neural Network
After hours of “swiping”, I was finally able to collect a sizable dataset with roughly 200 rows of which would be sufficient enough to train my model. For this section of the project, I would be making use of the Numpy, Pandas and Sklearn libraries so as to create and train my data models.

The format of the data I had collected.
From my data, I would only use the age, number of photos, bio length, distance, job and school information to train my model since those are the data values most likely to affect the swipe value.
The idea was to create an Artificial Neural Network that would predict how likely I am to like or dislike a user once presented with that user’s profile data. It would then like or dislike their profile on my behalf.
After importing the Excel spreadsheet with our data into the Python file, we needed to replace every unique text value in our model with numbers by using a label encoder. Changing these text values into numbers allows for the Artificial Intelligence to process them faster and more easily. In our case, only the school, job and swipe columns contained text values and so we encoded them using Sklearn.

Next, we split the dataset into two sections; a test set and a training set. The training set is used to create the model that will be used by our AI and the test set is used to check how accurate the predictions made by the models are. For this project, we split the dataset into a standard 20% test data and 80% training data.

At this point, our model was ready to be created. Our Artificial Neural Network would have two hidden layers. These hidden layers take in the raw data in our dataset, pass it through an activator function and then returns an output. For the first hidden layer, we would use a Rectifier function since it is the most commonly used and returns the most accurate data for this kind of model. We would then pass the output from the first hidden layer through another hidden layer that would use a Sigmoid function. The Sigmoid function returns an output that reflects a probability since the output ranges between 0 and 1.
After passing our dataset through these layers, we can now compile the results, compare our Artificial Neural Network’s predictions to the results in the test set and then see how accurately it predicts whether I would have liked or disliked a profile. We’ll run through 1000 epochs because our dataset isn’t very big and this also allows the model become as accurate as possible.

Finally, function that would be imported into the ‘data_getter’ Python file was created. It would primarily receive data related to a user and then would return a swipe value i.e like or dislike. This would be the function that would reference the model we trained and decided to either like or dislike a user.

Within the ‘data_getter’ Python file, a new function that would pass data values into the ‘TinderAI’ function was created. Based on the swipe value it received from the Artificial Neural Network, it would send a response back to Tinder.

The function used by the AI to swipe.
Now it was time to let the AI have full reign over my Tinder account. Feeling like a father teaching their child how to drive in the family’s only car, I anxiously ran the code and sat back in the passenger seat watching. I had set a delay of two seconds per swipe so as to prevent the code from sending too many requests to Tinder and thus causing the connection to get terminated.
Every minute, the AI received data and liked or disliked thirty profiles. Thirty potential wives or life long partners in the hands of the model I had trained and it was honestly an exhilarating experience. As I sat there, I wondered if Charles Babbage, the father of computing, would have ever imagined that his invention would one day lead to a 24 year old guy in Kenya creating an Artificial Intelligence for his online dating profile.

The Artificial Neural Network in action.
Conclusion
I let the Artificial Neural Network run for a while so as to collect a sizable dataset. I then used this data to compare how my ANN performed in relation to me by graphing the data points and seeing how they differed.

A plot showing my swipe activity in relation to user age.

The same plot showing how the Artificial Neural Network swiped.
In the end, I was able to collect very interesting data in relation to how I swipe and the interactions I generate with users on online dating applications. I guess it takes an algorithm centered around your personal data to truly know yourself.

The dataset generated by the AI. Kind of picky isn’t it?
Right now, we are a few years or decades away from creating Artificial Intelligence with the capacity to understand and help decide upon complex human matters such as love and dating. However, as long as a young student of science like myself is able to learn and implement the fundamentals of AI by themselves, we will surely meet that goal soon enough.
