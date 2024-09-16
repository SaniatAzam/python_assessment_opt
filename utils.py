from storage import Storage


def create_data_file(data_file: str, store: Storage) -> None:
    """
    Accesses the JSON file and loads the data into the Storage object. If the file doesn't exist, it creates it.

    Assumptions:
        - There are no Task objects to be loaded to the Storage object if the JSON Dataset does not exist in the first place.

    Parameters:
        - data_file: str
            file path
        - store: Storage
            storage object

    Returns:
        - None
    """

    try:
        with open(data_file, "r") as f:
            # Case where the file exists but there is no data.
            if f.read(1) == '':
                raise FileNotFoundError
            else:
                store.load_tasks(f)
    except FileNotFoundError:
        with open(data_file, "w") as f:
            f.write("[]")


def update_data_file(data_file: str, store: Storage) -> None:
    try:
        with open(data_file, "w") as f:
            store.dump(f)
    except FileNotFoundError:
        pass


