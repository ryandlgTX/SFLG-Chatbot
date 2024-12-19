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

def get_response(grade_level, learning_goals):
    """Send user input to the AI model and get a response using the Messages API."""
    client = anthropic.Anthropic(api_key=api_key)  # Pass the API key
    
    # Constructing the refined prompt to exclude additional explanatory content
    user_content = f"""
    ##CONTEXT##
    I'm writing self-assessments for students to reflect on their learning in math. Students will review learning goals and identify their confidence with each goal. The goals are currently written with teachers as the primary audience.
    
    ##OBJECTIVE##
    Please provide:
    Grade level: {grade_level}
    Original learning goals that need revision:
    {learning_goals}
    Convert these into student-friendly "I can" statements that:
    - Begin with "I can" or "I understand"
    - Include a specific example for each goal
    - Maintain mathematical accuracy while using grade-appropriate language
    - Preserve essential mathematical vocabulary (like "denominator", "fraction", "sum", etc.)
    - Replace complex academic language with simpler phrasing while keeping mathematical terms
    - Focus on conceptual understanding rather than procedures
    - Use a consistent format:
      - Main goal in clear, student-friendly language
      - Concrete example indented below, starting with "For example:"
    - Do not include additional explanations or lists at the end; only provide the revised goals.

    ##STYLE##
    Elementary math curriculum developer specializing in student-facing materials
    
    ##TONE##
    Direct "I can/I understand" statements
    Clear and concise
    Focuses on understanding over doing
    Uses proper mathematical vocabulary
    Avoids complex academic language while maintaining mathematical precision
    
    ##AUDIENCE##
    Students at the specified grade level
    
    ##FORMAT##
    Main goal
    For example: [specific concrete example]
    """
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",  # Use a supported model
        system="You are a helpful assistant that converts teacher-focused learning goals into student-friendly self-assessments.",
        messages=[
            {"role": "user", "content": user_content}
        ],
        max_tokens=500,  # Increase token limit for detailed outputs
        stream=False  # Set to False unless streaming output
    )
    # Extract the text content from the response
    return response.content[0].text  # Correctly access the text attribute of the TextBlock

# Streamlit app UI
st.title("Student-Friendly Learning Goals Generator")
st.subheader("Convert teacher-written learning goals into student-friendly language.")

# Grade level dropdown
grade_level = st.selectbox(
    "Select a grade level:",
    [
        "Kindergarten", "Grade 1", "Grade 2", "Grade 3", "Grade 4", 
        "Grade 5", "Grade 6", "Grade 7", "Grade 8", 
        "Algebra 1", "Geometry", "Algebra 2"
    ]
)

# Text input for learning goals
learning_goals = st.text_area("Enter the original learning goals to convert:")

# Generate response
if st.button("Generate"):
    if grade_level and learning_goals:
        with st.spinner("Generating student-friendly learning goals..."):
            try:
                response = get_response(grade_level, learning_goals)
                st.success("Student-Friendly Learning Goals Generated!")
                st.text_area("Generated Learning Goals", value=response, height=400)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please select a grade level and provide learning goals to convert.")
