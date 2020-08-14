# Pastehunter
## Applying a text classification model on the scraped Pastes to predict PII (Only Tested on Pastebin).

###### This research was carried out as part of my Masters Thesis. The developed scripts is a Proof of concept to demonstrate how text classification models along with keywords/Yara rules can aid in identifying PII from pastes.  

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



