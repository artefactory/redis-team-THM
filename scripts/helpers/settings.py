from pydantic import BaseSettings

from helpers.models import Format


class Settings(BaseSettings):
    format: Format = Format.BibTeX
    max_results: int = 3
