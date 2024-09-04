import streamlit as st
import openai

# Show title and description.
st.title("📄 Document question answering")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")

# Validate the API key immediately after it's entered.
if openai_api_key:
    try:
        # Use a simple API call to validate the key.
        openai.api_key = openai_api_key
        openai.Model.list()  # Simple call to check if the API key is valid.
        st.success("API key is valid!", icon="✅")
    except Exception as e:  # General exception handling
        st.error(f"Invalid API key or an error occurred: {str(e)}", icon="❌")

# Only continue if the API key is valid.
if openai_api_key:
    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:

        # Process the uploaded file and question.
        document = uploaded_file.read().decode()
        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
            }
        ]

        # Generate an answer using the OpenAI API.
        stream = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Use the model you need.
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)
