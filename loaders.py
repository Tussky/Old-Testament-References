import pandas as pd


def loader(name):
    return pd.read_pickle(f"./pickles/{name}.pickle")


def load_tisch():
    return loader("tisch")


def load_sept():
    return loader("sept")


def load_similarities():
    return loader("similarities")


def load_references():
    return loader("references")


def load_strong():
    return loader("strongs")


def load_references_naive():
    return loader("references-naive")

def load_munged_references():
    return loader("references2")

def load_bible():
    return loader("bible")

def load_strongs():
    return loader("strongs")

def load_rmac():
    return loader("rmac_df")