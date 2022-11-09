import inquirer
from rich import print as rprint

from tracklift.env import EnvNotFound
from tracklift.importers import IMPORTERS
from tracklift.main import Tracklift
from tracklift.trackers.cli_tracker import CliTracker

TITLE = """
____________________________________________________________________

████████ ██████   █████   ██████ ██   ██ ██      ██ ███████ ████████
   ██    ██   ██ ██   ██ ██      ██  ██  ██      ██ ██         ██
   ██    ██████  ███████ ██      █████   ██      ██ █████      ██
   ██    ██   ██ ██   ██ ██      ██  ██  ██      ██ ██         ██
   ██    ██   ██ ██   ██  ██████ ██   ██ ███████ ██ ██         ██

_____________________________________________________________________

            An easy way to export playlists to Spotify

"""


def main() -> None:
    rprint(f"{TITLE}")

    rprint("Which platform?")
    platforms = list(IMPORTERS.keys())
    platform = inquirer.list_input("", choices=platforms)
    tracker = CliTracker()
    try:
        tracklift = Tracklift(platform, tracker)
    except EnvNotFound as e:
        rprint(
            f"The required environment variable {e} is missing\n"
            "Please refer to the setup guide in the README.md"
        )
        exit(0)

    rprint("Which channel ID?")
    rprint(
        f"The channel ID is found at the end of the channel url - {tracklift.importer.channel_url()}<CHANNEL_ID>"
    )
    channel_id = inquirer.text("")

    all_playlists = tracklift.get_playlists(channel_id)
    all_playlists.insert(0, "all")  # type: ignore

    rprint(f"Tracklift found {len(all_playlists)}!\n")

    rprint("Please select the playlists you want to download?")
    playlists = inquirer.checkbox("playlists", choices=all_playlists)

    if "all" in playlists:
        playlists = all_playlists[1:]

    all_songs = tracklift.get_songs(playlists)
    total_songs_found = sum(len(e[1]) for e in all_songs)
    rprint(f"\nTracklift found {total_songs_found} songs!")
    rprint("Do you want to export these songs to Spotify?")
    export = inquirer.list_input("", choices=["Yes", "No"])

    if export:
        tracklift.add_songs(all_songs)
        rprint("\n")
        rprint(f"[underline bold]{' '*20}STATS{' '*20}")
        rprint("TOTAL")
        rprint(f"{' '*35}{total_songs_found}")
        rprint(f"[underline]{' '*45}")
        rprint("SUCCESSFUL")
        rprint(f"{' '*35}{len(tracker.succeeded)}")
        rprint(f"[underline]{' '*45}")
        rprint("UNSUCCESSFUL")
        rprint(
            f"{' '*35}{(len(tracker.already_exists + tracker.not_found + tracker.errored))}"
        )
        rprint("\n")
        rprint(f"{'Already exists'.ljust(34, ' ')} {len(tracker.already_exists)}")
        rprint(f"{'Unable to find song'.ljust(34, ' ')} {len(tracker.not_found)}")
        rprint(f"{'Unknown errors'.ljust(34, ' ')} {len(tracker.errored)}")
        rprint("\n")

        if len(tracker.already_exists + tracker.not_found + tracker.errored) > 0:
            rprint("Review songs that where not successfully exported?")
            see_errored = inquirer.list_input("", choices=["Yes", "No"])

            if see_errored == "Yes":
                for song in (
                    tracker.errored + tracker.not_found + tracker.already_exists
                ):
                    print(song)


if __name__ == "__main__":
    main()
