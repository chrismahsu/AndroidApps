import pandas as pd
import re
from scipy.stats import ttest_ind

df24 = pd.read_parquet("english_apps_2024.parquet")
df26 = pd.read_parquet("english_apps_2026.parquet")

# AI keywords
AI_TERMS = [
    "ai",
    "artificial intelligence",
    "machine learning",
    "generative",
    "assistant",
    "chatbot",
    "smart",
    "intelligent",
    "automated",
    "automation",
    "recommendation",
    "recommendations",
    "prediction",
    "insights",
    "recognition",
    "personalized",
    "tailored",
    "powered"
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
df24["ai_count"] = (
    df24["app_description"]
    .apply(
        lambda x:
        keyword_count(x, AI_TERMS)
    )
)

df26["ai_count"] = (
    df26["app_description"]
    .apply(
        lambda x:
        keyword_count(x, AI_TERMS)
    )
)

print(
    df24["ai_count"].mean()
)

print(
    df26["ai_count"].mean()
)

# Normalized frequency
ai24 = df24["ai_count"].sum()
ai26 = df26["ai_count"].sum()

words24 = df24["word_count"].sum()
words26 = df26["word_count"].sum()

print(
    "AI terms per 10k words (2024):",
    ai24 / words24 * 10000
)

print(
    "AI terms per 10k words (2026):",
    ai26 / words26 * 10000
)