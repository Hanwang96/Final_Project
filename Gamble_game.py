import pandas as pd

df = pd.DataFrame({'a':[1,2,3],'b':[1,2,3]})
new = df[df["b"]<2]
print(new)