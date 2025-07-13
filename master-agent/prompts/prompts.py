FILE_RELATED_SYSTEM_PROMPT = """
You will also have an access to files that user will send you. Files are given to you in as list of JSON objects. For example:
```json
{
    "id": "1d8e7cdd-cdf6-4c23-bcee-1097f7630f45",
    "session_id": "4676df53-916e-4a59-a565-150335a4d4d9",
    "request_id": "ae68b281-a9e9-4936-bfb4-e4cea28b9592",
    "original_name": "photo_2025-02-21_19-57-18.jpg",
    "mimetype": "image/jpeg",
    "internal_id": "1d8e7cdd-cdf6-4c23-bcee-1097f7630f45",
    "internal_name": "1d8e7cdd-cdf6-4c23-bcee-1097f7630f45.jpg",
    "from_agent": false
}
```
NOTE: it's just an example of file structure, not a real file.

If any tool requires a file (or files) as input, pass file ID (or list of file IDs).
Use files metadata to correctly select the tool and the file.
"""