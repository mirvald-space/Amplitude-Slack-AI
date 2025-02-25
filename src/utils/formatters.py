def convert_to_slack_markdown(text: str) -> str:
    """
    Преобразование Markdown от OpenAI в Slack-совместимый mrkdwn.

    Args:
        text: Текст в формате Markdown

    Returns:
        str: Текст в формате Slack mrkdwn
    """
    lines = text.split("\n")
    result = []
    for line in lines:
        line = line.strip()
        if not line:
            result.append("")
            continue
        if line.startswith("# "):
            result.append(f"*{line[2:]}*")
        elif line.startswith("## "):
            result.append(f"*{line[3:]}*")
        elif line.startswith("### "):
            result.append(f"*{line[4:]}*")
        elif "**" in line:
            line = line.replace("**", "*")
            result.append(line)
        else:
            result.append(line)
    return "\n".join(result)
