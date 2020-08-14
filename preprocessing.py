__author__ = "Karthick Thambidurai"
__status__ = "Prototype"
import pandas as pd
import re
import nltk
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords


def preprocess(df):
    try:
        # lowercasing
        df['paste'] = df['paste'].str.lower()
        # Remove stopwords
        words = set(stopwords.words('english'))
        df['paste'].apply(lambda x: [item for item in x if item not in words])
        # Replace multiple characters occurences that are common by single
        df['paste'] = [re.sub(r'[-]+', '-', str(x)) for x in df['paste']]
        df['paste'] = [re.sub(r'[=]+', '=', str(x)) for x in df['paste']]
        df['paste'] = [re.sub(r'[:]+', ':', str(x)) for x in df['paste']]
        df['paste'] = [re.sub(r'[;]+', ';', str(x)) for x in df['paste']]
        df['paste'] = [re.sub(r'[.]+', '.', str(x)) for x in df['paste']]

        # Email followed by a md5 hash
        df['paste'] = [
            re.sub(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\s?[;:]\s?)+\b[a-fA-F\d]{32}\b', 'emailmhash',
                   str(x)) for x in df['paste']]
        # Email followed by a sha1 hash
        df['paste'] = [
            re.sub(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+\s?[;:]\s?)+\b([a-f0-9]{40})\b', 'emailshash',
                   str(x)) for x in df['paste']]
        # Email followed by a bcrypt hash
        df['paste'] = [
            re.sub(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+\s?[;:]\s?)+\$2[aby]?\$\d{1,2}\$[.\/A-Za-z0-9]{53}',
                   'emailbhash', str(x)) for x in df['paste']]
        # keyword password followed by a md5 hash
        df['paste'] = [re.sub(r'(?i)(\bpassword\s?[;:]\s?)+\b[a-fA-F\d]{32}\b', 'passmhash', str(x)) for x in
                       df['paste']]
        # A md5 hashed username followed by a hashed password
        df['paste'] = [re.sub(r'(\bpassword\s?[;:]\s?)+\b[a-fA-F\d]{32}\b', 'hashmhash', str(x)) for x in df['paste']]

        # Convert all email:password combinations to a unique string so that it can represent a feature
        df['paste'] = [
            re.sub(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\s?)+[:|;]+(\s?[a-zA-Z0-9@:!+=#$%^&*-]{5,20}\b)',
                   'emailpasscombo ', str(x)) for x in df['paste']]
        # Convert all email adresses apart from the email:pass combination into a common word EmailOnly
        df['paste'] = [re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', 'emailonly ', str(x)) for x in
                       df['paste']]

        # Replace strings that appear after usernames and passwords
        df['paste'] = [re.sub(r'(?i)(\bUsername\s*[:;]\s*)\S+', r'\1usernameonly ', str(x)) for x in df['paste']]
        df['paste'] = [re.sub(r'(?i)(\bUname\s*[:;]\s*)\S+', r'\1usernameonly', str(x)) for x in df['paste']]
        df['paste'] = [re.sub(r'(?i)(\bPassword\s*[:;]\s*)\S+', r'\1passwordnly', str(x)) for x in df['paste']]
        df['paste'] = [re.sub(r'(?i)(\bpass\s*[:;]\s*)\S+', r'\1passwordonly', str(x)) for x in df['paste']]
        df['paste'] = [re.sub(r'(?i)(\bpwd\s*[:;]\s*)\S+', r'\1passwordonly', str(x)) for x in df['paste']]

        # Replace different types of hashes found to generic terms
        df['paste'] = [re.sub(r'\b[a-fA-F\d]{32}\b', 'mdfivehash', str(x)) for x in df['paste']]
        df['paste'] = [re.sub(r'\b([a-f0-9]{40})\b', 'shaonehash', str(x)) for x in df['paste']]
        df['paste'] = [re.sub(r'\b[A-Fa-f0-9]{64}\b', 'shatwohash', str(x)) for x in df['paste']]
        df['paste'] = [re.sub(r'\$2[aby]?\$\d{1,2}\$[.\/A-Za-z0-9]{53}', 'bcrypthash', str(x)) for x in df['paste']]

        # Remove URL's
        df['paste'] = [re.sub(r'http\S+', ' ', str(x)) for x in df['paste']]

        # A final preprocessing to remove remaining special characters
        df['paste'] = [re.sub(r'[^a-zA-Z]+', ' ', str(x)) for x in df['paste']]
        df['paste'] = [re.sub('\s+', ' ', str(x)) for x in df['paste']]
        df['paste'] = df['paste'].map(lambda x: ' '.join(word for word in x.split() if len(word) > 1))
    except Exception as e:
        print("Exception occured while preprocessing data"+e.message)



