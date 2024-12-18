from dotenv import load_dotenv
import os
import anthropic
import streamlit as st

# Load environment variables
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# Verify API key
if not api_key:
    st.error("API key not found. Please check your .env file.")
    st.stop()

def get_response(user_content):
    """Send user input to the AI model and get a response using the Messages API."""
    client = anthropic.Anthropic(api_key=api_key)  # Pass the API key
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",  # Use a supported model
        system="You are a helpful assistant that generates student-friendly learning goals.",
        messages=[
            {"role": "user", "content": user_content}
        ],
        max_tokens=300,  # Maximum number of tokens for the response
        stream=False  # Set to False unless streaming output

    )
    # Convert the response object to its textual content
    print(response)
    return response # Extract the generated content

# Streamlit app UI
st.title("Student-Friendly Learning Goals (SFLG) Generator")
st.subheader("Generate learning goals tailored to specific grades and topics.")

# User input
user_input = st.text_input("Enter grade level and topic (e.g., 'Grade 4, Fractions'):")

# Generate response
if st.button("Generate"):
    if user_input:
        with st.spinner("Generating learning goals..."):
            try:
                response = get_response(user_input)
                st.success("Learning Goals Generated!")
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a grade level and topic to generate learning goals.")
