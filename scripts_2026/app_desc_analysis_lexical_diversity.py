import pandas as pd
import re
from scipy.stats import ttest_ind

df24 = pd.read_parquet("english_apps_2024.parquet")
df26 = pd.read_parquet("english_apps_2026.parquet")

# per-app lexical diversity
def lexical_diversity(text):

    words = re.findall(
        r"\b[a-zA-Z]+\b",
        str(text).lower()
    )

    if len(words) == 0:
        return None

    return len(set(words))/len(words)

# compute
df24["lexdiv"] = (
    df24["app_description"]
    .apply(lexical_diversity)
)

df26["lexdiv"] = (
    df26["app_description"]
    .apply(lexical_diversity)
)

# compare
print(
    "2024:",
    df24["lexdiv"].mean()
)

print(
    "2026:",
    df26["lexdiv"].mean()
)

# significance
print(
    ttest_ind(
        df24["lexdiv"].dropna(),
        df26["lexdiv"].dropna(),
        equal_var=False
    )
)

