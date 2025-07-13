import json
from typing import Optional
import aiohttp
import logging
import aiofiles


class AsyncHTTPClient:
    def __init__(self, headers=None, timeout=None):
        """
        Initializes the AsyncHTTPClient.

        Args:
            headers (dict, optional): Default headers to include in all requests. Defaults to None.
            timeout (int or float, optional): Default timeout (in seconds) for requests. Defaults to None.
        """
        self.base_url = "http://localhost:8000"
        self.headers = headers if headers is not None else {}
        self.timeout = timeout

    def _build_url(self, path):
        """
        Builds the full URL by combining the base URL and the path.

        Args:
            path (str): The path to append to the base URL.

        Returns:
            str: The full URL.
        """
        if self.base_url:
            return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        return path

    async def get(
        self,
        path,
        params=None,
        headers=None,
        timeout=None,
        raise_for_status=True,
        expected_status_codes=[200],
        **kwargs,
    ):
        """
        Sends an HTTP GET request.

        Args:
            path (str): The path for the request.
            params (dict, optional): Query parameters to include in the URL. Defaults to None.
            headers (dict, optional): Request-specific headers. Defaults to None.
            timeout (int or float, optional): Request-specific timeout (in seconds). Defaults to None.
            **kwargs: Additional keyword arguments to pass to the aiohttp.ClientSession.get() method.

        Returns:
            dict: The JSON response.
        """
        url = self._build_url(path)
        merged_headers = self.headers.copy()
        if headers:
            merged_headers.update(headers)
        req_timeout = timeout if timeout is not None else self.timeout

        async with aiohttp.ClientSession() as session:
            get_info = dict(
                url=url,
                params=params,
                headers=merged_headers,
            )
            logging.info(f"Sending 'GET': {get_info}")

            async with session.get(
                url,
                params=params,
                headers=merged_headers,
                timeout=req_timeout,
                **kwargs,
            ) as response:
                expected_code_received = response.status in expected_status_codes

                if expected_code_received:
                    logging.info(f"Expected status code {response.status} received.")
                elif raise_for_status:
                    msg = f"Unexpected status code {response.status} received."
                    logging.warning(msg)
                    if raise_for_status:
                        response.raise_for_status()
                        assert response.status in expected_status_codes, msg
                elif raise_for_status:
                    response.raise_for_status()

                if response.headers.get("Content-Type", "") in ["application/json"]:
                    response_json = await response.json()
                    # logging.info(f"Response: {response_json}")
                    return response_json

                elif response.headers.get("Content-Type", "") in [
                    "application/pdf",
                    "application/vnd.ms-excel",
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    "image/jpeg",
                    "image/png",
                    "application/zip",
                    "text/html; charset=utf-8",
                    "audio/mpeg",
                    "video/mp4",
                ]:
                    data = await response.read()
                    # logging.info(f"Response: {data}")
                    return data

                else:
                    text = await response.text()
                    # logging.info(f"Response: {text}")
                    return text

    async def post(
        self,
        path,
        data=None,
        json=None,
        headers=None,
        timeout=None,
        raise_for_status=True,
        expected_status_codes=[200],
        **kwargs,
    ):
        """
        Sends an HTTP POST request.

        Args:
            path (str): The path for the request.
            data (dict or str, optional): The data to send in the request body (as form-encoded data).
        Defaults to None.
            json (dict, optional): The JSON data to send in the request body. Defaults to None.
            headers (dict, optional): Request-specific headers. Defaults to None.
            timeout (int or float, optional): Request-specific timeout (in seconds). Defaults to None.
            **kwargs: Additional keyword arguments to pass to the aiohttp.ClientSession.post() method.

        Returns:
            aiohttp.ClientResponse: The response object.
        """
        url = self._build_url(path)
        merged_headers = self.headers.copy()
        if headers:
            merged_headers.update(headers)
        req_timeout = timeout if timeout is not None else self.timeout

        # logging.info(f"Sending 'POST' to {url} with following json: {json}")

        async with aiohttp.ClientSession() as session:
            post_info = dict(
                url=url,
                data=data,
                json=json,
                headers=merged_headers,
            )
            # logging.info(f"Sending 'POST': {post_info}")

            async with session.post(
                url,
                data=data,
                json=json,
                headers=merged_headers,
                timeout=req_timeout,
                **kwargs,
            ) as response:
                expected_code_received = response.status in expected_status_codes

                if expected_code_received:
                    logging.info(f"Expected status code {response.status} received.")

                elif not expected_code_received:
                    msg = f"Unexpected status code {response.status} received."

                    logging.warning(msg)

                    if raise_for_status:
                        response.raise_for_status()

                        assert response.status in expected_status_codes, msg

                elif raise_for_status:
                    response.raise_for_status()

                return response

    async def delete(
        self,
        path,
        headers=None,
        timeout=None,
        raise_for_status=True,
        expected_status_codes=[204],
        **kwargs,
    ):
        """
        Sends an HTTP DELETE request.

        Args:
            path (str): The path for the request.
            headers (dict, optional): Request-specific headers. Defaults to None.
            timeout (int or float, optional): Request-specific timeout (in seconds). Defaults to None.
            **kwargs: Additional keyword arguments to pass to the aiohttp.ClientSession.delete() method.

        Returns:
            aiohttp.ClientResponse: The response object.
        """
        url = self._build_url(path)
        merged_headers = self.headers.copy()
        if headers:
            merged_headers.update(headers)
        req_timeout = timeout if timeout is not None else self.timeout

        async with aiohttp.ClientSession() as session:
            delete_info = dict(url=url, headers=merged_headers)
            logging.info(f"Sending 'DELETE': {delete_info}")

            async with session.delete(
                url, headers=merged_headers, timeout=req_timeout, **kwargs
            ) as response:
                expected_code_received = response.status in expected_status_codes

                if expected_code_received:
                    logging.info(f"Expected status code {response.status} received.")
                elif not expected_code_received:
                    msg = f"Unexpected status code {response.status} received."
                    logging.warning(msg)
                    if raise_for_status:
                        response.raise_for_status()
                        assert response.status in expected_status_codes, msg
                elif raise_for_status:
                    response.raise_for_status()

                return response

    async def patch(
        self,
        path,
        data=None,
        json=None,
        headers=None,
        timeout=None,
        raise_for_status=True,
        expected_status_codes=[200],
        **kwargs,
    ):
        """
        Sends an HTTP PATCH request.

        Args:
            path (str): The path for the request.
            data (dict or str, optional): The data to send in the request body (as form-encoded data).
        Defaults to None.
            json (dict, optional): The JSON data to send in the request body. Defaults to None.
            headers (dict, optional): Request-specific headers. Defaults to None.
            timeout (int or float, optional): Request-specific timeout (in seconds). Defaults to None.
            **kwargs: Additional keyword arguments to pass to the aiohttp.ClientSession.patch() method.

        Returns:
            dict: The JSON response.
        """
        url = self._build_url(path)
        merged_headers = self.headers.copy()
        if headers:
            merged_headers.update(headers)
        req_timeout = timeout if timeout is not None else self.timeout

        async with aiohttp.ClientSession() as session:
            patch_info = dict(
                url=url,
                data=data,
                json=json,
                headers=merged_headers,
            )
            logging.info(f"Sending 'PATCH': {patch_info}")

            async with session.patch(
                url,
                data=data,
                json=json,
                headers=merged_headers,
                timeout=req_timeout,
                **kwargs,
            ) as response:
                expected_code_received = response.status in expected_status_codes

                if expected_code_received:
                    logging.info(f"Expected status code {response.status} received.")

                elif not expected_code_received:
                    msg = f"Unexpected status code {response.status} received."
                    logging.warning(msg)
                    logging.warning(await response.text())
                    if raise_for_status:
                        response.raise_for_status()
                        assert response.status in expected_status_codes, msg
                elif raise_for_status:
                    response.raise_for_status()

                response_json = await response.json()
                # logging.info(f"Response: {response_json}")
                return response_json

    async def upload_file(
        self,
        path,
        filename,
        request_id=None,
        session_id=None,
        content_type=None,
        headers: Optional[dict] = {},
        expected_status_codes=[201],
    ):
        url = self._build_url(path)

        async with aiofiles.open(filename, mode="rb") as file:
            data = aiohttp.FormData()

            data.add_field("file", file, filename=filename, content_type=content_type)

            json_field = {}

            if request_id:
                json_field["request_id"] = request_id

            if session_id:
                json_field["session_id"] = session_id

            if json_field:
                data.add_field(
                    "json_field",
                    json.dumps(json_field),
                    content_type="application/json",
                )

            async with aiohttp.ClientSession() as session:
                upload_info = {
                    "url": url,
                    "filename": filename,
                    "content_type": content_type,
                    "request_id": request_id,
                    "session_id": session_id,
                }
                logging.info(f"Uploading file via POST: {upload_info}")

                async with session.post(url, data=data, headers=headers) as response:
                    if response.status in expected_status_codes:
                        json_response = await response.json()

                        file_id = json_response.get("id")
                        msg = f"File was successfully uploaded: {file_id}"
                        logging.info(msg)

                        return file_id

                    else:
                        status = response.status

                        warning = f"Failed to upload file. Status code: {status}, details:{await response.json()}"

                        logging.warning(warning)

                        return None
