import pandas as pd
import utils
df = pd.read_excel('emissivity_data.xlsx')

x=utils.get_emissivity(150)
print(x)

