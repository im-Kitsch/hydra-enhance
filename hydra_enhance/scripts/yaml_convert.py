import argparse
import pathlib
from ..generate_dataclass import generate_structured_default_list


def main():
    parser = argparse.ArgumentParser(description="Hydra")
    parser.add_argument("--file", "-f", type=str)

    args = parser.parse_args()

    str_list = generate_structured_default_list(args.file)

    f_path = pathlib.Path(args.file)
    target_file = f_path.parent / f"{f_path.stem}_cfg.py"
    with open(target_file, 'w') as f:
        f.writelines(str_list)
    return


if __name__ == '__main__':
    main()
