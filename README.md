# Trippy
### Name
Vishal Gupta

### Email id
vishstar88@gmail.com

### Team Name
git_rollback

### Project type
Mobile app based project

### Hackathon Idea
A virtual tourist guide that offers the following features : 

- **Travel Plan recommendations**
We track the user's travel history to understand the user's preferences and then recommend unvisited tourist sites using a collaborative filtering algorithm on the ratings by user, opening hours of tourist sites and distance from the user's location. 

- **Augmented Reality to provide a more immersive experience**
Each tourist attraction (statues) will have 3D models so that they can be visualized anytime and anywhere. We aim to provide an experience that preserve a site's historic splendour

- **Review Summarization**
Since reviews by other tourists provide key insight into the tourist places and it is not possible to read 1000s of reviews, summarization of public opinion could significantly help tourists. 

- **Multilingual offline application**
Content shall served in English, Hindi and Spanish thereby catering a larger crowd who need not be eloquent in English. 

- Audio Tours of cities and attractions
- Helpline numbers so tourists can get help easily

### How many people built your project?
3

### Briefly describe who built what part of the project.
I, Vishal worked on the recommender, NLP for highlights generation and firebase integration.
Shreyas worked on the Django backend
 Shrikanth worked on the Android app and Unity integration. 
 
### Who are your users?
All Tourists

### Describe your frontend (UI) language, framework that you have used to implement your idea.
Android + Retrofit + Unity, Vuforia

### Describe your backend language, framework and stack that you have used to implement your idea.
Python + Django, Scipy, pandas, requests, nltk, gensim

### Mention the third party APIs used if any.
Firestore, Vuforia

### Github link to your project
Backend : https://github.com/py-ranoid/Trippy
Android Repository :  https://github.com/shrikanth7698/TrippyDroid

### Hasura App URL
https://app.descent25.hasura-app.io/

### Video link of your working prototype
https://drive.google.com/open?id=1UROTMypG1SZjsMY-rHBD7n8lTUU-iPqb
##### Demo explanation: 

1. User selectes language of his choice
2. OTP to authentication user. Used as a primary key to track user's preferences and app usage. 
3. Opening the app displays a list of recommened places. The recommendation considers **user's visited-places history**, **ratings by 1000s of travellers** which we scraped from the web, **opening hours** of tourist attractions and lastly, **user's location**. For the demo which we took back at MS Uni, we set the user's history to Lake Pichola (a lake), Nehru Park (a garden) a garden and Bagore Ki Haveli (a musuem). Hence it displays a mix of historic places and gardens. Vintage Car Museum is top-most recommendation since it was closest to MS Uni, close enough to the user's preferences, and was open. 
4. The attractions page opens at the About tab, which has a description of the city along with a narration of the same (Play button).
5. Highlights are effectively review summaries. We performed natural language processing on the reviews to obtain a list of frequent noun phrases. These would help the tourist understand the reviews of a place without actually reading a single review.
6. Highlights are followed by Photos and directions to the attraction
7. *Discover* lists the sub-attractions inside the Attraction. Each has an audio tour of its own.
8. Tourists also can buy tickets for the attraction and pay on Bhim/Paypal
9. City page is very similar to Attractions page. We've added a list of helpline numbers for the tourists to contact in case of emergency.
10. Subattractions will also have 3D models that can be used to experience articles or structures that the user cannot view otherwise since the same have either deteriorated or are not open to the public. 
11. While our AR does needs a lot more work, we hope to accomplish the same and also market the app using the prize money (if we win. :P)
### APK link
https://drive.google.com/open?id=1so176QXwtdj_ZOTRqJqxnUo3MA8Afg2j
