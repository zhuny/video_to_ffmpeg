from app.core.models import VideoOutput


def run(name: str):
    """
    새로운 Output Video를 생성합니다.

    :param name: 생성할 비디오의 이름
    """

    for i in range(1000):
        video = VideoOutput(i)
        if video.is_exists():
            continue

        video.create(name)
        print(f"New Video ID: {i} ({name})")
        break
