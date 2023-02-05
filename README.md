# National AI Student Challenge Submission : AI-You

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**
    - [About](#about)
    - [Instructions](#setup)
    - [Credits](#credits)
    - [Bibliography](#bibliography)

<!-- markdown-toc end -->

## AI-You

![](/app/static/resources/logo_aiyou.svg)

This project is a team submission to AI Singapore for the AI Student Challenge 2023. 

### About

AI-You came about as a recognition of the drowning whirlwinds of information people face and the decisions they make in their everyday lives. Whether it's planning a date with someone for the first time, or special events with loved ones, it can be quite *'lece'* to pour over paragraphs of reviews to find the next adventure for you.

Powered by the Sentic GCN model through SGnlp, AI-You helps you and me sift through the haze of text, emojis and endless star ratings to get to what we want to know - *people say good or not?*

Providing sentiment analysis on key specific areas like cleanliness, ambience along with the basics like location and contacts, AI-You promises to help your search not just be efficient but a happier experience with this all-in-one web application.

Too many reviews? Well... AI-got-you.

### Instructions

#### Step 1: Download this project

You can choose to clone this project repository from Github or download the zip file from above. On your terminal or Git Bash, type the following:

```shell
cd "any_folder_path_you_want_here"
git clone https://github.com/mavene/aisc2023-aiyou
```

#### Step 2: Run setup file

Then, run through the setup for the demo:

```shell
python setup.py
```

You should now see this message at the end of the running terminal:

```shell
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

If there are any issues with the setup.py file, run these at the root of the folder:

```shell
pipenv shell
pipenv install -r requirements.txt
flask run
```

Look for the abovementioned message to confirm set up is successful.

#### Step 3: Run demo

Open your browser and access `http://127.0.0.1:5000/` to interact with the demo (and our friendly mascot!)

### Credits

Prototype developed by SUTD studetns - Darren Ang Wee Kiat, Dian Maisara, Michelle Ordelia Sumaryo, Wong Oi Shin

AI Bricks tools provided by AI Singapore

### Bibliography

[1] Sentic GCN: A Simple But Effective Framework for Aspect-Based Sentiment Analysis via Affective Knowledge Enhanced GCN - https://github.com/BinLiang-NLP/Sentic-GCN

[2] SGnlp Model Demos - https://sgnlp.aisingapore.net/aspect-based-sentiment-analysis 

[3] SGnlp Documentation - https://sgnlp.aisingapore.net/docs/ 