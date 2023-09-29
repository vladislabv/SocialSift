# Gastronomic Intelligence Hub (GIH)

// Short (general) description of the project

1. Einführung / Motivation

Im vorliegenden Exposé werden wir Ihnen unser Projekt „Gastronomic Intelligence Hub“ (GIH) vorstellen. Das Web-Mining-Projekt konzentriert sich auf die Analyse öffentlicher Daten von gastronomischen Unternehmen innerhalb Deutschlands. Mit der steigenden Vielfalt in der Gastronomiebranche wird es umso wichtiger, die
Gründungsentscheidung faktenbasiert zu treffen. Ob für die Analyse von Markt, Wettbewerb oder Standort wird unsere Lösung den Gründungsinteressierten zur Seite stehen.

// Body of the project

2. Vorgehensweise und Projektziel

2.1 Data Collection

Zu Beginn des Projektes werden die Metadaten über deutsche Restaurants (z.B. Website, Adresse und Name) gesammelt. Hierzu wird die Aggregator-Website „htps://www.speisekarte.de“ genutzt, auf der Unternehmen ihre Kontaktinformationen bereitstellen. Derzeit existiert eine Liste von mehr als 20 Tsd. Restaurants, die täglich auf den neusten Stand gebracht wird. Für das Ziehen von weiteren nützlichen Informationen, wie Öffnungszeiten oder Speisekarten, wird ein Website-Crawler gebaut, der die Webseiten der zuvor gesammelten Restaurants scannen wird. Dabei wird erwartet, dass mindestens 80 Prozent der Restaurants über eine eigene Webseite
verfügt.

Neben dem Crawling werden auch diverse Services mit Kundenbewertungen genutzt, deren Daten zur Ermittlung von bestgewerteten Gerichten und Durchschnittsbeträgen verwendet werden. Es wird davon ausgegangen, dass über 60 Prozent der Restaurants auf einer der größten Bewertungsplattformen (Yelp, Golocal) zu finden sind.


2.2 Data preprocessing

Die gesammelten Daten werden mit Hilfe von Python bereinigt. Python bietet eine Vielzahl von Bibliotheken, die das Text Mining bzw. Nature Language Processing (NLP) erleichtern. Im Preprocessing geht es vor allem darum, die Speisekarten oder andere Informationen aus unstrukturierten HTML- und JSON-Dokumenten in eine analysierbare und lesbare Form zu bringen.

Anschließend werden die bereinigten Daten in eine relationale PostgreSQL-Datenbank überführt. Um eine effiziente Datenverarbeitung zu ermöglichen, erfolgt die Normalisierung durch Views und diversen SQL-Abfragen. Diese Kombination ermöglicht eine schnelle Verarbeitung der Daten und trägt zu einer problemlosen Handhabung weiterer Änderungen bei.


2.3 Data Analysis (Projektziel)

Die Daten sollen den Unternehmer dabei unterstützen, folgende Fragen zu beantworten:
    - Wie verteilen sich die gegebenen Restaurants in einem bestimmten Bereich nach Preisniveau etc.?
    - Welche Gerichte sind auf einem bestimmten Standort auf der Karte am beliebtesten?

Um diese Fragestellungen anzugehen, wird ein Template erstellt, bei dem der dynamische Inhalt von dem ausgewählten Bereich auf der Deutschlandkarte abhängt. Für die ausstehenden Analysen werden verschiedene Python-Funktionen verwendet, um eine effiziente Datenverarbeitung zu ermöglichen. Um die Kommunikation mit den Benutzern zu vereinfachen, wird eine Webanwendung mit Flask entwickelt, die die Analysen mit einer benutzerfreundlichen Visualisierung darstellt.


3. Fazit
   
Das GIH-Projekt hat das Potenzial, Entrepreneurs wertvolle Einblicke in die Gastronomiebranche bereitzustellen. Zum Beispiel kann das Tool dazu beitragen, die Verteilung von Restaurants in einem bestimmten Bereich besser zu verstehen oder die beliebtesten Gerichte in der Nähe eines bestimmten Punktes auf der Karte zu identifizieren. Außerdem können die Daten dabei unterstützen, eine Nische im Markt zu finden und eine fundierte Entscheidung über die Gründung eines neuen Unternehmens zu treffen.

------------
// Some sort of general documentation
Project Organization

------------

    ├── LICENSE
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
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>