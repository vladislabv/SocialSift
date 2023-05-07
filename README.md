# SocialSift

==============================

This repo serves for a team project using web-mining techniques. The project dedicated to analyzing public data from social media and providing basic analysis of niche bloggers' and companies' online presence.

------------

# IDEAS

* Crime-Statistiken
    - Visualisierung: Live Map basierend auf die Daten über Täten (etw. Ort, Zeit und ggf. zusätzliche Daten)
    - Analysen: Aufgrund von Daten, örtliche | zeitliche Analysen
    - Datenquellen: ???

* Preisvergleich
    - Visualisierung: diverse Grafiken zu Preisfluktuationen, Trends
    - Produkt: 
        - Website mit Visualisierungen & Analysen (auf laufenenden Daten)
        - User-interaktiv
        - Eingabe von Ware und Vergleich von Preisen auf verschiedenen Plattformen (Amazon, Ebay)
        - Entwicklung von einem simplen Algorithm zur Produktempfehlung zu dem User, bzw. anzeigen von nicht-default Metriken, um den Benutzern die Entscheidung zu erleichtern
    - Datenquellen: Market APIs with free access or WebScraping

* Social Media Analysis
    - Analysis:
        1. Analysis of popular niche influencers' content strategy
            - Using the social media API, track the posts and engagement metrics of top N influencers;
            - Perform a topic modeling analysis using NLP techniques to identify the key topics and themes that these influencers are posting about;
            - Cluster the influencers based on their content strategy and identify the most effective strategy that generates the most engagement.
        2. Sentiment analysis of niche brands'/companies' social media mentions
            - Using the Facebook API, track the mentions of top 10 brands on social media;
            - Perform sentiment analysis on the mentions to identify the overall sentiment towards the brand;
            - Use the results to identify areas for improvement in the brand's social media strategy.
        3. Analysis of popular niche hashtags
            - Using the Instagram API, track the usage and engagement metrics of the top 10 travel hashtags;
            - Perform a clustering analysis to identify the most effective types of hashtags in terms of generating engagement.
    - Implementation:
        1. Popular niche influencers' analysis
            - Collect data on top N niche influencers' posts and engagement metrics using public data from API;
            - Perform topic modeling analysis using NLP techniques to identify the key topics and themes in their posts;
            - Cluster the influencers based on their content strategy using K-means clustering;
            - Analyze the clusters to identify the most effective strategy that generates the most engagement.
        2. Sentiment analysis of niche brands'/companies' social media mentions
            - Collect data on top N brands' social media mentions using social media APIs;
            - Perform sentiment analysis using NLP techniques to identify the overall sentiment towards the brand;
            - Analyze the results to identify areas for improvement in the brand's social media strategy.
        3. Niche hashtags analysis
            - Collect data on the usage and engagement metrics of top N niche hashtags using API;
            - Perform clustering analysis using K-means clustering to identify the most effective types of hashtags in terms of generating engagement;
            - Analyze the results to identify the most effective types of hashtags and use them to inform social media strategy.
    
    - Options to choose:
        - Product 1: Perform templates for the topic analysis, user provides niche, N, influencer id, brand names and gets the analysis in a report form. (ML models should be pretrained) - Analysis lack historical data.
        - Product 2: Choose 1 niche and perform analysing by including historical data. The scope of analysis in this case can be extended.
        - Form of a product: GUI interface (Y/N) or package.

    - Data: Social Media offering free tier APIs / minimal WebScraping techniques.
    - Data Structure (public data of post or page/user):
        - Page (followers, following, bio)
        - Post (publishing date, lifetime impressions & engagements (likes, shares), sometimes Meta Info like MessageText or comments/share texts) - Set time window to lookup lifetime values and get time bounded measurements
        
==============================

Project Organization

------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
=======

 Expose (bis 12.06.)
 
 Inhalt (1-2 Seiten):
 
 1. Projektname: SocialSift
 2. Projektziel
 3. Projektumfang (Eingrenzung/Scope)
 4. Genutzte Datenquellen
 5. Projektmeilensteine (Was müssen wir tun, um unser Projektziel zu erreichen)
 6. Nutzen und Mehrwert des Projektes
 
 -> Vorgang und Darstellung des Projektes soll klar und deutlich sein.
