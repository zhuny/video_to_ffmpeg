from app.core.model.custom import IntList
from app.core.model.video import VideoOutput


def run(video_id_list: IntList):
    """
    생성한 비디오의 ID와 리스트를 출력합니다.

    :param video_id_list: 비디오 리스트
    """
    for i in video_id_list:
        video = VideoOutput(i)
        if not video.is_exists():
            continue

        video.load()
        print(f'{i}. {video.model.name}')
        print(f'  Video Name : {video.model.video_name}')
        print(f'  Video Description : {video.model.video_description}')
        print()
