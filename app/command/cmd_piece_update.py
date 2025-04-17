import operator

from app.command.prompt import get_default_or_input
from app.core.model.video import VideoPieceModel, VideoOutput
from app.core.model.custom import VideoPoint


def run_read(video: VideoOutput):
    print("Piece List")
    for piece in video.model.piece_list:
        file_name = video.model.video_input[piece.file_id].name
        print(file_name, piece.start, piece.end)


def run_update(video: VideoOutput):
    run_read(video)

    piece_index = int(input('Piece > '))
    piece = video.model.piece_list[piece_index]
    piece.start = get_default_or_input(
        "시작 지점", piece.start,
        value_type=VideoPoint
    )
    piece.end = get_default_or_input(
        "끝 지점", piece.end,
        value_type=VideoPoint
    )


def run_sort(video: VideoOutput):
    video.model.piece_list.sort(
        key=operator.attrgetter('start')
    )


def run_delete(video: VideoOutput):
    run_read(video)
    piece_index = int(input("Delete Index > "))
    video.model.piece_list.pop(piece_index)


def run(function: str, video_id: int):
    """
    Piece를 수정합니다.

    :param function: 수정할 함수 이름 (read, update, split, sort)
    :param video_id: 비디오 ID
    """

    video = VideoOutput(video_id)
    if not video.is_exists():
        print("Video Not Exists!")
        return

    valid_func = {
        'read': run_read,
        'update': run_update,
        'sort': run_sort,
        'delete': run_delete
    }
    if function not in valid_func:
        print('Invalid Function Name')

    video.load()
    valid_func[function](video)
    video.save()
