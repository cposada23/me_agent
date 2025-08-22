---
title: me_agent
app_file: main.py
sdk: gradio
sdk_version: 5.43.1
---
## And now for deployment

This code is in `main.py`

We will deploy to HuggingFace Spaces.

Before you start: remember to update the files in the "me" directory - your LinkedIn profile and summary.txt - so that it talks about you! Also change `self.name = "Camilo Posada Angel"` in `/tools/ChatAgent.py`..  

Also check that there's no README file within the 1_foundations directory. If there is one, please delete it. The deploy process creates a new README file in this directory for you.

1. Visit https://huggingface.co and set up an account  
2. From the Avatar menu on the top right, choose Access Tokens. Choose "Create New Token". Give it WRITE permissions - it needs to have WRITE permissions! Keep a record of your new key.  
3. In the Terminal, run: `uv tool install 'huggingface_hub[cli]'` to install the HuggingFace tool, then `hf auth login` to login at the command line with your key. Afterwards, run `hf auth whoami` to check you're logged in  
4. Take your new token and add it to your .env file: `HF_TOKEN=hf_xxx` for the future
5. From the 1_foundations folder, enter: `uv run gradio deploy` 
6. Follow its instructions: name it "career_conversation", specify app.py, choose cpu-basic as the hardware, say Yes to needing to supply secrets, provide your openai api key, your pushover user and token, and say "no" to github actions.  

Thank you Robert, James, Martins, Andras and Priya for these tips.  
Please read the next 2 sections - how to change your Secrets, and how to redeploy your Space (you may need to delete the README.md that gets created in this 1_foundations directory).

#### More about these secrets:

If you're confused by what's going on with these secrets: it just wants you to enter the key name and value for each of your secrets -- so you would enter:  
`OPENAI_API_KEY`  
Followed by:  
`sk-proj-...`  

And if you don't want to set secrets this way, or something goes wrong with it, it's no problem - you can change your secrets later:  
1. Log in to HuggingFace website  
2. Go to your profile screen via the Avatar menu on the top right  
3. Select the Space you deployed  
4. Click on the Settings wheel on the top right  
5. You can scroll down to change your secrets (Variables and Secrets section), delete the space, etc.

#### And now you should be deployed!
