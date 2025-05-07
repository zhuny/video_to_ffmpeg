def ask_confirm(prompt):
    answer = input(f'{prompt} (Y if so) ')
    return answer.lower() == 'y'


def get_default_or_input(description, default_value,
                         *,
                         value_type=str):
    print(f'{description} : {default_value}')
    typed = input('New value or empty ("{}" => original text) ')
    typed = typed.replace("{}", str(default_value))

    if typed:
        return getattr(value_type, 'validate', value_type)(typed)
    else:
        return default_value
