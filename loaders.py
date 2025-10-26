import pandas as pd
import numpy as np 

def loader(name):
    return pd.read_pickle(f"./pickles/{name}.pickle")


def load_tisch():
    return loader("tisch")

def load_sept():
    return loader("sept")

def load_similarities():
    return loader("similarities")

def load_references_naive():
    return loader("references-naive.pickle")