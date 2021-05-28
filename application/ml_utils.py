import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder, StandardScaler
import numpy as np


def number_columns(data):
    df_imoveis = data.copy()
    numeric_columns = ["Codigo", "Dormitorios", "Suites",
                       "BanheiroSocialQtd", "Vagas", "AreaPrivativa", "ValorLocacao"]
    for column in numeric_columns:
        df_imoveis[column] = df_imoveis[column].replace(
            '', np.nan).astype(float)

    return df_imoveis


def clean_data(data):
    """Return the a copy of the original dataframe with the
    columns that are in the model and treated for missing values."""
    df_imoveis = number_columns(data)

    columns = ['Finalidade', 'Categoria', 'Dormitorios', 'Suites',
               'BanheiroSocialQtd', 'Vagas', 'AreaPrivativa', 'ValorLocacao',
               'Bairro', 'Caracteristicas', 'DescricaoWeb']
    df_imoveis = df_imoveis[columns]

    df_imoveis['Dormitorios'] = df_imoveis.groupby(
        'Categoria')['Dormitorios'].apply(lambda x: x.fillna(x.median()))
    df_imoveis['Dormitorios'].fillna(0, inplace=True)
    df_imoveis['Suites'] = df_imoveis.groupby(
        'Categoria')['Suites'].apply(lambda x: x.fillna(x.median()))
    df_imoveis['Suites'].fillna(0, inplace=True)
    df_imoveis['BanheiroSocialQtd'].fillna(0, inplace=True)
    df_imoveis['Vagas'].fillna(0, inplace=True)
    df_imoveis['AreaPrivativa'] = df_imoveis.groupby(
        'Categoria')['AreaPrivativa'].apply(lambda x: x.fillna(x.mean()))
    df_imoveis['AreaPrivativa'].fillna(0, inplace=True)
    df_imoveis['Caracteristicas'].fillna('', inplace=True)
    df_imoveis['DescricaoWeb'].fillna('', inplace=True)

    return df_imoveis


def transform_data(data):
    """Return the dataframe with categorical columns
    encoded with label encoder and numerical columns standardized."""
    df_imoveis = clean_data(data)

    le = LabelEncoder()
    categorical_columns = ['Finalidade', 'Categoria', 'Bairro']
    for column in categorical_columns:
        df_imoveis[column] = le.fit_transform(df_imoveis[column])
    sc = StandardScaler()
    numerical_columns = ['AreaPrivativa', 'Bairro']
    df_imoveis[numerical_columns] = sc.fit_transform(
        df_imoveis[numerical_columns])

    return df_imoveis


def stack_data(data):
    """Return the matrix that contain the similarity score between items.
    It have been used the tfidf vectorizer in order to work with text data.
    The metric that have been chosen it is cosine similarity."""
    df_imoveis = transform_data(data)

    title_metadescription = df_imoveis['DescricaoWeb']
    title_comodidades = df_imoveis['Caracteristicas']
    df_imoveis.drop(['DescricaoWeb', 'Caracteristicas'],
                    axis=1, inplace=True)
    nltk.download('stopwords')
    stopwords = nltk.corpus.stopwords.words('portuguese')
    title_vec = TfidfVectorizer(
        min_df=2, ngram_range=(1, 3), stop_words=stopwords)
    title_vec2 = TfidfVectorizer(
        min_df=2, ngram_range=(1, 1), stop_words=stopwords)
    title_bow_metadescription = title_vec.fit_transform(title_metadescription)
    title_bow_comodidades = title_vec2.fit_transform(title_comodidades)
    Xtrain_wtitle = hstack(
        [df_imoveis, title_bow_metadescription, title_bow_comodidades])
    nearest_neighbor = cosine_similarity(Xtrain_wtitle, Xtrain_wtitle)

    return nearest_neighbor


def recommend(id_, conteudo, quantity_similar_items):
    """Return the original df with the most similar
    items in descending order."""
    nearest_neighbor = stack_data(conteudo)

    columns = ['Codigo', 'Finalidade', 'Categoria', 'Mobiliado', 'Dormitorios',
               'Suites', 'BanheiroSocialQtd', 'Vagas', 'AreaPrivativa',
               'ValorLocacao', 'Bairro', 'Caracteristicas',
               'Score']

    similar_listing_ids = []
    df_original = conteudo
    df_original.reset_index(drop=True, inplace=True)
    try:
        idx = df_original.loc[df_original['Codigo'] == id_].index[0]
    except:
        return None, None
    # creating a Series with the similarity scores in descending order
    score_series = pd.Series(
        nearest_neighbor[idx]).sort_values(ascending=False)
    df_original['Score'] = score_series
    # getting the indexes of the most similar listings
    top_indexes = list(score_series.index)
    # populate the list with the ids of the top matching listings
    # checking if the goal of the rent it's the same
    # excluding if the property it is itself
    for i in top_indexes:
        if df_original['Finalidade'][idx] == df_original['Finalidade'][i] \
                and df_original['Codigo'][idx] != df_original['Codigo'][i]:
            similar_listing_ids.append(i)

    # return the top similar properties and the original property
    return \
        df_original.iloc[similar_listing_ids][0:quantity_similar_items], \
        df_original.iloc[idx]
