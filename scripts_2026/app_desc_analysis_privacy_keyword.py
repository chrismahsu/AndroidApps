import pandas as pd
import re

df24 = pd.read_parquet("english_apps_2024.parquet")
df26 = pd.read_parquet("english_apps_2026.parquet")

# Privacy Index keywords
PRI_TERMS = [
    "privacy",
    "private",
    "secure",
    "security",
    "safe",
    "protected",
    "protection",
    "encrypted",
    "encryption",
    "trusted",
    "reliable",
    "policy",
    "policies",
    "terms",
    "consent",
    "compliance",
    "data protection",
    "personal data"
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
df24["pri_count"] = (
    df24["app_description"]
    .apply(
        lambda x:
        keyword_count(x, PRI_TERMS)
    )
)

df26["pri_count"] = (
    df26["app_description"]
    .apply(
        lambda x:
        keyword_count(x, PRI_TERMS)
    )
)

print(
    df24["pri_count"].mean()
)

print(
    df26["pri_count"].mean()
)

# Normalized frequency
pri24 = df24["pri_count"].sum()
pri26 = df26["pri_count"].sum()

words24 = df24["word_count"].sum()
words26 = df26["word_count"].sum()

print(
    "Privacy terms per 10k words (2024):",
    pri24 / words24 * 10000
)

print(
    "Privacy terms per 10k words (2026):",
    pri26 / words26 * 10000
)