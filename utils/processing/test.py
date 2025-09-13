import textwrap
import time


# Main function: wraps the text to fit within pixel width and max lines
def wrap_text_to_string(text, font, max_width, max_lines=3):
    lines = []  # Final lines to return
    current_line = ""  # Current line being built
    truncated = False

    words = text.split(" ")  # Split input by words (spaces)
    for word in words:
        # Process each word, possibly breaking it or appending it
        current_line, lines, was_truncated = process_word(
            word, current_line, lines, font, max_width, max_lines
        )
        if was_truncated:
            truncated = True
            break

    # Add remaining line if it exists and we still have space
    if current_line and len(lines) < max_lines:
        lines.append(current_line)

    # If overflow, add ellipsis
    lines = apply_ellipsis_if_needed(lines, font, max_width, truncated)

    # Remove trailing whitespaces
    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(line.rstrip())

    # Return result as a single string separated by newlines
    return "\n".join(cleaned_lines)


# Processes a single word and decides whether it fits, wraps, or breaks it
def process_word(word, current_line, lines, font, max_width, max_lines):
    word_with_space = (" " + word) if current_line else word
    test_line = current_line + word_with_space

    if font.measure(test_line) <= max_width:
        return test_line, lines, False  # Still fits on current line, no truncation

    if font.measure(word) > max_width:
        # Word too long to fit even alone (needs breaking)
        return break_long_word(word, current_line, lines, font, max_width, max_lines)
    else:
        # Doesn't fit current line, so push current line to result
        if current_line:
            lines.append(current_line)
        return (
            word + " ",
            lines,
            len(lines) >= max_lines,
        )  # Start new line with the word (truncated if full)


# Breaks a long word that can't fit on a single line
def break_long_word(word, current_line, lines, font, max_width, max_lines):
    if current_line:
        lines.append(current_line)

    # First, break using textwrap to split into smaller parts
    broken = textwrap.wrap(
        word, width=9999, break_long_words=True, break_on_hyphens=False
    )

    for piece in broken:
        if font.measure(piece) > max_width:
            # Still too long (break by characters)
            char_line = ""
            for c in piece:
                if font.measure(char_line + c) > max_width:
                    if char_line:
                        lines.append(char_line)
                    char_line = c
                    if len(lines) >= max_lines - 1:
                        return char_line, lines, True  # Truncated
                else:
                    char_line += c
            lines.append(char_line)
            current_line = ""
        else:
            # Fits now (add to lines)
            lines.append(piece)
            current_line = ""

        if len(lines) >= max_lines:
            return current_line, lines, True  # Truncated

    return current_line + " ", lines, False  # Still fits on current line, no truncation


# Appends "..." to the last line if the text was truncated
def apply_ellipsis_if_needed(lines, font, max_width, truncated):
    if not truncated or len(lines) == 0:
        return lines

    last_line = lines[-1].rstrip()
    while font.measure(last_line + "...") > max_width and last_line:
        last_line = last_line[:-1]
    lines[-1] = last_line + "..."
    return lines


def format_number_short(num):
    if num >= 1000000:
        return (
            f"{num / 1000000:.2f}".rstrip("0").rstrip(".") + "M"
        )  # convert to "M" format, eg 12555678 -> 1.26M
    elif num >= 1000:  # if between 1000 and 999999
        return (
            f"{num / 1000:.2f}".rstrip("0").rstrip(".") + "K"
        )  # convert to "K" format, eg 1015 -> 1.01K
    else:
        return str(num)


def time_ago_short(timestamp):
    now = time.time()
    diff = now - timestamp

    if diff < 60:
        return "New"  # less than a minute ago
    elif diff < 3600:
        return f"{int(diff // 60)}m"
    elif diff < 86400:
        return f"{int(diff // 3600)}h"
    elif diff < 7 * 86400:
        return f"{int(diff // 86400)}d"
    elif diff < 30 * 86400:
        return f"{int(diff // (7 * 86400))}w"
    elif diff < 365 * 86400:
        return f"{int(diff // (30 * 86400))}mo"
    else:
        return f"{int(diff // (365 * 86400))}y"