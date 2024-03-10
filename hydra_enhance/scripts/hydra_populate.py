import argparse
from ..yaml_populate import populate_file


def main():
    parser = argparse.ArgumentParser(description="Hydra")
    parser.add_argument("--file", "-f", type=str)

    args = parser.parse_args()

    populate_file(args.file, False)
    return


if __name__ == "__main__":
    main()
