import os
import string
import sys
import subprocess as sp


def is_valid_thumb_print(thumb: str):
    if len(thumb) != 40:
        return False
    for c in thumb:
        if c not in string.hexdigits:
            return False
    return True


def main():
    if len(sys.argv) != 3:
        print("Expected arguments: /path/to/dir/with/exes/and/dlls/inside/ certum_cloud_cert_md1_thumbprint",
              file=sys.stderr)
        return 1

    cert_thumb = sys.argv[2]
    if not is_valid_thumb_print(cert_thumb):
        print("Invalid thumbprint", file=sys.stderr)
        return 1

    bin_dir = sys.argv[1]
    print(f"Signing binaries in {bin_dir}")
    bin_paths = []
    # NOTE: os.scandir is not recursive
    with os.scandir(bin_dir) as it:
        for entry in it:
            if entry.is_symlink():
                continue
            if entry.is_file():
                nl = entry.name.lower()
                if nl.endswith(".dll") or nl.endswith(".exe"):
                    bin_paths.append(entry.path)

    if len(bin_paths) == 0:
        print("No binaries found in directory", file=sys.stderr)
        return 1
    sp.run(
        ["signtool",
         "sign",
         "/sha1",
         cert_thumb,
         "/tr",
         "http://time.certum.pl",
         "/td",
         "sha256",
         "/fd",
         "sha256",
         *bin_paths
         ],
        check=True,
    )
    return 0


if __name__ == "__main__":
    exit(main())
