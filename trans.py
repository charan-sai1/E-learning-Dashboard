import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import time 

# Configure Google Generative AI
genai.configure(api_key="AIzaSyBnagd8vxfMIEQjcqsjxeXoyhBEUG20oD8")

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript
    except Exception as e:
        return None

def gen(p):
    config = {
        "max_output_tokens": 4000,
        "temperature": 0.1,  
    }
    try:
        model = genai.GenerativeModel(model_name='gemini-1.5-flash', generation_config=config)
        response = model.generate_content(p).text.replace('*', '')
    except Exception as e:
        response = "Error while generating questions"
    return response

def questions(transcript):
    prompt = f"""Act as a professional biology teacher, for the class 9 students,
    Give me 4 question based on the given context to text if the students understood the topic clearly\nTopic:
    {transcript}

    The questions should be in the format 
    1. Question-1
    2. Question-2
    3. Question-3
    4. Question-4
    Don't generate different format and out of the context"""
    questions = gen(prompt)
    return questions

def answers(qus):
    prompt = "Generate the accurate one small sentence answers for the given questions in this order\n1. ans1\n2. ans2\n3. ans3\n4. ans4\n" + qus
    try:
        ans = gen(prompt) 
    except Exception:
        time.sleep(2)
        ans = gen(prompt) 
    return ans

# Load the existing Excel file with processed links
input_file_path = 'output_file.xlsx'
df = pd.read_excel(input_file_path)

# Create columns for questions and answers
df['Questions'] = ''
df['Answers'] = ''

# Generate questions and answers for each processed link
for index, row in df.iterrows():
    transcript = row['Processed Links']
    if transcript.strip():  # Ensure there's content to process
        generated_questions = questions(transcript)
        generated_answers = answers(generated_questions)
        df.at[index, 'Questions'] = generated_questions
        df.at[index, 'Answers'] = generated_answers
    else:
        generated_questions = questions(row['Topic Name'])
        generated_answers = answers(generated_questions)
        df.at[index, 'Questions'] = generated_questions
        df.at[index, 'Answers'] = generated_answers
# Save the updated DataFrame back to the Excel file
output_file_path = 'output_file.xlsx'
df.to_excel(output_file_path, index=False)

print("Processing complete. Results saved to", output_file_path)
