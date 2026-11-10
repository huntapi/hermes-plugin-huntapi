# HuntAPI for Hermes Agent

Gives [Hermes Agent](https://hermes-agent.nousresearch.com) tools to read the metadata of public videos and download their video or audio, through the HuntAPI media API.

## Install

```sh
hermes plugins install huntapi
```

Hermes asks for `HUNTAPI_API_KEY` during the install. Create a key in the [HuntAPI dashboard](https://app.huntapi.com).

## Tools

| Tool | What it does |
|---|---|
| `huntapi_media_metadata` | Get the metadata of a public video or audio URL (YouTube, TikTok, Instagram, Vimeo, X, Reddit and more): title, channel, duration, views, likes, upload date, thumbnail and available formats. |
| `huntapi_video_download` | Start downloading a public video. Returns a job_id: call huntapi_job_status with it until the job completes, then read the download link from the result. |
| `huntapi_audio_download` | Start extracting the audio of a public media URL. Returns a job_id: call huntapi_job_status with it until the job completes, then read the download link from the result. |
| `huntapi_job_status` | Get the status, progress and result of a HuntAPI download job. |

The tools are hidden from the model until the API key is set.

## What it does on your machine

- **Network:** calls `https://api.huntapi.com` only, with your `HUNTAPI_API_KEY`. Calls can use credits on your HuntAPI account ([pricing](https://www.huntapi.com/pricing)).
- **Credentials:** reads the key only through Hermes's secret scope. It stores nothing.
- **Nothing else:** no files written, no processes started, no telemetry, no self-update. Standard library only, no dependencies.

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
