<h1 align="center" id="title">Digital Voice Assistant</h1>

<p align="center"><img src="https://tmbroadcast.com/wp-content/uploads/AI_translations.gif" alt="project-image"></p>

<p id="description">This project is a voice assistant application developed using the Python programming language. It can perform various tasks using voice commands such as sending emails controlling the web browser reading news and more.<br><br>This project is developed by integrating various Python libraries and external services. It utilizes libraries such as SpeechRecognition for voice recognition pyttsx3 for text-to-speech conversion NewsAPI for retrieving news and weather information and face_recognition for face recognition.</p>

  
  
<h2>🧐 Features</h2>
<br>
Here're some of the project's best features:

*   Ability to understand and process voice commands
*   Sending emails and performing online transactions
*   Opening the web browser and visiting specific websites
*   Retrieving information from Wikipedia
*   Checking the weather and news
*   Telling jokes and reading random jokes
*   Taking screenshots and simulating keyboard/mouse actions
*   Face recognition and performing custom operations using deep learning
<br>
<h2>🛠️ Installation Steps:</h2>
<br>
<p>You must download all the libraries in this file</p>

```
requirements.txt 
```
<p>You need to have a camera, and you can add "Facedetect.png" in the file. If you don't want to add photo, you can open jarvis.py file and run. After that if you want to you can say "I want to add face" then camera screen will show. </p>

```
Facedetect.png
```
<p>In line 527, you need to write your e-mail address, and in line 529 you need to write e-mail address and password. This can be crypt version and you can store in database. </p>

```
 msg['From'] = "...@gmail.com" #MAIL ADDRESS
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login("...@gmail.com", cipher_suite.decrypt(psw[0][0].encode("utf-8")).decode("utf-8")) #MAIL ADDRESS, PASSWORD
```
<p>In line 582, you need to insert news api client key. </p>

```
newsapi = NewsApiClient(api_key='#KEY')
```

<h2>💻 Built with</h2>
<br>
Technologies used in the project:

*   Python
*   AI
*   Speech Recognition
*   Text to Speech
*   Speech to Text
*   Face recognition
*   Weekly Planner
*   Sqlite
*   Multi Threading
*   UI Design
*   Emotion Analysis
  
<br>
<h2>Project Screenshots:</h2>
<br>
<img src="https://r.resimlink.com/8MNbD.png" alt="project-screenshot" width="600" height="400/">
<br>
<img src="https://r.resimlink.com/TygtbjVB.png" alt="project-screenshot" width="600" height="400/">
<br>
<img src="https://r.resimlink.com/p-EoG9HJF.png" alt="project-screenshot" width="600" height="400/">
<br>
<img src="https://r.resimlink.com/LZRzCU.png" alt="project-screenshot" width="300" height="300/">
<br>
<img src="https://r.resimlink.com/vQt27i5IZUkz.png" alt="project-screenshot" width="600" height="400/"><br> 
<br>
<h2>💖Like my work?</h2>
<br>
If you would like to contribute or enhance the project it is an open-source project and you can contribute through the GitHub repository.
