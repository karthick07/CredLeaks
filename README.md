# Pastehunter
## Applying a text classification model on the scraped pastes to predict PII (only tested on Pastebin and for output format - json ).

###### This research was carried out as part of my Masters Thesis. The developed scripts is a Proof of concept to demonstrate how text classification model along with keywords/Yara rules can aid in identifying PII from pastes. Pastehunter was used as a scraper and I made use of the repo (https://github.com/secbug/PasteHunter) for scraping and all additional scripts were developed as part of the thesis.

## Text Classification
Following are the components developed:

```
Prefilter - Eliminate source code and empty pastes using keywords and MIME types.
Model - Feeding the filtered pastes to a Machine Learning model to predict PII.
Database - Filtered pastes are stored in a sqlite database and predicted paste IDs can be fetched from the database.
```

In the current once Pastehunter is started the script *runscraper.py* can be invoked in a new tab to predict PII. Once the model predicts a paste as PII it saves the paste content along with the metadata into a sqlite database.

PasteHunter
PasteHunter is a python3 application that is designed to query a collection of sites that host publicly pasted data. For all the pastes it finds it scans the raw contents against a series of Yara rules looking for information that can be used by an organisation or a researcher.

For setup instructions please see the official documentation https://pastehunter.readthedocs.io/en/latest/installation.html

Supported Inputs
Pastehunter currently has support for the following sites:

```
pastebin.com
gist.github.com # Gists
github.com # Public commit activity feed
slexy.org
stackexchange # There are about 176!
```

Supported Outputs
Pastehunter supports several output modules:
```
dump to ElasticSearch DB (default).
Email alerts (SMTP).
Slack Channel notifications.
Dump to JSON file.
Dump to CSV file.
Send to syslog.
```
Supported Sandboxes
Pastehunter supports several sandboxes that decoded data can be sent to:
```
Cuckoo
Viper
```
For examples of data discovered using pastehunter check out my posts https://techanarchy.net/blog/hunting-pastebin-with-pastehunter and https://techanarchy.net/blog/pastehunter-the-results

If your interested in my thesis or need more information about the work done feel free to contact me. Thanks :)



