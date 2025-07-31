import re
from mcp.server.fastmcp import FastMCP
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

# Create an MCP server instance
mcp = FastMCP("YouTube Tools", 
dependencies=["youtube-transcript-api"], 
host="0.0.0.0",
port=8000 ###it seems render.com need this host and port
)

@mcp.tool()
def get_youtube_video_id(youtube_url: str) -> str:
    """
    Extracts the video ID from a YouTube URL.

    Args:
        youtube_url: The full URL of the YouTube video.

    Returns:
        The extracted YouTube video ID.
    """
    # Regex pattern to match various YouTube URL formats
    # This pattern covers standard URLs, shortened URLs, and embed URLs.
    pattern = (
        r'(?:https?://)?(?:www\.)?'
        r'(?:youtube\.com|youtu\.be|youtube-nocookie\.com)'
        r'(?:/(?:embed/|v/|watch\?v=|watch\?.+&v=))?'
        r'([a-zA-Z0-9_-]{11})'
    )
    match = re.search(pattern, youtube_url)
    if match:
        return match.group(1)
    else:
        # If no match, return an informative error message.
        return "Could not extract video ID. Please provide a valid YouTube URL."

@mcp.tool()
def get_youtube_transcript(video_id: str) -> str:
    """
    Fetches the full transcript of a YouTube video given its video ID.

    Args:
        video_id: The 11-character YouTube video ID.

    Returns:
        The full transcript of the video as a single string, or an error message.
    """
    try:
        # Retrieve the transcript for the given video ID.
        # This will attempt to get all available transcripts and concatenate them.
        transcript_list = YouTubeTranscriptApi().fetch(video_id).to_raw_data()
        full_transcript = " ".join([entry['text'] for entry in transcript_list])
        return full_transcript
    except NoTranscriptFound:
        return f"No transcript found for video ID: {video_id}. It might not have captions."
    except TranscriptsDisabled:
        return f"Transcripts are disabled for video ID: {video_id}."
    except Exception as e:
        # Catch any other potential errors during transcript retrieval.
        return f"An error occurred while fetching the transcript: {e}"

# This block allows you to run the server directly for testing.
if __name__ == "__main__":
    # Run the MCP server.
    # The 'stdio' transport allows interaction via standard input/output,
    # which is useful for development and testing with tools like `uv run mcp dev`
    mcp.run(transport="streamable-http")
