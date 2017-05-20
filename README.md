# Comment Police

`Last Modified: 08-29-2016`

This page contains information pertaining to the Comment Police project that was completed at a intern hackathon. The Comment Police project was originally developed by Amy Harris, Roshan Mirajkar, and Daniel Hoerauf of the 2016 intern team.

## Goal
Create a web service that takes in text inputs and evaluates text using extensible list of rules that are listed below. This can be used as a tool to help moderate WaPo comments by informing users of comment guidelines violations. The idea is to be adaptable and customizable ruleset for whatever attributes the incoming comment has. For example, a certain section of WaPo may have more reliable commenters, so only the spam check rule filter would be implemented.

## Project Setup

To get Comment Police app to run locally, follow instructions below. By running the app locally, you will be able to test sample comments against the designed rules and recieve an output. Note that some steps may differ depending on your operating system.

1. @Mac **_open terminal_**                                                                                                   
   @Windows **_open cmd_** 

2. Navigate to a directory where you want to store the project locally. Creating a new directory is recommended. Once you are in the directory you have chosen, on the command line use the command - `git@github.com:indianHacker/comments-police.git`.  

 This will clone the repo into your directory and you will have access to the project locally.
 
3. Navigate to `comment-police/local`

4. Create a virtual env using command `virtualenv wapo-comment-police`  

5. Activate virtual env using command `source wapo-comment-police/bin/activate` 

6. Now we want to unsure we have the correct file compatibilities and versions, to do this we will be downloading the requirements. Navigate to `comment-police/local` and run the command `pip install -r requirements.txt`. This will install the requirements and dependencies needed to run the app. Ensure there are no errors, then proceed.  

7. Run command: `python app.py` to get app running locally. 

8. Paste link <http://localhost:8080/demo/> in your browser. Enter the desired text inside the comment box and hit submit. You can use your own samples or the provided text samples in `sample.txt`. When an entered comment violates a rule, text will be displayed above the comment detailing feedback to the user depending on which rule was violated.

## Rules
`Last Modified: 08-29-2016`
- Excessive Uppercase 
- Black Word 
- Grey Words
- Spam (Repitition)
- Over Max Character Count 
- Directed User to USer Agression 

**_Each rule has its own return message when broken. This message can be improved by the comment editors, as currently we made our own sample messages._**


## Future Vision
1. Use the current rules logic to create a backend database that would be useded to track comments and changes made to comments. The front end would handle communicating information back to the user i.e.: the rules they broke and why. The vision is to do live processing of user's comments so that when the user hits the submit button the comment is evaluated and if rules are broken provide feedback to user and if not, post the comment. One interesting study would be to see if giving comment feedback changes the behavior of commenters. If they are given a preliminary warning that the comment is getting flagged and will likely be deleted, does the commenter change their behavior?

2. Another possible addition down the road would be to use machine learning to detect more ‘bad words’ and auto add this to the black or grey lists. In particular, machine learning could improve the `directed_aggression` method, since the phrases and range of words checked was set up intuitively, without studying hundreds of comment patterns. 

3. Metrics could be collected using DataDog and presented to the comment editors in an easily readable dashboard.
