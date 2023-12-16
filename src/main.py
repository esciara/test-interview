from pathlib import Path

from icecream import ic

from cleaning_loading_app import cleaner_loader


if __name__ == "__main__":
    import argparse
    import logging

    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-file",
        help="Datafile to clean and load.",
    )
    args, beam_args = parser.parse_known_args()

    cleaner_loader.clean_and_load(Path(args.data_file))
