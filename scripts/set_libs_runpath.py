import os
import sys
import subprocess as sp


def main():
    if len(sys.argv) != 2:
        print("Expected arguments: /path/to/dir/with/elfs/inside", file=sys.stderr)
        return 1

    elfs_dir = sys.argv[1]
    print(f"Setting run paths for ELFs in: {elfs_dir}")
    # NOTE: os.scandir is not recursive
    with os.scandir(elfs_dir) as it:
        for entry in it:
            if entry.is_symlink():
                continue
            if entry.is_file():
                sp.run(["patchelf", "--set-rpath", "$ORIGIN", entry.path], check=True)
    return 0


if __name__ == "__main__":
    exit(main())
