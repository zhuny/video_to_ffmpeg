import datetime
import operator

from app.core.model.custom import IntList
from app.core.model.video import VideoOutput
from app.core.youtube import YoutubeUploader


def run(video_id_list: IntList):
    """
    유튜브에 영상을 업로드 합니다.

    :param video_id_list: 올릴 Video ID list
    """

    video_id_list.shuffle()
    today = datetime.date.today()

    for video_id in video_id_list:
        video = VideoOutput(video_id)
        if not video.is_exists():
            continue

        video.load()
        video.model.publish_date = today
        today += datetime.timedelta(days=1)
        video.save()
        print(video.model.name, video.model.publish_date)

    uploader = YoutubeUploader()

    video_list = [
        vo
        for video_id in video_id_list
        if (vo := VideoOutput(video_id)).is_exists()
    ]
    for video in video_list:
        video.load()
    video_list = [
        video
        for video in video_list
        if video.model.publish_date is not None
    ]
    video_list.sort(
        key=operator.attrgetter("model.publish_date")
    )

    for video in video_list:
        print(video.output_file)
        print(video.model.video_id)
        print(video.thumbnail_image)
        video.model.video_id = uploader.upload2_stream(
            title=video.model.video_name,
            description=video.model.video_description,
            publish_date=video.model.publish_date,
            video_file=video.output_file
        )
        video.save()
        uploader.upload_thumbnail(
            video_id=video.model.video_id,
            thumbnail_path=video.thumbnail_image
        )
