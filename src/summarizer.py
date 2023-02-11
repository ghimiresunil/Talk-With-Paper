import os
import openai
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from src.paper_parser import Parser
from openai.embeddings_utils import get_embedding, cosine_similarity

load_dotenv()

openai.api_key = os.getenv("openai_api_key")


class Summarize:
    def __init__(self):
        self.parser = Parser()
        self.summary_model = "text-davinci-003"
        self.embedding_model = "text-embedding-ada-002"
        self.temperature = 0.6
        self.max_token = 120
        self.top_p = 0.9
        self.frequency = 0.0
        self.presence_penalty = 1

    def search(self, df, query, n=3, pprint=True):
        query_embedding = get_embedding(query, engine="text-embedding-ada-002")
        df["similarity"] = df.embeddings.apply(
            lambda x: cosine_similarity(x, query_embedding)
        )
        results = df.sort_values("similarity", ascending=False)
        return results

    def generate_summary(self, text):
        prompt = "summarize in short: " + text + "\n Tl;dr:"
        response = openai.Completion.create(
            model= self.summary_model,
            prompt=prompt,
            temperature=self.temperature,
            max_tokens=self.max_token,
            top_p=self.top_p,
            frequency_penalty=self.frequency,
            presence_penalty=self.presence_penalty,
        )
        return response["choices"][0]["text"]

    @st.cache(allow_output_mutation=True)
    def process_file(self, file):
        print("[INFO] Processing and calc embeddings")
        # Process the file and filter
        with st.spinner(text="Procesing your paper and generating summary..."):
            doc = self.parser.pdf_to_text(file)
            summary_list = []
            for page in doc:
                text = page.get_text("text", sort=True, flags=16)
                text = self.parser.clean_text(text, False)
                summary_list.append(self.generate_summary(text))
            paper_summary1 = "<br>".join(summary_list)
            paper_summary2 = "".join(summary_list)

            summary_list = paper_summary2.split(". ")
            for i, sentence in enumerate(summary_list):
                summary_list[i] = sentence + ". "
            paper_df = pd.DataFrame(summary_list)

        with st.spinner(text="Calculate embeddings"):
            embeddings = (
                paper_df[0]
                .astype(str)
                .apply([lambda x: get_embedding(x, engine=self.embedding_model)])
            )
            paper_df["embeddings"] = embeddings

        return len(doc), paper_summary1, paper_df
