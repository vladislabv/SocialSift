# Gastronomic Intelligence Hub (GIH)

This web mining project focuses on the analysis of public data of gastronomic companies within Germany.

With the increasing diversity in the gastronomic industry, it becomes even more important to make the start-up decision based on facts. Whether it is for analyzing the market, competition or location, this solution will assist those interested in founding a business with all of these aspects.

The goal of the project is to gain a holistic understanding of the gastronomy landscape in Germany. To achieve this, public data from various information sources will be collected and analyzed so that sound insights can be gained.

For this purpose, web mining techniques are used to provide information about restaurants, cafés, bars and other gastronomic businesses. This includes information such as locations, opening hours, ratings, menus and the like.

The platform not only enables detailed analysis of the data, but also provides tools that can be used to visualize and interpret it. In this way, prospective restaurant entrepreneurs, investors or market researchers can make qualified decisions.

# Code & Dependencies
Before running code, be sure all dependencies are installed:

-- scraper
"scrapy"
"scrapy-user-agents"
"python-dateutil"
"phonenumbers"

-- flask UI
"flask"
"flask-login"
"flask-wtf"
"flask-caching"
"email-validator"

-- both
"pymongo"
"python-dotenv"

To run the scraper for inserting data into your (local) instance of MongoDB, you will need:
`scrapy run spider restos.py`

After some data collected, you will need to start the Flask via:
`flask run run_flask.py --no-debugger --no-reload`

That is it, enjoy exploring the collected & aggregated data!

# Contribution & Maintaince
Vladislav Stasenko & Sinan Eker, but further community is highly welcome!

------------
Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   ├── webscraper     <- any txt/csv files coming from the Scrapy spiders
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- Paper where the final project is fully described.
    │
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
    │
    └── logs               <- Logging information running separately from Spiders and Flask
    ...

--------
