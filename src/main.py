from cleaning_loading_app import cleaner_loader

if __name__ == "__main__":
    import logging

    logging.getLogger().setLevel(logging.INFO)

    cleaner_loader.ingest_files()
