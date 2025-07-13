import json
import pathlib
import platform
import os
from typing import Optional

import typer
from src.exceptions import UnAuthorizedException
from src.log import render_error, render_success, render_warning


class CredentialsManager:
    def __init__(self):
        self.cli_creds_directory_name = ".genai"
        self.credentials_filename = "credentials.json"
        self.unauthorized_exc = UnAuthorizedException(
            "Token is invalid or expired. Please log in again."
        )

    def get_config_dir(self) -> pathlib.Path:
        """
        Function to get genai folder path under /home/user/.genai
        to store the credentials json file
        """
        if platform.system() == "Windows":
            config_dir = (
                pathlib.Path(os.getenv("LOCALAPPDATA"))
                / self.cli_creds_directory_name[1:]
            )

            return config_dir
        else:
            home = pathlib.Path().home()
            config_dir = home / self.cli_creds_directory_name
            return config_dir

    def get_creds_fp(self) -> pathlib.Path:
        return self.get_config_dir() / self.credentials_filename

    def load_credentials(self) -> Optional[dict[str, str]]:
        creds_path = self.get_creds_fp()
        if not creds_path.is_file():
            return None

        try:
            with open(creds_path, "r") as f:
                token_data = json.load(f)
                return token_data

        except (OSError, json.JSONDecodeError) as e:
            render_warning(
                f"Could not parse credentials file at {creds_path}: {str(e)}"
            )
            return None

        except json.JSONDecodeError:
            raise UnAuthorizedException(
                "Credentials file is invalid or malformed. Please log in again."
            )

    def dump_credentials(self, access_token: str) -> None:
        config_dir = self.get_config_dir()
        creds_path = self.get_creds_fp()

        try:
            config_dir.mkdir(parents=True, exist_ok=True)
            with open(creds_path, "w+") as f:
                json.dump({"token": access_token}, f)

        except OSError as e:
            render_error(
                f"Error: Could not write credentials file at {config_dir}: {e}"
            )
            raise typer.Exit(code=1)

    def logout(self):
        with open(self.get_creds_fp(), "w+") as creds_file:
            creds_file.write("{}")
            render_success("Logged out successfully!")
        return
