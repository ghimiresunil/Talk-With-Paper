# Talk with Paper

This project is a user interface (UI) built with Streamlit, which uses embeddings models from OpenAI to read and interact with research papers. You can upload either a PDF file or provide an ArXiv paper link. The app provides the following features:

- Paper Upload: You can upload a PDF file or provide an ArXiv paper link.
- Summarization: The app uses OpenAI models to generate summaries of the papers. You can also use Hugging Face models for summarization.
- Interact with Paper: You can ask questions related to the content of the paper.
  - The app gets chunks of text from the paper and calculates embeddings for each chunk
  - During inference: 
    - You can input a new question
    - The app calculates the embedding for the question.
    - It retrieves the top K similar chunks of text from the paper using cosine similarity

# Usage

To use the app, follow these steps:

- Install the requirements using the following command: 

`pip install -r requirements.txt`

- Create a `.env` file in the project directory with your OpenAI API key. The file should contain the following content:

`OPENAI_API_KEY=YOUR_API_KEY`

- Run the app using the command:

`streamlit run main.py`

Note: Make sure to replace `YOUR_API_KEY` in the `.env` file with your actual OpenAI API key.

This app is ready for deployment and can be used to interact with research papers in a user-friendly way. For more details, refer to the provided notebooks.

Happy exploring and interacting with research papers using this Streamlit app! 📄🔍🔬🚀

Note: Make sure to comply with the terms and conditions of using OpenAI API, and respect the licensing and usage restrictions of the research papers you upload to the app. Please follow ethical guidelines for using and interacting with research papers. Always give proper attribution and follow the guidelines set by the authors and publishers of the research papers. This app is not intended for any unauthorized or unethical use of research papers. Use it responsibly and in compliance with applicable laws and regulations. The developers and contributors of this app are not responsible for any misuse or violation of terms and conditions by users. Use it at your own risk. Thank you! 📚💻😊
