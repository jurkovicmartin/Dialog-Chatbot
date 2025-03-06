import pandas as pd
from sentence_transformers import SentenceTransformer, util

class Chatbot:
    def __init__(self):
        """Dialog based chatbot.
        """
        # Loading pretrained transforming model
        self.transformer = SentenceTransformer("all-MiniLM-L6-v2")

    def load_dialogs(self, path: str):
        """Load dialogs. Expected form: question \t response (\t as a separator)

        Args:
            path (str): path to the dialogs
        """
        self.dialogs = pd.read_csv(path, sep="\t", names=["question", "response"])
        
        self.questions_list = self.dialogs["question"].to_list()
        # Convert to dictionary (question as a key and response as a value)
        self.dialogs = self.dialogs.set_index("question")["response"].to_dict()
        # Encoding into numerical vectors
        self.embeddings = self.transformer.encode(self.questions_list)


    def chat(self, input: str) -> str:
        """Chat with model.

        Args:
            input (str): input question

        Returns:
            str: response
        """
        # Find the most similar question to determine the response
        question = self._find_similar_question(input)
        return self.dialogs[question]


    def _find_similar_question(self, input: str) -> str:
        """Finds the most similar question to the input one within the questions list from dialogs.

        Args:
            input (str): question

        Returns:
            str: the most similar question
        """
        
        # User's input
        user_embedding = self.transformer.encode(input)
        # Computing cosine similarities between user's input and other questions
        similarities = util.cos_sim(user_embedding, self.embeddings)
        # Getting the index of the most similar question
        best_match_idx = similarities.argmax()

        return self.questions_list[best_match_idx]
