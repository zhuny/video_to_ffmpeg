from app.command.prompt import get_default_or_input
from app.core.model.video import VideoOutput


def run(video_id: int):
    """
    Video의 meta data를 수정합니다.

    :param video_id: 비디오 ID
    """

    video = VideoOutput(video_id)
    if not video.is_exists():
        print("Video Not Exists!")
        return

    video.load()

    print(f'{video_id}. {video.model.name}')
    print(f'  Video Name : {video.model.video_name}')
    print(f'  Video Description : {video.model.video_description}')
    print()

    video.update_meta(
        name=get_default_or_input(
            "Name", video.model.name
        ),
        video_name=get_default_or_input(
            "Video Name", video.model.video_name
        ),
        video_description=get_default_or_input(
            "Video Description",
            video.model.video_description
        )
    )
    video.save()
