import os
import pandas as pd
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer, util

KB_PATH = os.path.join(os.path.dirname(__file__), '..', 'kb', 'kb.csv')
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')

def load_kb():
    df = pd.read_csv(KB_PATH)
    df.fillna('', inplace=True)
    return df

def build_or_load_embeddings(rebuild=False):
    os.makedirs(MODEL_DIR, exist_ok=True)
    emb_path = os.path.join(MODEL_DIR, 'embeddings.npy')
    model_path = os.path.join(MODEL_DIR, 'embed_model.pkl')

    df = load_kb()

    # Jika sudah ada model dan embedding, muat ulang saja
    if (not rebuild) and os.path.exists(emb_path) and os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        embeddings = np.load(emb_path)
        return df, model, embeddings

    # Load model multilingual
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

    # Encode semua pertanyaan di knowledge base
    embeddings = model.encode(df['question'].tolist(), convert_to_numpy=True, normalize_embeddings=True)

    # Simpan ke file
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    np.save(emb_path, embeddings)

    return df, model, embeddings

def search_query(query, df, model, embeddings, top_k=3):
    # Encode query
    query_emb = model.encode([query], convert_to_numpy=True, normalize_embeddings=True)

    # Hitung cosine similarity
    sims = np.dot(embeddings, query_emb.T).squeeze()
    top_idx = np.argsort(-sims)[:top_k]

    results = []
    for idx in top_idx:
        results.append({
            'question': df.iloc[idx]['question'],
            'answer': df.iloc[idx]['answer'],
            'score': float(sims[idx])
        })
    return results