# HuntAPI for Hermes Agent

Video and audio from public links for [Hermes Agent](https://hermes-agent.nousresearch.com), through the [HuntAPI](https://www.huntapi.com) media API.

- **Read a video's metadata** without downloading it: title, channel, duration, views, likes, upload date, thumbnail and description.
- **Download the video** in the quality and format you want, or the picture only.
- **Extract the audio** of a video, talk or podcast as MP3, M4A or WAV.

Works with YouTube, TikTok, Instagram, Facebook, Vimeo, X, Twitch, Reddit and many more sites.

## Contents

- [Install](#install)
- [How it works](#how-it-works)
- [Tools](#tools)
- [Download options](#download-options)
- [Example prompts](#example-prompts)
- [Credits and errors](#credits-and-errors)
- [What it does on your machine](#what-it-does-on-your-machine)

## Install

```sh
hermes plugins install huntapi
```

Hermes asks for `HUNTAPI_API_KEY` during the install. Create a key in the [HuntAPI dashboard](https://app.huntapi.com).

Answer yes to `Enable 'huntapi' now?`, or run `hermes plugins enable huntapi` later. The tools join the `huntapi` toolset, which is on by default; turn it on or off in `hermes tools` like any other toolset. They stay hidden from the model until the API key is set.

## How it works

Each tool is one HTTPS call to `https://api.huntapi.com`, authenticated with your key.

Metadata comes back right away. Downloads take longer, so they run as jobs on HuntAPI's servers:

1. `huntapi_video_download` or `huntapi_audio_download` starts the job and returns a `job_id`.
2. The model calls `huntapi_job_status` with that id. While `status` is `Queued` or `Running`, `progress` goes from 0 to 100.
3. When `status` is `CompletedJob`, `result.response` is a link to the file on HuntAPI's storage, and `result.metadata` describes it. `Error`, `NotFound` or `BadRequest` mean the job failed, with the reason.

```json
{
  "status": "CompletedJob",
  "progress": 100,
  "result": {
    "metadata": {"title": "…", "view_count": 82398, "upload_date": 1729641600},
    "response": "https://s3.huntapi.com/videos/32f88fc4-e728-4c45-b27c-6ee539575595.webm"
  }
}
```

The tool descriptions tell the model this flow, so a request like "download this video" ends with the link in the chat. The file stays on HuntAPI's storage: nothing is downloaded to your machine unless you open the link.

## Tools

| Tool | What it does | Input | Credits |
|---|---|---|---|
| `huntapi_media_metadata` | Title, description, channel and its URL, duration, views, likes, upload date, thumbnail, width and height, live status, without downloading. | `url` | 1 |
| `huntapi_video_download` | Starts a video download and returns a `job_id`. | `url` | 1 |
| `huntapi_audio_download` | Starts an audio extraction and returns a `job_id`. | `url` | 1 |
| `huntapi_job_status` | Status, progress and result (download link) of a job. | `job_id` | free |
| `huntapi_usage` | Your plan, credits used, credits left, renewal date and rate limit. | none | free |

## Download options

| Option | Tool | Values |
|---|---|---|
| `video_quality` | video | `best` (default), `1080p`, `720p`, `480p`, `360p`. Videos longer than an hour are capped at 720p. |
| `video_format` | video | `mp4` (default), `webm`, `mkv` |
| `without_sound` | video | `true` for the picture only |
| `audio_format` | audio | `mp3` (default), `m4a`, `wav` |
| `audio_quality` | audio | `best` (default), `320kbps`, `256kbps`, `128kbps` |
| `max_duration` | both | keep only the first N seconds |

Formats are a preference: when a source cannot be converted, the file can come in another format.

Some links cannot be read or downloaded: private videos, deleted ones, age-restricted ones, and content that needs a login. The job then ends in `Error` with the reason.

## Example prompts

- "What is this video about, how long is it and how many views does it have? https://www.youtube.com/watch?v=…"
- "Download this TikTok in the best quality and send me the link."
- "Get the audio of this talk as an MP3 so I can listen to it offline."
- "Download only the first 60 seconds of this video in 720p."
- "Compare the views and likes of these five YouTube videos."
- "How many HuntAPI credits do I have left?"

## Credits and errors

- Metadata and each download use 1 credit; following a job and `huntapi_usage` are free. The cost is at the end of each tool's description, so the model knows it before it calls. Plans and prices: [huntapi.com/pricing](https://www.huntapi.com/pricing).
- Errors come back to the model as `{"error": "HuntAPI: <message>"}` with the API's own message (invalid key, no credits left, unsupported or private link), so it can explain or try another option.
- Calls time out after 60 seconds; long downloads keep running as jobs.

## What it does on your machine

- **Network:** calls `https://api.huntapi.com` only, with your `HUNTAPI_API_KEY`. Calls use credits on your HuntAPI account.
- **Credentials:** reads the key only through Hermes's secret scope. It stores nothing.
- **Nothing else:** no files written, no processes started, no telemetry, no self-update. Standard library only, no dependencies.

Download only content you have the right to download.

## Development

```sh
python -m pytest
```

The tests mock the network and run without Hermes installed.

## Contact

- Source: https://github.com/huntapi/hermes-plugin-huntapi
- HuntAPI: https://www.huntapi.com
- Issues: https://github.com/huntapi/hermes-plugin-huntapi/issues

## License

MIT
