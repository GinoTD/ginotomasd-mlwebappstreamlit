# src/app.py

import streamlit as st
import joblib
import os
import pandas as pd
import re
import numpy as np
from urllib.parse import urlparse

# Load trained model
base_path = os.path.dirname(__file__)
model = joblib.load(os.path.join(base_path, 'ridge_model.pkl'))

# === Feature extraction from raw URL ===
def extract_features(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname if parsed_url.hostname else ""
    path = parsed_url.path if parsed_url.path else ""

    return pd.DataFrame([{
        "nb_dots": url.count('.'),
        "nb_hyphens": url.count('-'),
        "nb_at": url.count('@'),
        "nb_qm": url.count('?'),
        "nb_and": url.count('&'),
        "nb_eq": url.count('='),
        "nb_underscore": url.count('_'),
        "nb_percent": url.count('%'),
        "nb_slash": url.count('/'),
        "nb_colon": url.count(':'),
        "nb_star": url.count('*'),
        "nb_comma": url.count(','),
        "nb_semicolumn": url.count(';'),
        "nb_dollar": url.count('$'),
        "nb_space": url.count(' '),
        "url_length": len(url),
        "hostname_length": len(hostname),
        "path_length": len(path),
        "fd_length": len(hostname.split('.')[0]) if '.' in hostname else 0,
        "tld_length": len(hostname.split('.')[-1]) if '.' in hostname else 0,
        "nb_subdomains": len(hostname.split('.')) - 2 if hostname.count('.') >= 2 else 0,
        "nb_www": url.lower().count("www"),
        "nb_com": url.lower().count("com"),
        "https_token": int("https" in url.lower()),
        "ratio_digits_url": sum(c.isdigit() for c in url) / len(url),
        "ratio_digits_host": sum(c.isdigit() for c in hostname) / len(hostname) if hostname else 0,
        "ratio_letters_url": sum(c.isalpha() for c in url) / len(url),
        "ratio_letters_host": sum(c.isalpha() for c in hostname) / len(hostname) if hostname else 0,
        "punycode": int("xn--" in url),
        "port": int(parsed_url.port) if parsed_url.port else 0,
        "tld_in_path": int(any(ext in path.lower() for ext in ['.com', '.net', '.org'])),
        "tld_in_subdomain": int(any(ext in hostname.lower() for ext in ['.com', '.net', '.org'])),
        "abnormal_subdomain": int(re.match(r"^[a-zA-Z0-9\-\.]+$", hostname) is None),
        "nb_redirection": url.count('//') - 1,
        "nb_external_redirection": int(url.startswith("http") and "//" in url[8:]),
        "domain_in_ip": int(re.match(r"^\d{1,3}(\.\d{1,3}){3}$", hostname) is not None),
        "shortening_service": int(any(x in url.lower() for x in [
            "bit.ly", "goo.gl", "shorte.st", "go2l.ink", "x.co", "ow.ly", 
            "tinyurl", "tr.im", "is.gd", "cli.gs", "yfrog.com", "migre.me", 
            "ff.im", "tiny.cc", "url4.eu", "twit.ac", "su.pr", "twurl.nl", 
            "snipurl.com", "short.to", "BudURL.com", "ping.fm", "post.ly", 
            "Just.as", "bkite.com", "snipr.com", "fic.kr", "loopt.us", 
            "doiop.com", "short.ie", "kl.am", "wp.me", "rubyurl.com", 
            "om.ly", "to.ly", "bit.do", "t.co", "lnkd.in", "db.tt", 
            "qr.ae", "adf.ly", "bitly.com", "cur.lv", "tinyurl.com", 
            "ow.ly", "bit.ly", "ity.im", "q.gs", "is.gd", "po.st", 
            "bc.vc", "twitthis.com", "u.to", "j.mp", "buzurl.com", 
            "cutt.us", "u.bb", "yourls.org", "x.co", "prettylinkpro.com", 
            "scrnch.me", "filoops.info", "vzturl.com", "qr.net", 
            "1url.com", "tweez.me", "v.gd", "tr.im", "link.zip.net"
        ]))
    }])

# === Streamlit UI ===
st.set_page_config(page_title="Spam Link Detector", layout="centered")
st.title("Spam Link Detector")
st.write("Enter a URL to check if it's likely spam or not:")

user_input = st.text_input("🔗 URL")

if st.button("Predict"):
    if user_input:
        features = extract_features(user_input.strip())

        # Reorder columns to match training feature order
        expected_features = [
            'nb_dots', 'nb_hyphens', 'nb_at', 'nb_qm', 'nb_and', 'nb_eq',
            'nb_underscore', 'nb_percent', 'nb_slash', 'nb_colon', 'nb_star',
            'nb_comma', 'nb_semicolumn', 'nb_dollar', 'nb_space', 'url_length',
            'hostname_length', 'path_length', 'fd_length', 'tld_length',
            'nb_subdomains', 'nb_www', 'nb_com', 'https_token', 'ratio_digits_url',
            'ratio_digits_host', 'ratio_letters_url', 'ratio_letters_host',
            'punycode', 'port', 'tld_in_path', 'tld_in_subdomain',
            'abnormal_subdomain', 'nb_redirection', 'nb_external_redirection',
            'domain_in_ip', 'shortening_service'
        ]
        features = features[expected_features]

        prediction = model.predict(features.values)[0]

        if prediction == 1:
            st.error("⚠️ This link is likely **SPAM**.")
        else:
            st.success("✅ This link is likely **SAFE**.")
    else:
        st.warning("Please enter a URL first.")
