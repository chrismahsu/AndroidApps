import pandas as pd
import re
from scipy.stats import ttest_ind

df24 = pd.read_parquet("english_apps_2024.parquet")
df26 = pd.read_parquet("english_apps_2026.parquet")

# Marketing-oriented terms
MARKETING_TERMS = [
    "awesome",
    "best",
    "great",
    "powerful",
    "ultimate",
    "easy",
    "simple",
    "premium",
    "exclusive",
    "amazing",
    "personalized",
    "professional",
    "discover",
    "transform",
    "effortless",
    "seamless",
    "intuitive"
]

# Word counting function
def word_count(text):

    return len(
        re.findall(r"\b[a-zA-Z]+\b", str(text))
    )

# Keyword counting function
def keyword_count(text, keywords):

    text = str(text).lower()

    total = 0

    for kw in keywords:
        pattern = r"\b" + re.escape(kw.lower()) + r"\b"
        total += len(re.findall(pattern, text))

    return total

# count
df24["marketing_count"] = (
    df24["app_description"]
    .apply(
        lambda x:
        keyword_count(
            x,
            MARKETING_TERMS
        )
    )
)

df26["marketing_count"] = (
    df26["app_description"]
    .apply(
        lambda x:
        keyword_count(
            x,
            MARKETING_TERMS
        )
    )
)

# compute word count
df24["word_count"] = (
    df24["app_description"]
    .apply(word_count)
)

df26["word_count"] = (
    df26["app_description"]
    .apply(word_count)
)

# compare
print(
    "2024:",
    df24["marketing_count"].mean()
)

print(
    "2026:",
    df26["marketing_count"].mean()
)

# Normalized frequency
mkt24 = df24["marketing_count"].sum()
mkt26 = df26["marketing_count"].sum()

words24 = df24["word_count"].sum()
words26 = df26["word_count"].sum()

print(
    mkt24/words24*10000
)

print(
    mkt26/words26*10000
)
