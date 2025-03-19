from rank_bm25 import BM25Okapi
import numpy as np

class AnnouncementRetriever:
    def __init__(self,elements ,emb_model, korean_tokenizer):
        self.elements = elements
        self.emb_model = emb_model
        self.korean_tokenizer = korean_tokenizer
        
        self.chunks_with_title = [e['title'] + '\n' + e['markdown'] for e in self.elements]
        self.tokenized_chunks = [self.korean_tokenizer.morphs(chunk) for chunk in self.chunks_with_title]
        self.bm25 = BM25Okapi(self.tokenized_chunks)

        self.title_embeddings = np.array([e['title_emb'] for e in elements], dtype=np.float16)
        self.doc_embeddings = np.array([e['doc_emb'] for e in elements], dtype=np.float16)

        self.bm25_weights = 1/3
        self.title_similarity_weights = 1/3
        self.doc_similarity_weights = 1/3

    def get_bm25_scores(self, query):
        tokenized_query = self.korean_tokenizer.morphs(query)
        bm_scores = self.bm25.get_scores(tokenized_query)
        return bm_scores

    def get_similarity(self, query):
        query_embedding = self.emb_model.encode([query])['dense_vecs']

        title_sim = query_embedding @ self.title_embeddings.T
        doc_sim = query_embedding @ self.doc_embeddings.T

        return (title_sim, doc_sim)

    def min_max_normilize(self, scores):
        if scores.max() == scores.min():
            return np.array([0]*len(scores),dtype=np.float16)
        return (scores - scores.min()) / (scores.max() - scores.min())

    def get_rag_scores(self, query):
        bm25_scores = self.get_bm25_scores(query)
        sims = self.get_similarity(query)
        norm_bm25 = self.min_max_normilize(bm25_scores)
        norm_title = self.min_max_normilize(sims[0][0])
        norm_doc = self.min_max_normilize(sims[1][0])
        rag_scores = self.bm25_weights*norm_bm25 + \
                        self.title_similarity_weights*norm_title + \
                        self.doc_similarity_weights*norm_doc
        return rag_scores
    
    def get_retriever_results(self,query):
        rag_scores = self.get_rag_scores(query)
        arg_max_idx = rag_scores.argsort()[::-1]
        total_token_len = 0
        idx_with_order = []
        for idx in arg_max_idx:
            token_len = self.elements[idx]['token_len']
            order = self.elements[idx]['id']
            if total_token_len + token_len > 3000:
                break
            idx_with_order.append([order, idx])
            total_token_len += token_len
        idx_with_order.sort()
        cur_title = ''
        total_md_txt = ''
        for idx in idx_with_order:
            title = self.elements[idx[1]]['title']
            md_txt = self.elements[idx[1]]['markdown']
            if title != cur_title:
                total_md_txt = total_md_txt + '\n' + title + '\n'
                cur_title = title
            total_md_txt = total_md_txt + md_txt + '\n'
        
        return total_md_txt
            
