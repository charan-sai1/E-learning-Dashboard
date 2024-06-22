import streamlit as st
import pandas as pd

def display_videos(topic):
    st.session_state['selected_topic'] = topic
    st.session_state['selected_link'] = None  # Reset selected link when new topic is selected
    st.session_state['show_questions'] = False  # Reset show questions when new topic is selected

def play_video(link):
    st.session_state['selected_link'] = link

def show_questions():
    st.session_state['show_questions'] = True

if __name__ == "__main__":
    # Set Streamlit page configuration
    
    st.set_page_config(page_title="Rangamma teaching portal Class-9", layout="wide", initial_sidebar_state="expanded")

    # Load the Excel file
    file_path = 'newClass9.xlsx'
    df = pd.read_excel(file_path)
    
    # Remove trailing spaces from column names
    df.columns = df.columns.str.strip()

    # Group the data by Chapter
    chapters = df.groupby('Chapter')

    st.sidebar.title("Class 9 Topics")

    # Iterate over each chapter in the sidebar
    for chapter, topics in chapters:
        with st.sidebar.expander(chapter):
            for index, row in topics.iterrows():
                st.button(row['Topic'], key=row['Topic'], on_click=display_videos, args=(row['Topic'],))

    # Display selected video and questions on the main page
    if 'selected_topic' in st.session_state:
        topic = st.session_state['selected_topic']
        youtube_links = df.loc[df['Topic'] == topic, 'Youtube link'].values[0]
        youtube_links = youtube_links.split(',')

        
        # Display expandable elements for each video
        for link in youtube_links:
            with st.expander(f"{link}"):
                if st.button("Play Video", key=link, on_click=play_video, args=(link,)):
                    pass  # Button click handled by on_click callback

        if 'selected_link' in st.session_state and st.session_state['selected_link']:
            st.video(st.session_state['selected_link'])

        # Add button to show questions
        if st.button("Show Topic related Questions"):
            show_questions()
        
        # Display questions if the button is clicked
        if 'show_questions' in st.session_state and st.session_state['show_questions']:
            questions = df.loc[df['Topic'] == topic, 'Questions'].values[0]  # Adjust 'Questions' to your column name
            if questions:
                st.write("Questions for this topic:")
                st.write(questions)

                # Add checkbox to show answers
                show_answers = st.checkbox("Show Answers")
                if show_answers:
                    answers = df.loc[df['Topic'] == topic, 'Answers'].values[0]  # Adjust 'Answers' to your column name
                    if answers:
                        st.write("Answers for this topic:")
                        st.write(answers)
    else:
        st.title("My teching Portal",anchor=False)
        st.header("Class - 9",anchor=False)
        st.subheader("Text Book",divider="blue",anchor=False,help="Click the text Bool button")
        st.link_button(label="Text Book",url = "https://drive.google.com/file/d/1o2Bvh0QxZJ5X_Bdkk96oYK9Xy5elZ5PZ/edit")
        st.subheader("Syllabus",divider="blue",anchor=False)
        st.image(image="sylabus.png")