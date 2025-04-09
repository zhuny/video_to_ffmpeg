from decimal import Decimal


def run(video_id: int, file_id: int, start: Decimal, end: Decimal):
    """
    Video에 동영상 조각을 추가합니다.

    :param video_id: Video ID
    :param file_id: File ID
    :param start: 영상의 시작 시간
    :param end: 영상의 끝 시간
    """
