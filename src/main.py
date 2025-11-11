import os
import shutil


def generate_public():
    public = "./public"
    if os.path.exists(public):
        print("PATH EXISTS... removing")
        shutil.rmtree(public)
    copy_static("./static", "./public")


def copy_static(path, destination):
    print(f"CURRENT PATH: {path}")
    print(f"CURRENT DESTINATION: {destination}")
    if os.path.exists(path):
        print(f"ON PATH: {path}")
        static_contents = os.listdir(path)
        print(static_contents)
    for item in static_contents:
        if str(item).startswith("."):
            continue
        new_path = os.path.join(path, item)
        new_destination = os.path.join(destination, item)
        print(f"NEW DESTINATION: {new_destination}")
        if os.path.isdir(new_path):
            os.makedirs(f"{new_destination}")
            copy_static(new_path, new_destination)
        if os.path.isfile(new_path):
            os.makedirs(os.path.dirname(new_destination), exist_ok=True)
            shutil.copy(new_path, new_destination)


def main():
    generate_public()


if __name__ == "__main__":
    main()
