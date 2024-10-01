import subprocess as sp
from pathlib import Path
import argparse


def main():
    parser = argparse.ArgumentParser(description="Build and package a release build")
    parser.add_argument("--build-dir", required=True)
    parser.add_argument("--cpack-out-dir", help="Directory to store resultant CPack packages", required=True)
    parser.add_argument("--generator", help="A valid CPack generator", required=True)
    parser.add_argument("--pack-source", help="Create a source package instead of building the project",
                        action="store_true")
    parser.add_argument("--cert-thumb",
                        help="MD1 thumbprint of the Certum Cloud Certificate to use for signing binaries on Windows",
                        required=False)
    args = parser.parse_args()
    cert_thumb = args.cert_thumb

    cpack_out_dir = args.cpack_out_dir

    parent_dir = Path(__file__).parent
    source_dir = parent_dir
    build_dir = Path(args.build_dir)
    source_dir_posix = source_dir.as_posix()
    build_dir_posix = build_dir.as_posix()

    config_cmd = ["cmake",
                  "-G",
                  "Ninja",
                  "-DCMAKE_BUILD_TYPE=Release",
                  "-S",
                  source_dir_posix,
                  "-B",
                  build_dir_posix]
    if cert_thumb:
        config_cmd += [f"-DQRCAT_CERTUM_CLOUD_CERT_MD1_THUMBPRINT={cert_thumb}"]
    sp.run(config_cmd, check=True)
    if not args.pack_source:
        build_cmd = ["cmake", "--build", build_dir_posix]
        sp.run(build_cmd, check=True)
    cpack_cmd = ["cpack", "-G", args.generator, "-B", cpack_out_dir]
    if args.pack_source:
        cpack_cmd += ["--config", "CPackSourceConfig.cmake"]
    sp.run(cpack_cmd, check=True, cwd=build_dir)
    return 0


if __name__ == "__main__":
    exit(main())
