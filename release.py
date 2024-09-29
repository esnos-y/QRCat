import os
import shutil
import subprocess as sp
from pathlib import Path
import sys


def main():
    cert_thumb = None
    if len(sys.argv) == 2:
        cert_thumb = sys.argv[1]
        print(f"Using {cert_thumb} as certificate thumbprint")

    parent_dir = Path(__file__).parent
    source_dir = parent_dir
    build_dir = parent_dir / "build"
    source_dir_posix = source_dir.as_posix()
    build_dir_posix = build_dir.as_posix()
    if build_dir.exists():
        answer = input("Build directory exists, confirm remove? Y to confirm/Anything else to abort\n")
        if answer.lower().strip() == "y":
            shutil.rmtree(build_dir)
        else:
            print("Aborting...")
            return 1

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
    if cert_thumb is not None:
        os.environ["QRCAT_CERTUM_CLOUD_CERT_THUMB"] = cert_thumb
    sp.run(cpack_cmd, check=True, cwd=build_dir)
    return 0


if __name__ == "__main__":
    exit(main())
