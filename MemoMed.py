import openai
import speech_recognition as sr
import streamlit as st
from langchain.memory import ChatMessageHistory, ConversationBufferMemory

openai.api_key = 'openai api'

# Initialize the conversation history
conversation_history = ChatMessageHistory()

def transcribe_speech():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak Anything :")
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            print("You said : {}".format(text))
            return text
        except:
            print("Sorry could not recognize your voice")
            return None

def transcribe_audio(audio_file):
    r = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)

    try:
        text = r.recognize_google(audio)
        st.write("Transcript: ", text)
        return text
    except:
        st.write("Sorry, I could not transcribe the file.")
        return None

def generate_notes(transcribed_text):
    template = f"""
    <b>Patient:</b> {transcribed_text}

    <b>Source of Information:</b>
    <b>Date and Time:</b>
    <b>Interpreter/Substitute Decision-Maker:</b>

    <b>Allergies:</b>

    <b>Relevant History and Physical Findings:</b>

    <b>Vital Signs:</b>

    <b>Pertinent Positive/Negative Findings:</b>

    <b>Assessment of Patient Capacity:</b>

    <b>Clinical Assessment:</b>

    <b>Working Diagnosis:</b>
    <b>Differential Diagnosis:</b>
    <b>Final Diagnosis:</b>

    <b>Plan of Action:</b>

    <b>Investigations:</b>
    <b>Consultations:</b>
    <b>Treatment:</b>
    <b>Follow-Up:</b>

    <b>Rationale for the Plan:</b>

    <b>Expectations of Outcomes:</b>

    <b>Medications (Doses and Duration):</b>

    <b>Medication Reconciliation:</b>

    <b>Calls to Consultants:</b>
    <b>Consultant's Name:</b>
    <b>Advice Received:</b>

    <b>Information Given by/to the Patient (or SDM):</b>

    <b>Concerns Raised, Questions Asked, and Responses Given:</b>

    <b>Verification of Patient Understanding:</b>

    <b>Consent Discussion Summary:</b>

    <b>Discharge Instructions:</b>

    <b>Symptoms and Signs that Should Prompt a Reassessment:</b>

    <b>Urgency of Follow Up:</b>

    <b>Where and When to Return:</b>

    <b>Missed Appointments:</b>

    <b>Efforts to Follow Up on Investigation Results:</b>

    <b>Communication with Other Care Providers at Discharge:</b>

    <b>Signature of Writer and Role:</b>

    -End of Note-

    {{
    - The generated note should not include any personally identifiable information (PII) or protected health information (PHI) that could violate privacy laws like HIPAA.
    - The note should be factual and based on the information provided in the transcribed text.
    - The note should not include any speculative or hypothetical information.
    }}
    """
    # Use the OpenAI API to generate the note
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": template},
            {"role": "user", "content": transcribed_text}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

def generate_suggestions(note):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful healthcare assistant that generates suggestions based on medical notes."
        },
        {
            "role": "user",
            "content": note
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    suggestion = response['choices'][0]['message']['content']
    return suggestion

# def chat_with_gpt(prompt, conversation_history):
#     # Add the user's message to the conversation history
#     conversation_history.add_user_message(prompt)
#     # conversation_history.add_ai_message(generated_notes)

#     # Initialize the memory
#     memory = ConversationBufferMemory()

#     # Add the conversation history to the memory
#     memory.chat_memory = conversation_history

#     # Load the memory variables
#     memory_variables = memory.load_memory_variables({})

#     # Use the OpenAI API to generate the response
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[
#             {"role": "system", "content": "You are a helpful healthcare assistant."},
#             {"role": "user", "content": memory_variables['history']}
#         ]
#     )

#     # Add the AI's message to the conversation history
#     conversation_history.add_ai_message(response['choices'][0]['message']['content'])

#     return response['choices'][0]['message']['content']

# def chat_with_gpt(prompt, generated_notes, conversation_history):
#     # Add the generated notes to the conversation history
#     conversation_history.add_system_message(generated_notes)

#     # Add the user's message to the conversation history
#     conversation_history.add_user_message(prompt)

#     # Initialize the memory
#     memory = ConversationBufferMemory()

#     # Add the conversation history to the memory
#     memory.chat_memory = conversation_history

#     # Load the memory variables
#     memory_variables = memory.load_memory_variables({})

#     # Use the OpenAI API to generate the response
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": memory_variables['history']}
#         ]
#     )

#     # Add the AI's message to the conversation history
#     conversation_history.add_ai_message(response['choices'][0]['message']['content'])

#     return response['choices'][0]['message']['content']
def chat_with_gpt(prompt, generated_notes, conversation_history):
    # Add the generated notes to the conversation history
    conversation_history.add_ai_message(generated_notes)

    # Add the user's message to the conversation history
    conversation_history.add_user_message(prompt)

    # Initialize the memory
    memory = ConversationBufferMemory()

    # Add the conversation history to the memory
    memory.chat_memory = conversation_history

    # Load the memory variables
    memory_variables = memory.load_memory_variables({})

    # Use the OpenAI API to generate the response
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": memory_variables['history']}
        ]
    )

    # Add the AI's message to the conversation history
    conversation_history.add_ai_message(response['choices'][0]['message']['content'])

    return response['choices'][0]['message']['content']



# def main():
#     st.title("Medical Assistant App")
#     st.write("This is a prototype of a medical assistant application.")

#     transcript = None
#     note = None
#     suggestion = None
#     chat_history = []

#     # option = st.selectbox(
#     #     'Choose an option',
#     #     ('Transcribe speech', 'Generate notes', 'Generate suggestions', 'Chat with GPT')
#     # )

#     # if option == 'Transcribe speech':
#     #     if st.button("Start Transcription"):
#     #         transcript = transcribe_speech()
#     #         if transcript:
#     #             st.write("Transcript: ", transcript)

#     option = st.selectbox(
#         'Choose an option',
#         ('Transcribe audio', 'Generate notes', 'Generate suggestions', 'Chat with GPT')
#     )

#     transcript = None
#     note = None
#     chat_history = []

#     if option == 'Transcribe audio':
#         audio_file = st.file_uploader("Upload an audio file", type=['wav', 'mp3', 'flac'])
#         if audio_file is not None:
#             if st.button("Start Transcription"):
#                 st.write("Transcribing...")
#                 transcript = transcribe_audio(audio_file)
#                 st.button("Transcription Complete", disabled=True)

#     elif option == 'Generate notes':
#         input_option = st.radio("Choose an input option", ("Enter transcript manually", "Use transcribed text"))
#         if input_option == "Enter transcript manually":
#             transcript = st.text_input("Enter transcript")
#         if st.button("Generate Note"):
#             if transcript:
#                 note = generate_notes(transcript)
#                 st.write("Note: ", note)
#     elif option == 'Generate suggestions':
#         input_option = st.radio("Choose an input option", ("Enter note manually", "Use generated note"))
#         if input_option == "Enter note manually":
#             note = st.text_input("Enter note")
#         if st.button("Generate Suggestion"):
#             if note:
#                 suggestion = generate_suggestions(note)
#                 st.write("Suggestion: ", suggestion)
#     elif option == 'Chat with GPT':
#         message = st.text_input("Enter message")
#         if st.button("Chat"):
#             if message:
#                 reply = chat_with_gpt(message)
#                 chat_history.append({"user": message, "assistant": reply})
#                 for chat in chat_history:
#                     st.write("User: ", chat["user"])
#                     st.write("Assistant: ", chat["assistant"])
def main():
    st.title("MemoMed: An Auto Note-Taking Tool for Doctors and Nurses")

    # st.header("Transcribe Speech")
    # audio_file = st.file_uploader("Upload Audio", type=['mp3', 'wav'])
    # if 'transcript' not in st.session_state:
    #     st.session_state.transcript = ''
    # if st.button("Start Transcription"):
    #     st.session_state.transcript = transcribe_audio(audio_file)
    # st.write(st.session_state.transcript)

    # st.header("Generate Notes")
    # notes_input = st.text_area("Input for Notes", st.session_state.transcript)
    # if st.button("Generate Notes"):
    #     st.session_state.notes = generate_notes(notes_input)
    #     st.write(st.session_state.notes)

    # st.header("Generate Suggestions")
    # suggestion_input = st.text_area("Input for Suggestions", st.session_state.notes if 'notes' in st.session_state else '')
    # if st.button("Generate Suggestions"):
    #     suggestions = generate_suggestions(suggestion_input)
    #     st.write(suggestions)

    # st.header("Chat with GPT")
    # chat_input = st.text_area("Input for Chat", st.session_state.notes if 'notes' in st.session_state else '')
    # if st.button("Start Chat"):
    #     chat = chat_with_gpt(chat_input)
    #     st.write(chat)

    st.header("Transcribe Audio")
    audio_file = st.file_uploader("Upload Audio", key='audio_file')
    if st.button("Start Transcription"):
        st.button("Transcribing...", disabled=True)
        transcribed_text = transcribe_audio(audio_file)
        st.session_state.transcribed_text = transcribed_text
        st.write(transcribed_text)
        st.button("Transcription Complete", disabled=True)

    # Generate Notes
    st.header("Start of the Generate Notes")
    notes_input = st.text_area("Input", value=st.session_state.transcribed_text if 'transcribed_text' in st.session_state else '', key='notes_input')
    if st.button("Generate Notes"):
        notes = generate_notes(notes_input)
        st.session_state.notes = notes
        st.markdown(f"**{notes}**", unsafe_allow_html=True)

    # Generate Suggestions
    st.header("Start of the Generate Suggestions")
    suggestions_input = st.text_area("Input", value=st.session_state.notes if 'notes' in st.session_state else '', key='suggestions_input')
    if st.button("Generate Suggestions"):
        suggestions = generate_suggestions(suggestions_input)
        st.write(suggestions)

    # # Chat with GPT
    # st.header("Start of the Chat with GPT Section")
    # chat_input = st.text_area("Input", value=st.session_state.notes if 'notes' in st.session_state else '', key='chat_input')
    # if st.button("Chat with GPT"):
    #     chat = chat_with_gpt(chat_input)
    #     st.write(chat)

    st.title("MemoMed Chatbot")

    # User input
    user_input = st.text_input("Enter your message:")

    # Send button
    if st.button("Send"):
        response = chat_with_gpt(user_input, st.session_state.notes, conversation_history)
        st.write(f"AI: {response}")

if __name__ == "__main__":
    main()
