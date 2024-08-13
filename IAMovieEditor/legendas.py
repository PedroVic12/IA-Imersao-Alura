import requests
import json
import time


base_url = "https://api.assemblyai.com/v2"

headers = {
    "authorization": "YOUR_API_KEY"
}

with open("./my-audio.mp3", "rb") as f:
  response = requests.post(base_url + "/upload",
                          headers=headers,
                          data=f)

upload_url = response.json()["upload_url"]

data = {
    "audio_url": upload_url
}


url = base_url + "/transcript"
response = requests.post(url, json=data, headers=headers)


transcript_id = response.json()['id']
polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

while True:
  transcription_result = requests.get(polling_endpoint, headers=headers).json()

  if transcription_result['status'] == 'completed':
    break

  elif transcription_result['status'] == 'error':
    raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

  else:
    time.sleep(3)



def get_subtitle_file(transcript_id, file_format):
    if file_format not in ["srt", "vtt"]:
        raise ValueError("Invalid file format. Valid formats are 'srt' and 'vtt'.")

    url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}/{file_format}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        raise RuntimeError(f"Failed to retrieve {file_format.upper()} file: {response.status_code} {response.reason}")


subtitle_text = get_subtitle_file(transcript_id, "vtt")
# subtitle_text = get_subtitle_file(transcript_id, "srt")
print(subtitle_text)