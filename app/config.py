from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('config/default.env', 'config/prod.env'),
        env_file_encoding='utf-8'
    )

    ffmpeg_executable: Path
    video_output_folder: Path


setting = Settings()
