# Credits to https://www.projectpro.io/recipes/create-word-cloud-python

import os
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np

plt.set_loglevel("critical")

def generate(text):
    print(os.path.abspath(__file__))
    mask = np.array(Image.open(os.path.realpath(__file__)+r"\..\static\resources\mask2.png"))
    word_cloud = WordCloud(
        width=1920,
        height=1920,
        background_color="#EAEBED",
        colormap="turbo",
        collocations=False,
        stopwords=STOPWORDS,
        mask=mask
    ).generate(text)

    plt.figure( figsize=(20,20) )
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(os.path.realpath(__file__)+r"\..\static\resources\wordcloud.svg", dpi=300, format='svg')