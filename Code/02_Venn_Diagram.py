import pandas as pd
import venn
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
data = pd.read_excel("Articles.xlsx" , engine = "openpyxl", sheet_name="Relevant")

sns.set_palette("colorblind")
mpl.rcParams['font.size'] = 16
mpl.rcParams["font.family"] = "calibri"

cm = 1/2.54
gs = set()
ieee = set()
scopus = set()
wos = set()

for index, row in data.iterrows():
    if row["GOOGLE SCHOLAR"] == 1:
        gs.add(index)
    if row["IEEE XPLORE"] == 1:
        ieee.add(index)
    if row["SCOPUS"] == 1:
        scopus.add(index)
    if row["WEB OF SCIENCE"] == 1:
        wos.add(index)

fig, ax1 = plt.subplots(1, 1,  figsize=(6*cm, 6*cm))

labels = venn.get_labels([gs, ieee, scopus, wos], fill=['number', 'logic'])
labels_new = {}
for label in list(labels):
    item = labels[label][6:]
    
    item = item[:-1]
    labels_new[label] = item

fig, ax = venn.venn4(labels_new, names=['Google Scholar', 'IEEE Xplore', 'Scopus', 'Web of Science'], fontsize = 16, dpi=1600)
plt.savefig("Venn_Diagram.png", dpi=1600)
plt.savefig("Venn_Diagram.svg", format='svg', dpi=1600)
fig.show()