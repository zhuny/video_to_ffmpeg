from app.core.model.video import VideoOutput


def run():
    """
    생성한 비디오의 ID와 리스트를 출력합니다.
    """
    for i in range(1000):
        video = VideoOutput(i)
        if not video.is_exists():
            break

        video.load()
        print(f'{i}. {video.model.name}')
        print(f'  Video Name : {video.model.video_name}')
        print(f'  Video Description : {video.model.video_description}')
        print()
