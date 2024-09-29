import os
import shutil
import subprocess as sp
from pathlib import Path
import sys
from typing import Optional


def print_help(file):
    print("Valid usages:", file=file)
    print("Without vcpkg: build_release.py", file=file)
    print("With vcpkg: build_release.py --vcpkg /path/to/vcpkg", file=file)
    print("Print this help message: build_release.py --help", file=file)


def main():
    # Yes I know argparse exists
    vcpkg_root_posix: Optional[str] = None
    if len(sys.argv) == 3:
        if sys.argv[1] == "--vcpkg":
            vcpkg_root = Path(sys.argv[2])
            if not vcpkg_root.exists() or not vcpkg_root.is_dir() or not vcpkg_root.is_absolute():
                print("Provided vcpkg root does not exist or is not a directory or is not an absolute path",
                      file=sys.stderr)
                return 1
            vcpkg_root_posix = vcpkg_root.as_posix()
        else:
            print_help(sys.stderr)
            return 1
    elif len(sys.argv) == 2:
        if sys.argv[1] == "--help":
            print_help(sys.stdout)
            return 0
        else:
            print_help(sys.stderr)
            return 1

    source_dir = Path(__file__).parent
    build_dir = source_dir / "build"
    source_dir_posix = source_dir.as_posix()
    build_dir_posix = build_dir.as_posix()
    if build_dir.exists():
        answer = input("Build directory exists, confirm remove? Y to confirm/Anything else to abort\n")
        if answer.lower().strip() == "y":
            shutil.rmtree(build_dir)
        else:
            print("Aborting...")
            return 1
    if vcpkg_root_posix is not None:
        os.environ["VCPKG_ROOT"] = vcpkg_root_posix
        os.environ["PATH"] = vcpkg_root_posix + os.pathsep + os.environ["PATH"]
        os.environ["CMAKE_TOOLCHAIN_FILE"] = f"{vcpkg_root_posix}/scripts/buildsystems/vcpkg.cmake"

    config_cmd = ["cmake",
                  "-G",
                  "Ninja",
                  "-DCMAKE_BUILD_TYPE=Release",
                  "-S",
                  source_dir_posix,
                  "-B",
                  build_dir_posix]
    sp.run(config_cmd, check=True)
    build_cmd = ["cmake", "--build", build_dir_posix]
    sp.run(build_cmd, check=True)
    cpack_cmd = ["cpack", "-G", "ZIP"]
    sp.run(cpack_cmd, check=True, cwd=build_dir)
    return 0


if __name__ == "__main__":
    exit(main())
