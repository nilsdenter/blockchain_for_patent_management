import pandas as pd

data = pd.read_excel("Articles.xlsx" , engine = "openpyxl", sheet_name="Relevant")

x_variable = list(set(data["PUBL. YEAR"]))


"""
ADDRESSING WHICH 7D PMMM DIMENSION?
"""


GENERATION = []
GENERATION_data = data[data["GENERATION"]==1]
for year in x_variable:
    try:
        df = GENERATION_data[GENERATION_data["PUBL. YEAR"]==year]
        GENERATION.append(df.shape[0])
    except:
        GENERATION.append(0)
        
        
ENFORCEMENT = []
ENFORCEMENT_data = data[data["ENFORCEMENT"]==1]
for year in x_variable:
    try:
        df = ENFORCEMENT_data[ENFORCEMENT_data["PUBL. YEAR"]==year]
        ENFORCEMENT.append(df.shape[0])
    except:
        ENFORCEMENT.append(0)

EXPLOITATION = []
EXPLOITATION_data = data[data["EXPLOITATION"]==1]
for year in x_variable:
    try:
        df = EXPLOITATION_data[EXPLOITATION_data["PUBL. YEAR"]==year]
        EXPLOITATION.append(df.shape[0]) 
    except:
        EXPLOITATION.append(0)
        
INTELLIGENCE = []
INTELLIGENCE_data = data[data["INTELLIGENCE"]==1]
for year in x_variable:
    try:
        df = INTELLIGENCE_data[INTELLIGENCE_data["PUBL. YEAR"]==year]
        INTELLIGENCE.append(df.shape[0]) 
    except:
        INTELLIGENCE.append(0)

ORGANIZATION = []
ORGANIZATION_data = data[data["ORGANIZATION"]==1]
for year in x_variable:
    try:
        df = ORGANIZATION_data[ORGANIZATION_data["PUBL. YEAR"]==year]
        ORGANIZATION.append(df.shape[0]) 
    except:
        ORGANIZATION.append(0)
        
CULTURE = []
CULTURE_data = data[data["CULTURE"]==1]
for year in x_variable:
    try:
        df = CULTURE_data[CULTURE_data["PUBL. YEAR"]==year]
        CULTURE.append(df.shape[0]) 
    except:
        CULTURE.append(0)



import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
sns.set_palette("colorblind")
mpl.rcParams['font.size'] = 8
mpl.rcParams["font.family"] = "arial"
cm = 1/2.54

"""
WHICH ARTICLE TYPE?
"""


df = data[data["TYPE"]=="Book Chapter"]
book_chapter = [df[df["PUBL. YEAR"]==year].shape[0] for year in x_variable]

df = data[data["TYPE"]=="Conference Paper"]
conference_paper = [df[df["PUBL. YEAR"]==year].shape[0] for year in x_variable]

df = data[data["TYPE"]=="Grey Literature"]
grey_literature = [df[df["PUBL. YEAR"]==year].shape[0] for year in x_variable]

df = data[data["TYPE"]=="Journal Article"]
journal_article = [df[df["PUBL. YEAR"]==year].shape[0] for year in x_variable]

"""
ADDRESSING WHICH BLOCKCHAIN ARCHITECTURE?
"""

df = data[data['PUBLIC PERMISSIONLESS']==1]
public_permissionless = [df[df["PUBL. YEAR"]==year].shape[0] for year in x_variable]

df = data[data['PUBLIC PERMISSIONED']==1]
public_permissioned = [df[df["PUBL. YEAR"]==year].shape[0] for year in x_variable]

df = data[data['PRIVATE PERMISSIONED']==1]
private_permissioned = [df[df["PUBL. YEAR"]==year].shape[0] for year in x_variable]

df = data[data['NONE ARCHITECTURE']==1]
none_architecture = [df[df["PUBL. YEAR"]==year].shape[0] for year in x_variable]


"""
ADDRESSING HOW MANY DIMENSIONS?
"""

number_of_dimensions = {}
num_dimensions = []

for index, row in data.iterrows():
    number = 0
    for dimension in ["GENERATION", "ENFORCEMENT", "EXPLOITATION", "INTELLIGENCE", "ORGANIZATION", "CULTURE"]:
        if str(row[dimension]) == "nan": continue
        else: number += 1
    num_dimensions.append(number)
    if number not in number_of_dimensions:
        number_of_dimensions[number] = 1
    else:
        number_of_dimensions[number] += 1

data["Number_Dimensions_Adressed"] = num_dimensions


df = data[data["Number_Dimensions_Adressed"]==1]
one_dimension = [df[df["PUBL. YEAR"]==year].shape[0] for year in x_variable]

df = data[data["Number_Dimensions_Adressed"]==2]
two_dimensions = [df[df["PUBL. YEAR"]==year].shape[0] for year in x_variable]

df = data[data["Number_Dimensions_Adressed"]==3]
three_dimensions = [df[df["PUBL. YEAR"]==year].shape[0] for year in x_variable]

df = data[data["Number_Dimensions_Adressed"]==4]
four_dimensions = [df[df["PUBL. YEAR"]==year].shape[0] for year in x_variable]

"""
TOP AUTHORS?
"""

author_contributions = {}

for index, row in data.iterrows():
    authors = row["AUTHORS"]
    citation_score = row["#CITATIONS"]
    aac = row["AAC"]
    
    authors = authors.split(", ")
    for author in authors:
        if author not in author_contributions:
            last_name = author.split(" ")
            if len(last_name) > 2 and not isinstance(last_name, str):
                last_name = last_name[-1]
            else: last_name = last_name[1]
            author_contributions[author] = [last_name, 0, 0, 0]
            author_contributions[author][1] = 1
            author_contributions[author][2] = citation_score
            author_contributions[author][3] = aac
            
        else:
            author_contributions[author][1] += 1
            author_contributions[author][2] += citation_score
            author_contributions[author][3] += aac
            

"""
TOP COUNTRIES?
"""

country_contributions = {}
for index, row in data.iterrows():
    countries = row["INSTITUTE LOCATIONS"]
    citation_score = row["#CITATIONS"]
    aac = row["AAC"]
    
    countries = countries.split(", ")
    for country in countries:
        if country not in country_contributions:
            
            country_contributions[country] = 1
            
        else:
            country_contributions[country] += 1

df = pd.DataFrame.from_dict(data=country_contributions, orient="index").rename(columns={0: "No. of observations"})
df.sort_values(by=["No. of observations"], inplace=True, ascending=[False])

total_observations = sum(df["No. of observations"])

share = []
for observation in list(df["No. of observations"]):
    share.append(observation*100/total_observations)

df["Share of total (%)"] = share

df.to_excel("top_countries_by_observations.xlsx")

            
linewidth=0.8
markersize = 2.2
legend_width = 0
legend_height = 0
transparency = 0.8
vlines_width = 20
fig, ax = plt.subplots(2, 2, sharex = True,  figsize=(16*cm, 12*cm))

ax[0,0].grid(color='lightgray', linewidth=0.5, zorder=0)
ax[0,1].grid(color='lightgray', linewidth=0.5, zorder=0)
ax[1,0].grid(color='lightgray', linewidth=0.5, zorder=0)
ax[1,1].grid(color='lightgray', linewidth=0.5, zorder=0)

mpl.rcParams['font.size'] = 8

ax[0,0].plot(x_variable,GENERATION, label="Generation: {0}".format(sum(GENERATION)), color = "black", linestyle="solid", linewidth=linewidth, marker="o", markersize=markersize, zorder=5)
ax[0,0].plot(x_variable,ENFORCEMENT, label="Enforcement: {0}".format(sum(ENFORCEMENT)), color = "black", linestyle="dashed", linewidth=linewidth, marker="o", markersize=markersize, zorder=5)
ax[0,0].plot(x_variable,EXPLOITATION, label="Exploitation: {0}".format(sum(EXPLOITATION)), color = "black", linestyle="dotted", linewidth=linewidth, marker="o", markersize=markersize, zorder=5)
ax[0,0].plot(x_variable,ORGANIZATION, label="Organization: {0}".format(sum(ORGANIZATION)), color = "grey", linestyle="solid", linewidth=linewidth, marker="o", markersize=markersize, zorder=5)
ax[0,0].plot(x_variable,CULTURE, label="Culture: {0}".format(sum(CULTURE)),  color = "grey",linestyle="dashed", linewidth=linewidth, marker="o", markersize=markersize, zorder=5)

ax[0,0].set_xticks(x_variable)
ax[0,0].set_yticks([0,2,4,6,8,10])



ax[1,0].plot(x_variable,journal_article, label="Journal article: {0}".format(sum(journal_article)), color = "black", linestyle="solid", linewidth=linewidth, marker="o", markersize=markersize, zorder=5)
ax[1,0].plot(x_variable,conference_paper, label="Conference paper: {0}".format(sum(conference_paper)), color = "black", linestyle="dashed", linewidth=linewidth, marker="o", markersize=markersize, zorder=5)
ax[1,0].plot(x_variable,grey_literature, label="Grey literature: {0}".format(sum(grey_literature)), color = "grey", linestyle="solid", linewidth=linewidth, marker="o", markersize=markersize, zorder=5)
ax[1,0].plot(x_variable,book_chapter, label="Book chapter: {0}".format(sum(book_chapter)), color = "grey", linestyle="dashed", linewidth=linewidth, marker="o", markersize=markersize, zorder=5)
ax[1,0].set_xlabel("Publication Year", style="italic")

ax[1,1].plot(x_variable,public_permissionless, label="Public permissionless: {0}".format(sum(public_permissionless)), color = "black", linestyle="solid", linewidth=linewidth, marker="o", markersize=markersize, zorder=5)
ax[1,1].plot(x_variable,none_architecture, label="None architecture: {0}".format(sum(none_architecture)), color = "black", linestyle="dashed", linewidth=linewidth, marker="o", markersize=markersize, zorder=5)
ax[1,1].plot(x_variable,private_permissioned, label="Private permissioned: {0}".format(sum(private_permissioned)), color = "grey", linestyle="solid", linewidth=linewidth, marker="o", markersize=markersize, zorder=5)
ax[1,1].plot(x_variable,public_permissioned, label="Public permissioned: {0}".format(sum(public_permissioned)), color = "grey", linestyle="dashed", linewidth=linewidth, marker="o", markersize=markersize, zorder=5)
ax[1,1].set_xlabel("Publication Year", style="italic")



ax[0,1].plot(x_variable,one_dimension, label="One: {0}".format(sum(one_dimension)), color = "black", linestyle="solid", linewidth=linewidth, marker="o", markersize=markersize, zorder=5)
ax[0,1].plot(x_variable,two_dimensions, label="Two: {0}".format(sum(two_dimensions)), color = "black", linestyle="dashed", linewidth=linewidth, marker="o", markersize=markersize, zorder=5)
ax[0,1].plot(x_variable,three_dimensions, label="Three: {0}".format(sum(three_dimensions)), color = "grey", linestyle="solid", linewidth=linewidth, marker="o", markersize=markersize, zorder=5)

#make last year grey
ax[0,0].vlines(x=2020.85, ymin=-.25, ymax=11.25, alpha=transparency, colors="lightgrey", linewidth=vlines_width, zorder=10)
ax[0,1].vlines(x=2020.85, ymin=-.25, ymax=8.25, alpha=transparency, colors="lightgrey", linewidth=vlines_width, zorder=10)
ax[1,0].vlines(x=2020.85, ymin=-.25, ymax=6.25, alpha=transparency, colors="lightgrey", linewidth=vlines_width, zorder=10)
ax[1,1].vlines(x=2020.85, ymin=-.25, ymax=7.25, alpha=transparency, colors="lightgrey", linewidth=vlines_width, zorder=10)

ax[0,0].set_ylim(bottom = -.5, top = 11+.5)
ax[0,1].set_ylim(bottom = -.5, top = 8+.5)
ax[1,0].set_ylim(bottom = -.5, top = 6+.5)
ax[1,1].set_ylim(bottom = -.5, top = 7+.5)


l=ax[0,0].legend(title='7D model dimensions addressed',title_fontsize = 10, loc='center', bbox_to_anchor=(0.5, 1.15,legend_width,legend_height), fancybox=True,  ncol=3, framealpha=0, handlelength=1.5, borderpad=0, labelspacing=.3, handletextpad=0.3, columnspacing=1)
plt.setp(l.get_title(), multialignment='center')

l = ax[0,1].legend(title='No. of 7D model dimensions addressed',title_fontsize = 10, loc='center', bbox_to_anchor=(0.5, 1.15,legend_width,legend_height), fancybox=True,  ncol=2, framealpha=0, handlelength=1.5, borderpad=0, labelspacing=.3, handletextpad=0.3, columnspacing=1)
plt.setp(l.get_title(), multialignment='center')

l=ax[1,0].legend(title='Document type', loc='center',title_fontsize = 10, bbox_to_anchor=(0.5, 1.15, legend_width,legend_height), fancybox=True,  ncol=2, framealpha=0, handlelength=1.5, borderpad=0, labelspacing=.3, handletextpad=0.3, columnspacing=1)
plt.setp(l.get_title(), multialignment='center')

l=ax[1,1].legend(title='Blockchain architecture',title_fontsize = 10, loc='center', bbox_to_anchor=(0.5, 1.15,legend_width,legend_height), fancybox=True,  ncol=2, framealpha=0, handlelength=1.5, borderpad=0, labelspacing=.3, handletextpad=0.3, columnspacing=1)
plt.setp(l.get_title(), multialignment='center')

plt.tight_layout()
plt.savefig("Figure 3.png", dpi=1600)
plt.savefig("Figure 3.svg", format='svg', dpi=1600)
plt.plot()