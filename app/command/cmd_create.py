from app.core.models import VideoOutput


def ask_confirm(prompt):
    answer = input(f'{prompt} (Y if so)')
    return answer.lower() == 'y'


def get_default_or_input(description, default_value):
    print(f'{description} : {default_value}')
    typed = input('New value or empty ("{}" => original text)')
    typed = typed.replace("{}", default_value)
    return typed or default_value


def run():
    """
    새로운 Output Video를 생성합니다.
    """

    for i in range(1000):
        video = VideoOutput(i)
        if video.is_exists():
            continue

        name = input("Video Name : ")

        video_name = ""
        video_description = ""

        if ask_confirm("Preset by SMM2 API?"):
            level_code = input("SMM2 Level Code : ")
            level_info = load_smm2_level_info(level_code)
            video_name = get_video_name(**level_info)
            video_description = get_video_description(**level_info)

        video_name = get_default_or_input("Video Name", video_name)
        video_description = get_default_or_input("Video Description", video_description)

        video.update_meta(
            name=name,
            video_name=video_name,
            video_description=video_description
        )
        video.save()
        print(f"New Video ID: {i} ({name})")
        break
