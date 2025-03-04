import pandas as pd
from sentence_transformers import SentenceTransformer, util

class Chatbot:
    def __init__(self):
        self.transformer = SentenceTransformer("all-MiniLM-L6-v2")

    def load_dialogs(self, path: str):
        self.dialogs = pd.read_csv(path, sep="\t", names=["question", "response"])
        
        self.questions_list = self.dialogs["question"].to_list()
        # Convert to dictionary
        self.dialogs = self.dialogs.set_index("question")["response"].to_dict()


    def chat(self, input: str) -> str:
        similar_question = self._find_similar_question(input)
        return self._get_response(similar_question)


    def _find_similar_question(self, input: str) -> str:
        embeddings = self.transformer.encode([input] + self.questions_list)
        user_embedding = embeddings[0]
        similarities = util.cos_sim(user_embedding, embeddings[1:])
        best_match_idx = similarities.argmax()
        return self.questions_list[best_match_idx]


    def _get_response(self, question: str) -> str:
        return self.dialogs[question]
