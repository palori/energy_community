import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
import numpy as np
#%matplotlib inline


###############
# not used!!! #
###############

m_data = pd.read_csv('log/master_th_0_4.csv', index_col=0)
s_data = pd.read_csv('log/slave_1_4.csv', index_col=0)
m_data.fillna(0)
print(m_data.iloc[0])
#print(s_data.iloc[0])

m_data.plot(linestyle='--')
plt.xlabel(u'Time')
plt.ylabel('Actions')
plt.show()

############
# not used #
############