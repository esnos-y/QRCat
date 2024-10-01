import subprocess as sp
import sys
from pathlib import Path
import argparse
import platform


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
    parser.add_argument("--target-i386",
                        help="Pass compiler and linker flags to cross compile for i386 on Linux via MultiArch",
                        action="store_true")
    args = parser.parse_args()

    cert_thumb = args.cert_thumb
    cpack_out_dir = args.cpack_out_dir
    target_i386 = args.target_i386

    if target_i386 and platform.system() != "Linux":
        print(
            "Targeting i386 via this script is only valid on Linux, if on Windows please use the x86 native development CMD instead to target x86",
            file=sys.stderr)
        return 1

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

    # https://wiki.debian.org/Multiarch/Compiling?action=recall&rev=9
    if target_i386:
        config_cmd += [
            "-DCMAKE_C_FLAGS=-m32",
            "-DCMAKE_CXX_FLAGS=-m32",
            "-DCMAKE_Fortran_FLAGS=-m32",
            "-DCMAKE_EXE_LINKER_FLAGS=-m32",
            "-DCMAKE_MODULE_LINKER_FLAGS=-m32",
            "-DCMAKE_SHARED_LINKER_FLAGS=-m32",
            "-DCMAKE_ASM-ATT_FLAGS=-m32"
        ]

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
