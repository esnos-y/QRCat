import os
import sys
import subprocess as sp


def main():
    if len(sys.argv) != 3:
        print("Expected arguments: CERTUM_CLOUD_CERT_THUMBPRINT /path/to/exes/and/dlls/inside", file=sys.stderr)
        return 1

    cert_thumb = sys.argv[1]
    bin_dir = sys.argv[2]
    bin_paths = []
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
         "https://time.certum.pl",
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
