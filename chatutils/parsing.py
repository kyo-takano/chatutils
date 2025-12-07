import re


def get_completion(response, *args, **kwargs):
    return response.choices[0].message.content


def parse(text, pattern=r"```(?:\w+)?\n([\s\S]*?)```", delimiter="```", index=None):
    if not (pattern or delimiter):
        raise ValueError("Specify `pattern` (regex) or `delimiter`.")

    if not pattern:
        if isinstance(delimiter, str):
            start = end = delimiter
        elif isinstance(delimiter, (list, tuple)):
            start, end = delimiter
        else:
            raise NotImplementedError(
                f"Delimiter type {type(delimiter)} not supported."
            )
        pattern = f"{re.escape(start)}([\\s\\S]*?){re.escape(end)}"

    matches = re.findall(pattern, text)
    if not matches:
        return []

    if isinstance(index, int):
        try:
            return matches[index]
        except IndexError:
            return []

    return matches
