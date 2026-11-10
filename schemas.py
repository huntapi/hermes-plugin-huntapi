"""Tool schemas (what the model reads) and how each tool maps to the API."""

# name: (description, JSON schema of the arguments, API path, {argument: API parameter}, fixed parameters)
TOOLS = {
    'huntapi_media_metadata': (
        'Get the metadata of a public video or audio URL (YouTube, TikTok, Instagram, Vimeo, X, Reddit and more): title, channel, duration, views, likes, upload date, thumbnail and available formats.',
        {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "Public media URL."
                }
            },
            "required": [
                "url"
            ]
        },
        '/v1/media/metadata',
        {'url': 'query'},
        {},
    ),
    'huntapi_video_download': (
        'Start downloading a public video. Returns a job_id: call huntapi_job_status with it until the job completes, then read the download link from the result.',
        {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "Public video URL."
                },
                "video_quality": {
                    "type": "string",
                    "description": "Video quality: best (default), or a height such as 1080, 720, 480."
                },
                "video_format": {
                    "type": "string",
                    "description": "Output format, for example mp4 (default) or webm."
                }
            },
            "required": [
                "url"
            ]
        },
        '/v1/video/download',
        {'url': 'query', 'video_quality': 'video_quality', 'video_format': 'video_format'},
        {},
    ),
    'huntapi_audio_download': (
        'Start extracting the audio of a public media URL. Returns a job_id: call huntapi_job_status with it until the job completes, then read the download link from the result.',
        {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "Public media URL."
                },
                "audio_format": {
                    "type": "string",
                    "description": "Output format, for example mp3 (default) or m4a."
                }
            },
            "required": [
                "url"
            ]
        },
        '/v1/audio/download',
        {'url': 'query', 'audio_format': 'audio_format'},
        {},
    ),
    'huntapi_job_status': (
        'Get the status, progress and result of a HuntAPI download job.',
        {
            "type": "object",
            "properties": {
                "job_id": {
                    "type": "string",
                    "description": "The job_id returned by huntapi_video_download or huntapi_audio_download."
                }
            },
            "required": [
                "job_id"
            ]
        },
        '/v1/jobs/{job_id}',
        {},
        {},
    ),
}
