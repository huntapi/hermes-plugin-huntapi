"""Tool schemas (what the model reads) and how each tool maps to the API."""

# name: (description, JSON schema of the arguments, API path, {argument: API parameter}, fixed parameters)
TOOLS = {
    'huntapi_media_metadata': (
        'Read the metadata of a public video or audio URL without downloading it (YouTube, TikTok, Instagram, Facebook, Vimeo, X, Twitch, Reddit and more): title, description, channel, duration, views, likes, upload date, thumbnail, size and whether it is live. Costs 1 credit per call.',
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
        'Start downloading a public video (YouTube, TikTok, Instagram, Facebook, Vimeo, X, Twitch, Reddit and more). Returns a job_id: call huntapi_job_status with it until status is CompletedJob, then give the user the download link in result.response. Costs 1 credit per call.',
        {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "Public video URL."
                },
                "video_quality": {
                    "type": "string",
                    "enum": [
                        "best",
                        "1080p",
                        "720p",
                        "480p",
                        "360p"
                    ],
                    "description": "Video quality: best (default), 1080p, 720p, 480p or 360p. Videos longer than an hour are capped at 720p."
                },
                "video_format": {
                    "type": "string",
                    "enum": [
                        "mp4",
                        "webm",
                        "mkv"
                    ],
                    "description": "Output format: mp4 (default), webm or mkv. A preference: the file can come in another format."
                },
                "without_sound": {
                    "type": "boolean",
                    "description": "true downloads the picture only, without the audio track."
                },
                "max_duration": {
                    "type": "integer",
                    "minimum": 1,
                    "description": "Keep only the first N seconds."
                }
            },
            "required": [
                "url"
            ]
        },
        '/v1/video/download',
        {'url': 'query', 'video_quality': 'video_quality', 'video_format': 'video_format', 'max_duration': 'max_duration', 'without_sound': 'without_sound'},
        {},
    ),
    'huntapi_audio_download': (
        'Start extracting the audio track of a public video or audio URL, for example a podcast, a talk or a song. Returns a job_id: call huntapi_job_status with it until status is CompletedJob, then give the user the download link in result.response. Costs 1 credit per call.',
        {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "Public media URL."
                },
                "audio_format": {
                    "type": "string",
                    "enum": [
                        "mp3",
                        "m4a",
                        "wav"
                    ],
                    "description": "Output format: mp3 (default), m4a or wav. A preference: the file can come in another format."
                },
                "audio_quality": {
                    "type": "string",
                    "enum": [
                        "best",
                        "320kbps",
                        "256kbps",
                        "128kbps"
                    ],
                    "description": "Audio quality: best (default), 320kbps, 256kbps or 128kbps."
                },
                "max_duration": {
                    "type": "integer",
                    "minimum": 1,
                    "description": "Keep only the first N seconds."
                }
            },
            "required": [
                "url"
            ]
        },
        '/v1/audio/download',
        {'url': 'query', 'audio_format': 'audio_format', 'audio_quality': 'audio_quality', 'max_duration': 'max_duration'},
        {},
    ),
    'huntapi_job_status': (
        'Get the status and progress (0-100) of a HuntAPI download job. status is Queued or Running while it works; when it is CompletedJob, result.response is the download link and result.metadata describes the file; Error, NotFound or BadRequest mean it failed. Wait a few seconds between two calls. Free.',
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
    'huntapi_usage': (
        'Your HuntAPI account: plan, credits used, credits left, renewal date and rate limit. Free.',
        {
            "type": "object",
            "properties": {},
            "required": []
        },
        '/v1/usage',
        {},
        {},
    ),
}
