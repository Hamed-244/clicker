
# Auto Clicker

[Persian README - راهنمای فارسی](README_FA.md)

This project is an auto clicker built using Python and Flask. It allows you to automate clicks on [hamster combat](https://t.me/hamsTer_kombat_bot/start?startapp=kentId7445441654)  telegram bot.

## Features

- Automate clicks
- Taking all the profits every 20 minutes
- Easy to setup

## Installation Guide

Follow these steps to set up and run the project on your local machine:

>[!WARNING]
> IT COULD BAN YOUR ACCOUNT SO DON'T USE THIS BOT WITH YOUR PRIMARY ACCOUNT

1. **Clone this repository:**

   ```bash
   git clone https://github.com/Hamed-Fakoori/clicker.git
   cd clicker
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

6. **Find the esential keys for you accounts:**

   - go to [this](#get-account-information-guide) section to see how to get account informationi

6. **Run the application:**

   ```bash
   python app.py
   ```

7. **Open your web browser and go to:**

   ```
   http://localhost:8000
   ```

8. **Say thanks to me**
   - star this project on github
   - you can say thanks to me by liking my post on [linkedin]() or [virgool]()

## Get Account Information Guide
1. open Telegram on web
2. press ctrl + f12 or right click and inspect
3. go to network tab
4. refresh the page 
5. now you can find telegram-web-app.js file
6. overwrite this code 
   ```
   Object.defineProperty(WebApp, 'platform', {
     get: function () {
         return webAppPlatform;
     },
     enumerable: true,
   });
   ```
   with this code
   ```
   Object.defineProperty(WebApp, 'platform', {
     get: function () {
         return 'ios';
     }, enumerable: true,
   });
   ```
   it allow you to run bot on the web platform
7. open bot and make some taps
8. now you can see the taps request on you network tab of console
9. open the request and find request headers 
10. copy Authorization key and paste it to data.json file
11. you can find other information in the response tab 
12. find the keys we write them in the data.json and put them in data.json file
>[!NOTE]
>DON'T COPY `BEARER` FROM THE AUTHORIZATION KEY