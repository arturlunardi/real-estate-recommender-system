import pandas as pd
import numpy as np
import json
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack, vstack
from sklearn.metrics.pairwise import cosine_similarity
from run_backend import *
from sklearn.preprocessing import LabelEncoder, StandardScaler


def clean_data(data):

    df_imoveis = data.copy()
    colunas = ['tipo', 'subtipo', 'mobiliado', 'dormitorios', 'suites', 'banheiros', 'garagens', 'area_total', 
    'valor_locacao', 'endereco_bairro', 'meta_description', 'imovel_comodidades']
    df_imoveis = df_imoveis[colunas]

    df_imoveis['dormitorios'].fillna(0, inplace=True)
    df_imoveis['suites'].fillna(0, inplace=True)
    df_imoveis['banheiros'].fillna(0, inplace=True)
    df_imoveis['area_total'] = df_imoveis.groupby('subtipo')['area_total'].apply(lambda x: x.fillna(x.mean()))
    df_imoveis['area_total'].fillna(0, inplace=True)
    df_imoveis['meta_description'].fillna('', inplace=True)
    df_imoveis['imovel_comodidades'].fillna('', inplace=True)

    return df_imoveis


def transform_data(data):

    df_imoveis = clean_data(data)

    le = LabelEncoder()
    colunas = ['tipo', 'subtipo', 'endereco_bairro']
    for column in colunas:
        df_imoveis[column] = le.fit_transform(df_imoveis[column])
    
    sc = StandardScaler()
    colunas = ['area_total', 'valor_locacao', 'endereco_bairro']
    df_imoveis[colunas] = sc.fit_transform(df_imoveis[colunas])

    df_imoveis['valor_locacao'] = df_imoveis['valor_locacao'] * 50

    return df_imoveis

    
def stack_data(data):

    df_imoveis = transform_data(data)

    title_metadescription = df_imoveis['meta_description']
    title_comodidades = df_imoveis['imovel_comodidades']

    df_imoveis.drop(['meta_description', 'imovel_comodidades'], axis=1, inplace=True)

    nltk.download('stopwords')
    stopwords = nltk.corpus.stopwords.words('portuguese')

    title_vec = TfidfVectorizer(min_df=2, ngram_range=(1,3), stop_words=stopwords)
    title_vec2 = TfidfVectorizer(min_df=2, ngram_range=(1,1), stop_words=stopwords)
    title_bow_metadescription = title_vec.fit_transform(title_metadescription)
    title_bow_comodidades = title_vec2.fit_transform(title_comodidades)

    Xtrain_wtitle = hstack([df_imoveis, title_bow_metadescription, title_bow_comodidades])

    nearest_neighbor = cosine_similarity(Xtrain_wtitle, Xtrain_wtitle)

    return nearest_neighbor


def recommend(id_, conteudo):

    nearest_neighbor = stack_data(conteudo)
        
    similar_listing_ids = []

    df_original = conteudo

    df_original.reset_index(drop=True, inplace=True)
    
    idx = df_original.loc[df_original['codigo'] == id_].index[0]
    
    # getting the index of the listing that matches the name
    # idx = indices[indices == id_].index[0]
    
    #creating a Series with the similarity scores in descending order
    score_series = pd.Series(nearest_neighbor[idx]).sort_values(ascending=False)
    
    # getting the indexes of the 20 most similar listings except itself
    top_10_indexes = list(score_series.iloc[0:51].index)
    
    # population the list with the names of the top 10 matching listings
    # if the tipo of the id(index) = tipo of the id similar(iloc)
    for i in top_10_indexes:
        if df_original['tipo'][idx] == df_original['tipo'][i] and df_original['codigo'][idx] != df_original['codigo'][i]:
            similar_listing_ids.append(i)
        
    return df_original.iloc[similar_listing_ids][['codigo', 'tipo', 'subtipo', 'mobiliado', 'dormitorios', 'suites', 
                                                  'banheiros', 'garagens', 'area_total', 'valor_locacao', 'endereco_bairro', 'imovel_comodidades']][0:3]#, df_original.shape

