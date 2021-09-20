def lint_config(config_data):
    # Verify config is a list.
    if type(config_data) != list:
        print("[Error] YAML data needs to be a list.")
        exit(1)

    number = 1

    # Verify each list item in config.
    for i in config_data:
        # Store the data in a separate variable, as we'll be removing the values
        # later to verify no extra keys are present in the config.
        list_data = i.copy()

        # Verify needed keys are present.
        for j in ["name", "data", "mask"]:
            if list_data.get(j) is None:
                print(f"[Error] List {number} is missing key '{j}'.")
                exit(1)
            else:
                list_data.pop(j)

        # Verify no extra keys are present.
        if list_data != {}:
            print(f"[Error] List {number} contains extra keys:")
            for j in list_data.keys():
                print(f"   [->] {j}")
            exit(1)

        # Verify the 'mask' key is a boolean.
        if i.get("mask") not in (True, False):
            print(f"[Error] Key 'mask' needs to be set to true or false.")
            exit(1)
