from app.core.models import VideoPoint, VideoOutput, VideoPieceModel


def run(video_id: int, file_id: int, start: VideoPoint, end: VideoPoint):
    """
    Video에 동영상 조각을 추가합니다.

    :param video_id: Video ID
    :param file_id: File ID
    :param start: 영상의 시작 시간
    :param end: 영상의 끝 시간
    """
    video = VideoOutput(video_id)
    if not video.is_exists():
        print("Video Not Exists!")
        return

    video.load()
    if not video.is_valid_file_id(file_id):
        print("Input Wrong!")
        return

    if end < start:
        print(f"Start({start}) should be earlier than End({end})")
        return

    piece = VideoPieceModel(
        file_id=file_id,
        start=start, end=end
    )
    video.add_piece(piece)
    video.save()
