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

    file_name_tokenized = data_file.split(".")
    length_of_tokens = len(file_name_tokenized)
    extension = file_name_tokenized[length_of_tokens - 1]

    if extension != "json":
        raise ValueError(f"*** The file needs to have .json extension. ***"
                         f"\n Currently you are using a .{extension} extension, which is not supported. "
                         f"\n Please rename it to {'.'.join(file_name_tokenized[0:length_of_tokens-1])}.json")

    try:
        with open(data_file, "r") as f:
            # Case where the file exists but there is no data.
            # Just going to treat as if it doesn't exist
            if f.read(1) == '':
                raise FileNotFoundError
            else:
                try:
                    store.load_tasks(f)
                except ValueError as e:
                    raise e
    except FileNotFoundError:
        with open(data_file, "w") as f:
            f.write("[]")


def update_data_file(data_file: str, store: Storage) -> None:
    """
    Updates the specified data file with the tasks in storage's task dict

    Parameters:
        - data_file: str
            file path
        - store: Storage
            the storage object

    Returns:
        None
    """
    try:
        with open(data_file, "w") as f:
            store.dump(f)
    except FileNotFoundError:
        pass


