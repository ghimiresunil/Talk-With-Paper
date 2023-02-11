import streamlit as st
from src.paper_parser import Parser
from src.summarizer import Summarize

class Main:
    def __init__(self):
        self.parse = Parser()
        self.summarize = Summarize()
        
    def main(self):
        st.title("📚 Interact with Paper 📚")

        source = ("PDF", "ARXIV LINK")
        source_index = st.sidebar.selectbox(
            "Select Input type", range(len(source)), format_func=lambda x: source[x]
        )

        if source_index == 0:
            uploaded_file = st.sidebar.file_uploader("Load File", type=["pdf"])
            if uploaded_file is not None:
                # Upload pdf file
                with st.spinner(text="Uploading your pdf..."):
                    with open(f"data/pdf/{uploaded_file.name}", mode="wb") as w:
                        w.write(uploaded_file.getvalue())

                total_pages, paper_summary, paper_df = self.summarize.process_file(
                    f"data/pdf/{uploaded_file.name}"
                )
                # paper_df = process_file(f'data/pdf/{uploaded_file.name}')

                st.write(
                    f"<b>Paper Summary of Total Pages: {total_pages} </b><br>",
                    unsafe_allow_html=True,
                )
                st.write(paper_summary, unsafe_allow_html=True)
                st.write("<hr>", unsafe_allow_html=True)

                st.subheader("👇 Talk with Paper 👇")

                text_input = st.text_input(
                    "Ask your paper here and hit enter",
                    # label_visibility='visible',
                    placeholder="Your Question",
                )
                if text_input:
                    print(text_input)
                    results = self.summarize.search(paper_df, text_input, n=3)
                    print(results.iloc[0][0])
                    st.write(results.iloc[0][0])
        else:
            text_input = st.sidebar.text_input(
                "Enter your arxiv Link here 👇",
                # label_visibility='visible',
                placeholder="Arvix Link",
            )

            if text_input:
                st.sidebar.write("You entered: ", text_input)
                with st.spinner(text="Procesing your link..."):
                    self.parse.download_arxiv(text_input)

                total_pages, paper_summary, paper_df = self.summarize.process_file(
                    "data/pdf/download_paper.pdf"
                )

                st.write(
                    f"<b>Paper Summary of Total Pages: {total_pages} </b><br>",
                    unsafe_allow_html=True,
                )
                st.write(paper_summary, unsafe_allow_html=True)
                st.write("<hr>", unsafe_allow_html=True)

                st.subheader("👇 Talk with Paper 👇")

                text_input = st.text_input(
                    "Ask your paper here and hit enter 👇",
                    # label_visibility='visible',
                    placeholder="Your Question",
                )
                if text_input:
                    print(text_input)
                    results = self.summarize.search(paper_df, text_input, n=3)
                    st.write(results.iloc[0][0] + ".")

if __name__ == '__main__':
    summrize = Main()
    summrize.main()