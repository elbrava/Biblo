import pandas as pd

df = pd.DataFrame()
p = pd.read_html("https://biblehub.com/timeline/#complete")
print(p[-1].head())
p[-1].to_csv("2.csv", index=False)
p[-2].to_csv("1.csv", index=False)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
