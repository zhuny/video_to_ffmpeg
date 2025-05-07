import functools
import time
from pathlib import Path
from typing import Optional

from PIL import Image
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError, ResumableUploadError
from googleapiclient.http import MediaFileUpload


def is_quota_exceeded(error: ResumableUploadError):
    for detail in error.error_details:
        if detail['reason'] == 'quotaExceeded':
            return True
    return False


def wrap_quota_exceed(f):
    @functools.wraps(f)
    def __wrapped__(self, *args, **kwargs):
        while True:
            try:
                return f(self, *args, **kwargs)
            except (ResumableUploadError, HttpError) as e:
                if is_quota_exceeded(e):
                    print("Wait for a hour")
                    time.sleep(3600)
                else:
                    raise

    return __wrapped__


class YoutubeUploader:
    def __init__(self):
        self.auth_service = self._get_auth_service()

    def _get_auth_service(self):
        return build(
            "youtube",
            "v3",
            credentials=self._get_credential2()
        )

    def _get_credential2(self):
        return Credentials.from_authorized_user_file(
            "C:/Users/zhuny/commons/credential.json"
        )

    @wrap_quota_exceed
    def upload2_stream(self,
                       title: str, description: str,
                       publish_date: str,
                       video_file: Path):
        request = self._create_video(
            title, description,
            publish_date,
            video_file
        )
        return self._deal_stream_request(request)

    def _create_video(self,
                      title: str, description: str, publish_date: str,
                      video_file: Path):
        description = description.replace('<', '[').replace('>', ']')
        body = {
            "snippet": {
                "title": title,
                "description": description
            },
            "status": {
                "privacyStatus": "private",
            }
        }
        if publish_date:
            body['status']['publishAt'] = f"{publish_date}T22:00:00+09:00"
        return self.auth_service.videos().insert(
            part=",".join(body),
            body=body,
            media_body=MediaFileUpload(
                video_file,
                chunksize=-1, resumable=True,
                mimetype="application/octet-stream"
            )
        )

    @staticmethod
    def _deal_stream_request(request):
        response = None
        while response is None:
            try:
                print("Upload...")
                status, response = request.next_chunk()
                if response is not None:
                    return response['id']
            except HttpError as e:
                if e.resp.status not in (500, 502, 503, 504):
                    raise
                time.sleep(2)

    @wrap_quota_exceed
    def upload_thumbnail(self, video_id: str, thumbnail_path: Optional[Path]):
        # thumbnail이 없는 경우 스킵
        if thumbnail_path is None or not thumbnail_path.is_file():
            return

        # 2MB보다 크면 썸네일을 좀 더 작게 만든다.
        if thumbnail_path.stat().st_size > 2097152:
            thumbnail_path = self._make_thumbnail(thumbnail_path)

        self.auth_service.thumbnails().set(
            videoId=video_id,
            media_body=str(thumbnail_path)
        ).execute()

    def _make_thumbnail(self, thumbnail_path: Path) -> Path:
        image = Image.open(thumbnail_path)
        size = image.size[0] // 2, image.size[1] // 2
        image.thumbnail(size)
        small_version = thumbnail_path.with_stem(thumbnail_path.stem + "_thumb")
        image.save(small_version)
        return small_version
