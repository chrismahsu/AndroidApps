import pandas as pd
import re
from scipy.stats import ttest_ind

df24 = pd.read_parquet("english_apps_2024.parquet")
df26 = pd.read_parquet("english_apps_2026.parquet")

# social keywords
X_TERMS = [
    "twitter",
    "tweet",
    "facebook",
    "instagram",
    "tiktok",
    "discord",
    "reddit",
    "youtube",
    "x.com",
    "x",
    "facebook.com",
    "instagram.com",
    "youtube.com"
]

# Word counting function
def word_count(text):

    return len(
        re.findall(r"\b[a-zA-Z]+\b", str(text))
    )

# AI keyword counting function
def keyword_count(text, keywords):
    text = str(text).lower()

    total = 0

    for kw in keywords:
        pattern = r"\b" + re.escape(kw.lower()) + r"\b"
        total += len(re.findall(pattern, text))

    return total

# compute word count
df24["word_count"] = (
    df24["app_description"]
    .apply(word_count)
)

df26["word_count"] = (
    df26["app_description"]
    .apply(word_count)
)

# Compute AI keyword frequencies
df24["x_count"] = (
    df24["app_description"]
    .apply(
        lambda x:
        keyword_count(x, X_TERMS)
    )
)

df26["x_count"] = (
    df26["app_description"]
    .apply(
        lambda x:
        keyword_count(x, X_TERMS)
    )
)

print(
    df24["x_count"].mean()
)

print(
    df26["x_count"].mean()
)

# Normalized frequency
x24 = df24["x_count"].sum()
x26 = df26["x_count"].sum()

words24 = df24["word_count"].sum()
words26 = df26["word_count"].sum()

print(
    "Social terms per 10k words (2024):",
    x24 / words24 * 10000
)

print(
    "Social terms per 10k words (2026):",
    x26 / words26 * 10000
)