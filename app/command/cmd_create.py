import requests

from app.core.models import VideoOutput


def ask_confirm(prompt):
    answer = input(f'{prompt} (Y if so) ')
    return answer.lower() == 'y'


def get_default_or_input(description, default_value):
    print(f'{description} : {default_value}')
    typed = input('New value or empty ("{}" => original text) ')
    typed = typed.replace("{}", default_value)
    return typed or default_value


class SMM2Controller:
    @classmethod
    def load_smm2_level_info(cls, level_code):
        level_code = level_code.upper().replace('-', '')
        try:
            response = requests.get(
                f"https://tgrcode.com/mm2/level_info/{level_code}"
            )
            return response.json()
        except Exception:
            print("Cannot load")

    @classmethod
    def get_video_name(cls, name, uploader, **kwargs):
        return f"{name} by {uploader['name']}"

    @classmethod
    def get_video_description(cls, name, course_id, uploader, **kwargs):
        return (
            f"Course Name : {name}\n"
            f"Course ID : {cls._with_dash(course_id)}\n"
            f"Maker : {uploader['name']} ({cls._with_dash(uploader['code'])})"
        )

    @classmethod
    def _with_dash(cls, level_code):
        return '-'.join([
            level_code[:3],
            level_code[3:6],
            level_code[6:]
        ])


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
            level_info = SMM2Controller.load_smm2_level_info(level_code)
            if level_info:
                video_name = SMM2Controller.get_video_name(**level_info)
                video_description = SMM2Controller.get_video_description(**level_info)

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
