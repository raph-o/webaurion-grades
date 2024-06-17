# Webaurion grades

Just a simple utility script which fetch your grades on webaurion and tell you if there is a new one on your discord channel.

To configure this, it's actually pretty straightforward :

- Install the requirements by running `pip -r requirements.txt`
- Put your username and your password in the script (line 80)
- Create a webhook on your discord server by going to `Server Settings > Integrations > Create Webhook`
- Copy the url of your webhook and put it in the script (`webhook_url` variable)

Then run it. You could have it run on a daily basis so that he will tell you when a new grade appear.