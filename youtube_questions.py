from youtube_transcript_api import YouTubeTranscriptApi
import generative


def get_transcript(url, max_length=512, start_time=-1, end_time=-1):
  if start_time == -1 and end_time == -1:
    transcript = YouTubeTranscriptApi.get_transcript(url[32:47])
    text = ''
    for i in transcript:
      new_text = text + i['text']
      if len(new_text) > max_length:
        return text
      text = new_text
    return text

def generate_questions_from_youtube(url):
  transcript = get_transcript(url)
  questions = generative.generate_questions(generative.form_questions_prompt(transcript))
  return questions