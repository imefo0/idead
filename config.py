from pathlib import Path

home = Path.home()

# XDG folders
folder_config = home / ".config" / "idead"
folder_data = home / ".local" / "share" / "idead"
folder_cache = home / ".cache" / "idead"

# Other folders
folder_ideas = folder_data / "ideas"
folder_posts = folder_data / "posts"
folder_tasks = folder_data / "tasks"
folder_guides = folder_data / "guides"

ideas_format = "md"

warning_choice = True

separator_length = 30
separator_symbol = "-"

delete_idea_ask = "Are you sure you want to delete this idea?"

ideas_version = "1.0"
