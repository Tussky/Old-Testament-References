# %%
from loaders import load_tisch, load_sept, load_bible, load_references
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from scipy.stats import chisquare

sns.set(style="white", context="paper")

# %%
# load and format data
bible = load_bible()
bible.index = np.arange(len(bible))
references = load_references()

bible_books = bible["book"].unique()
book_map = pd.Series(np.arange(1, len(bible_books) + 1), index=bible_books)
bible["booknum"] = book_map[bible["book"]].values

references["obook"] = bible.iloc[references["ostart"]]["book"].values
references["nbook"] = bible.iloc[references["nstart"]]["book"].values

ot = bible.query("booknum < 40").copy()
nt = bible.query("booknum >= 40").copy()

ot_books = pd.Series(ot["book"].unique())
ot_books.index = ot_books
nt_books = pd.Series(nt["book"].unique())
nt_books.index = nt_books

# mark each word with a boolean flag indicating if it's an OT quotation
# additionally mark each word with a boolean flag for each OT book
nt["reference_text"] = False
ot["reference_text"] = False
for obook in ot_books:
    nt[f"reference_{obook}"] = False

for ostart, oend, nstart, nend in references[
    ["ostart", "oend", "nstart", "nend"]
].values:
    nt.loc[nstart : nend - 1, "reference_text"] = True
    ot.loc[ostart : oend - 1, "reference_text"] = True
    obook = ot.iloc[ostart]["book"]
    nt.loc[nstart : nend - 1, f"reference_{obook}"] = True

# calculate which books use which books how much
use_counts = (
    nt.groupby("book")
    .apply(
        lambda book: ot_books.apply(lambda obook: book[f"reference_{obook}"].sum()),
        include_groups=False,
    )
    .reindex(nt_books, columns=ot_books)
    .fillna(0)
    .astype(int)
)
total_quoted = nt.groupby("book")["reference_text"].sum().loc[use_counts.index]
book_lens = nt["book"].value_counts().loc[use_counts.index]
use_props = use_counts / book_lens.values[:, None]
total_props = total_quoted / book_lens.values
use_percents = (use_props * 100).round(2).astype(str) + "%"
use_percents.to_clipboard()

# calculate the logarithm of proportions, for better spacing
flat_props = use_props.values.flatten()
minv = flat_props[flat_props != 0].min()
logged_props = np.log(use_props + minv)

# %%
ax = total_props[::-1].plot.barh(ylabel="", xlabel="Proportion quote")

# %%
(use_counts / len(nt)).T.sum(axis=1)[::-1].plot.barh(ylabel="")


# %%
def plot(logged_props, books, **kwargs):
    with sns.axes_style("white"):
        pca = PCA(n_components=2)
        new_comps = pca.fit_transform(logged_props)
        print(pca.explained_variance_ratio_.sum())

        new_df = pd.DataFrame(data=new_comps, columns=["x", "y"])
        new_df["book"] = books
        new_df = new_df[["book", "x", "y"]]

        ax = sns.scatterplot(new_df, x="y", y="x", **kwargs)
        # for x, y, book in new_df[["x", "y", "book"]].values:
        #    ax.annotate(book, (y, x))
        sns.despine()
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.figure.set_size_inches(6, 6)
        return ax


# %%
from sklearn.cluster import AgglomerativeClustering

hcnt = AgglomerativeClustering(n_clusters=3, metric="euclidean", linkage="ward")
labelsnt = "NT" + pd.Series(hcnt.fit_predict(logged_props) + 1, index=nt_books).astype(
    str
)
hcot = AgglomerativeClustering(n_clusters=3, metric="euclidean", linkage="ward")
labelsot = "OT" + pd.Series(
    hcot.fit_predict(logged_props.T) + 1, index=ot_books
).astype(str)

# %%
ax = plot(logged_props, nt_books.values, hue=labelsnt.values, hue_order=["NT1", "NT2"])
plt.tight_layout()
ax.figure.savefig("nt-clusters.png")
# ax.figure.savefig('../Desktop/nt.png')

# %%
ax = plot(
    logged_props.T,
    ot_books.values,
    hue=labelsot.values,
    hue_order=["OT1", "OT2", "OT3"],
    palette=sns.color_palette("colorblind")[2:5],
)
plt.tight_layout()
ax.figure.savefig("ot-clusters.png")
# ax.figure.savefig('../Desktop/nt.png')

# %%
all_clusters = [
    *ot.groupby(labelsot[ot["book"]].values),
    *nt.groupby(labelsnt[nt["book"]].values),
]
# to be pasted into document
cluster_stats = pd.DataFrame(
    [
        [
            label,
            len(books := contents["book"].unique()),
            word_count := len(contents),
            quote_word_count := contents["reference_text"].sum(),
            (
                cluster_references := references[
                    references["obook"].isin(books) | references["nbook"].isin(books)
                ]
            )["nlen"]
            .mean()
            .round(2),
            len(cluster_references),
            (quote_word_count / word_count * 100).round(2).astype(str) + "%",
        ]
        for label, contents in all_clusters
    ],
    columns=[
        "Cluster",
        "Number of books",
        "Word Count",
        "Total Referenced Words",
        "Mean Reference Length",
        "Number of References",
        "Quotation Density",
    ],
).set_index("Cluster")

# %% [markdown]
# ### What proportion Law, Prophetic, Writing?

# %%
ot_groups = pd.Series(
    {
        "Genesis": "Law",
        "Exodus": "Law",
        "Leviticus": "Law",
        "Numbers": "Law",
        "Deuteronomy": "Law",
        "Joshua": "Prophets",
        "Judges": "Prophets",
        "1 Samuel": "Prophets",
        "2 Samuel": "Prophets",
        "1 Kings": "Prophets",
        "2 Kings": "Prophets",
        "Isaiah": "Prophets",
        "Jeremiah": "Prophets",
        "Ezekiel": "Prophets",
        "Hosea": "Prophets",
        "Joel": "Prophets",
        "Amos": "Prophets",
        "Obadiah": "Prophets",
        "Jonah": "Prophets",
        "Micah": "Prophets",
        "Nahum": "Prophets",
        "Habakkuk": "Prophets",
        "Zephaniah": "Prophets",
        "Haggai": "Prophets",
        "Zechariah": "Prophets",
        "Malachi": "Prophets",
        "Psalms": "Writings",
        "Proverbs": "Writings",
        "Job": "Writings",
        "Song of Solomon": "Writings",
        "Ruth": "Writings",
        "Lamentations": "Writings",
        "Ecclesiastes": "Writings",
        "Esther": "Writings",
        "Daniel": "Writings",
        "Ezra": "Writings",
        "Nehemiah": "Writings",
        "1 Chronicles": "Writings",
        "2 Chronicles": "Writings",
    }
)

# %%
references_by_nt_cluster = references.groupby(labelsnt[references["nbook"]].values)
references_by_ot_cluster = references.groupby(labelsot[references["obook"]].values)
references_by_ot_group = references.groupby(ot_groups[references["obook"]].values)

# %%
fig, axes = plt.subplots(ncols=2, sharey=True)

for ax, (label, cluster_references) in zip(axes, references_by_nt_cluster):
    ax.set_title(label)
    ot_group_props = ot_groups[cluster_references["obook"]].value_counts()
    ot_group_props[["Law", "Prophets", "Writings"]].plot.bar(
        ax=ax, ylabel="# of Quotations"
    )

fig.suptitle("Groups used in New Testament references")
fig.tight_layout()

# %%
fig, axes = plt.subplots(ncols=2)

for ax, (label, cluster_references) in zip(
    axes, references.groupby(labelsnt[references["nbook"]].values)
):
    ax.set_title(label)
    ot_cluster_props = labelsot[cluster_references["obook"]].value_counts()[
        ["OT1", "OT2", "OT3"]
    ]
    ot_cluster_props.index += " (" + ot_cluster_props.astype(str) + ")"
    ot_cluster_props.plot.pie(
        ax=ax, ylabel="", colors=sns.color_palette("colorblind")[2:5]
    )

fig.set_size_inches(4.5, 2.5)
fig.tight_layout()
fig.savefig("OT use in NT clusters.png")

# %%
fig, axes = plt.subplots(ncols=2, nrows=2)
axes[1, 1].set_axis_off()
axes = axes.flatten()[:3]

for ax, (label, cluster_references) in zip(axes, references_by_ot_cluster):
    ax.set_title(label)
    nt_cluster_props = labelsnt[cluster_references["nbook"]].value_counts()[
        ["NT1", "NT2"]
    ]
    nt_cluster_props.index += " (" + nt_cluster_props.astype(str) + ")"
    nt_cluster_props.plot.pie(ax=ax, ylabel="")

fig.set_size_inches(5, 3.5)
fig.tight_layout(rect=(0.02, 0.01, 0.99, 0.99))
fig.savefig("NT use in OT clusters.png")

# %%
reference_counts_by_ot_group = (
    references.groupby(ot_groups[references["obook"]].values)["obook"]
    .value_counts()
    .unstack()
)
reference_counts_by_ot_group["Song of Solomon"] = 0
ax = (
    reference_counts_by_ot_group[ot_books]
    .T[["Law", "Prophets", "Writings"]][::-1]
    .plot.barh(stacked=True, ylabel="", color=sns.color_palette("colorblind")[5:8])
)
ax.figure.set_size_inches(6.5, 6)
ax.figure.tight_layout()
ax.figure.savefig("OT books colored by group.png")

# %%
reference_counts_by_nt_cluster = (
    references.groupby(labelsnt[references["nbook"]].values)["obook"]
    .value_counts()
    .unstack()
)
reference_counts_by_nt_cluster["Song of Solomon"] = 0
ax = (
    reference_counts_by_nt_cluster[ot_books]
    .T[["NT1", "NT2"]][::-1]
    .plot.barh(stacked=True, ylabel="", color=sns.color_palette("colorblind")[:2])
)
ax.figure.set_size_inches(6.5, 6)
ax.figure.tight_layout()
ax.figure.savefig("OT books colored by NT cluster.png")

# %%
reference_counts_by_ot_cluster = (
    references.groupby(labelsot[references["obook"]].values)["nbook"]
    .value_counts()
    .unstack()
)
reference_counts_by_ot_cluster[["Titus", "Philemon", "3 John"]] = 0
ax = (
    reference_counts_by_ot_cluster[nt_books]
    .T[["OT1", "OT2", "OT3"]][::-1]
    .plot.barh(stacked=True, ylabel="", color=sns.color_palette("colorblind")[2:5])
)
ax.figure.set_size_inches(6.5, 6)
ax.figure.tight_layout()
ax.figure.savefig("NT books colored by OT cluster.png")


# %%
def to_hex(color):
    """
    Used to conditionally format cluster table in google sheets
    """
    return "#" + "".join(
        f"{int(channel * 255):02x}"
        for channel in sns.color_palette("colorblind")[color]
    )
