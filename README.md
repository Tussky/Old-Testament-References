# Old Testament References
## File structure:
 - depricated

   Contains old notebook files we're no longer using. Mostly word2vec stuff

 - Isaac-Analysis.ipynb

   Code Isaac wrote, mostly to generate information for the presentation

 - loaders.py

   Utility functions to load the pickles we care about, so we don't have to keep typing out the full path every time

 - make-stuff-for-slides.ipynb

   More code to generate information for the presentation. This is seperate from Isaac-Analysis.ipynb mostly so Wes and Isaac wouldn't be committing to the same file all the time

 - old-testament-use.ipynb

   Cluster New Testament books by how the use the Old, and Old Testament books by how they're used in the New. Output used in research paper

 - reference-analysis.ipynb

   Takes references-naive.pickle, does merging and munging, and produces references.pickle and references2.pickle

 - reference_search.ipynb

   Uses all available cores to compare 5-grams in NT to 5-grams in OT, saves to references-naive.ipynb. Takes 8-12 hours to run

 - references-naive.pickle

   Contains saved references, unmerged

 - requirements.txt

   run `pip install -r requirements.txt` in default environment to install requirements

 - rmac_df

   pickle file containing RMAC interpretations

 - SEPTUAGINT.xml
 - TSICHENDORF.xml

 - strongs-dictionary.xhtml

 - themes-clustering.ipynb

   Attempts to cluster Old Testament verses by word use

## Usage
First, `pip install -r requirements.txt` in a new virtual environment. Then run "make-pickles.ipynb" to generate pickles from the xml documents. Then run "reference_search.ipynb" (which takes 8-12 hours), or just don't delete the saved "references-naive.pickle". Then run "reference-analysis.ipynb" to generate "references.pickle" (merged references, indexed by word count into the Bible) and "references2.pickle" (merged references, indexed by verse and chapter number). Then you can run any of the analysis files ("themes-clustering.ipynb", "Isaac-Analysis.ipynb", "make-stuff-for-slides.ipynb", or "old-testament-use.ipynb").

## AI Use:
### Wes
 - https://chatgpt.com/share/690d1dfd-1154-8002-8022-b33be65a9f64
 - https://chatgpt.com/share/68f11049-47c8-8002-b963-bc47264e8b01
 - https://chatgpt.com/share/690d1e79-5718-8002-816f-7710bdaf5a88
 - https://chatgpt.com/share/690d1e89-c04c-8002-a14e-6a05e055468f
 - https://chatgpt.com/share/690d1e9c-5d18-8002-b15c-a13cf0253c7c
 - https://chatgpt.com/share/690d1ea8-5cb4-8002-8cee-0c36d9ce0be5
 - https://chatgpt.com/share/690d1eb3-f400-8002-87b8-ef2946ee4a5c
 - https://chatgpt.com/share/690d1e38-57dc-8002-8c21-46adb7162748
