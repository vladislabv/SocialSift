1. Introduction

Wir freuen uns, Ihnen unser Projekt, SocialSift, vorzustellen. Das Projekt widmet sich der Analyse öffentlicher Daten aus sozialen Medien und der Bereitstellung einer grundlegenden Analyse der Online-Präsenz von Nischen-Bloggern und Unternehmen. Mit dem explosionsartigen Wachstum der Nutzung sozialer Medien ist es für Unternehmen und Influencer immer wichtiger geworden, eine starke Online-Präsenz zu haben, um ihr Publikum anzuziehen und zu engagieren.

SocialSift wird Unternehmen und Influencern helfen, indem es Einblicke in ihre Online-Präsenz bietet, ihre Aktivitäten in sozialen Medien analysiert, wichtige Einflussnehmer und Follower identifiziert und andere wertvolle Metriken bereitstellt, die ihnen helfen, datenbasierte Entscheidungen über ihre Online-Strategien zu treffen. Dadurch, dass die Ergebnisse werden auf (kostenfreien) öffentlichen Daten bereitgestellt, ermöglicht es allen, auch kleinen Unternehmen & Blogger-Anfänger, mehr Traffic auf ihre Seiten zu ziehen, ohne grandioses Budget für Posts-Promotion auszugeben.

In dieser Exposition möchten wir die Ziele, Methoden und potenziellen Vorteile von SocialSift erläutern. Außerdem werden wir die Bedeutung der Analyse von sozialen Medien im heutigen digitalen Zeitalter diskutieren und wie SocialSift Unternehmen und Influencern helfen kann, sich einen Vorsprung zu verschaffen.

2. Methodology

Für das "SocialSift" Projekt wird hauptsächlich auf Social Media APIs zur Datenerfassung zurückgegriffen. Das Scraping von Daten wird zunehmend unpopulär, da es auf vielen Websites unzulässig ist und schnell zu einer IP-Sperre führen kann. Trotzdem wird für bestimmte Zwecke auch Scraping eingesetzt, um eine flexible Datenerfassung sicherzustellen. Die Daten werden stündlich aus den APIs und gelegentlich auch durch Scraping gesammelt, um Änderungen der Post-KPIs zu verfolgen. Alle Daten werden in einer relationalen PostgreSQL-Datenbank gespeichert, die sowohl für den Storage als auch für die Datennormalisierung verwendet wird. Die Normalisierung erfolgt durch Views, die eine schnelle Verarbeitung der Daten ermöglichen. Diese Views dienen als Grundlage für die NLP- und Clustering-Modelle. Nach Abschluss des Trainings werden die Ergebnisse in Form von Jupyter Notebooks präsentiert, um individualisierte Berichte für jeden Influencer oder jedes Unternehmen zu erstellen.

# ML-modelling

Bei der Realisierung von unserem Projekt wird den Schwerpunkt auf Nature Language Processing Thema gelegt, da der Text ein der einfachsten und zudem mächtigsten Tools, die den Unternehmen und Influencer auf Social Media zur Verfügung steht. Mit Hilfe von Latent Dirichlet allocation (LDA) haben wir vor, die wichtigsten Themen aus den letzten Posts zu identifizieren und diese Information mit den gesammelten numerischen Metriken (KPIs), wie Likes/Shares/Impressions/Comments zu kategorisieren. Somit werden wir eine Vorstellung haben, welche Themen oder Bezüge in bessere Sichtbarkeit von Posts auf Social Media in einer bestimmten Nische führen würde.

3. Potential Results

Die Ergebnisse werden in Form von individualisierten Berichten präsentiert, die den Bedürfnissen und Zielen jedes einzelnen Kunden entsprechen.

Mit SocialSift können kleinere Unternehmen und Influencer-Anfänger ihre Social-Media-Strategien verbessern und ihr Online-Publikum besser ansprechen. Unsere Analysen können zeigen, welche Art von Inhalten das Engagement erhöhen und welche Trends in der Branche beliebt sind. Wir werden auch Identifizieren von Schlüsselinfluencern und Followern, die für den Erfolg eines Unternehmens von Bedeutung sein können.

Unsere Reports können auch helfen, die Effektivität von Werbekampagnen und Marketingstrategien zu messen und somit Kosten und Zeit zu sparen. SocialSift gibt Kunden die Möglichkeit, auf Daten-basierte Entscheidungen zu treffen und ihre Social-Media-Präsenz zu optimieren, um ihre Ziele zu erreichen.

4. Discussion

5. Conclusion