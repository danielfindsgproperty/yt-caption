from fastapi import FastAPI, HTTPException, Query
from youtube_transcript_api import YouTubeTranscriptApi
import os
from typing import List

app = FastAPI(title="YouTube Transcript API", version="1.0.0")

@app.get("/")
def health_check():
    return {"status": "healthy", "message": "YouTube Transcript API is running"}

@app.get("/transcript")
def get_transcript(video_id: str = Query(..., description="YouTube Video ID")):
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id)
        
        # Convert to text
        text = "\n".join([snippet.text for snippet in transcript])
        
        return {
            "video_id": video_id,
            "transcript": text,
            "language": transcript.language,
            "segments": transcript.to_raw_data()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error extracting transcript: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
