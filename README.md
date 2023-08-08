# University of Waterloo Classes Bot
#### Video Demo: https://www.youtube.com/watch?v=ci9gOJX0x7s
#### University of Waterloo Classes Website: https://classes.uwaterloo.ca/

# main.py
## Why only main.py?
#### At first I had a helper.py that contained spotcheck(). However, one day out of the blue main.py 
#### stopped recognizing helper.py, giving a warning saying that it doesn't recognize the module. It
#### was likely due to me messing around with environments with venv but I didn't know how to solve,
#### which led to me combining helper.py into main.py.


## Step 1: Send a post request to the University of Waterloo Database Website
#### My first step was to figure out how to send a post request to the UW website. I decided to use
#### response.post() as it was pretty convenient. I didn't use os.execute() along with a curl command
#### as it always outputted a string that was harder to work with. Unfortunately the website does not
#### use get, as it would have been so much easier to just enter a modified url instead of having to 
#### manually submit a form.

## Step 2: Read the output, parse the HTML
#### Due to the UW Classes Website having limited API options, I decided it was best to just parse 
#### the HTML with an HTML parser. I chose BeautifulSoup4 due to its convenience. response.text only
#### gave back text, but bs4 allowed me to only parse through the table data <td>, giving me a list
#### of all the data in the table. It was no dictionary, as the UW HTML did not assign any values with
#### and special id tags, which lead me to hard code some of the index value increments. Nonetheless,
#### this step allowed me to finally read and detect whether or not a class was full.

## Step 3: Send an email alerting availability
#### Now that the script can detect vacancies in a class, it should now be able to send some form of
#### notification to the user. I chose email due to its accessability, but in the future I would also
#### like to implement a cellphone messaging feature, as I don't always have wifi. I settled on STMP
#### as it was the first result. However, it was a good choice as it was easy to configure and the 
#### tutorial was straightforward. I made things look better with python's email module. At first I
#### was getting a password error, but that was fixed with a generation of a new google app password
#### that I hardcoded in. If others need to use this code, they should configure their own passwords 
#### and emails.

# .github/workflows/actions.yml
#### Now that I had the script working, I needed to find a way to keep this script running from 8am
#### to 8pm. I spent a very long time finding free services, but platforms such as Google Cloud
#### and Amazon Web Services required entering credit card information. PythonAnywhere did not require
#### it but it only allowed outside connection to a list of whitelisted websites, websites that had
#### well documented APIs. I finally found a video which suggested using Github as an option, which I 
#### was both suprised and excited about, as I had already seen the Seminar on Github and wanted to
#### work with the commands. By following youtube videos and the official Github Actions YML and cron
#### documentation, I got the script running! However, the script was running at 4am, which was far
#### the scheduled 8am schedule. I looked into the Github documentation and realized they were running
#### the code on UTC as opposed to my EST! Now that my code is working, I am currently testing it on 
#### the MATH 145 Class 6025, which before was the class that I checked every 30 minutes with my own
#### hands.

## requirements.text, .gitignore
#### Just some files needed in order to get the code running (I have no clue how it works but the
#### youtube video and sample repository had it)