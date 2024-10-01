cmake_minimum_required(VERSION 3.22)
project(QRCat_cmake_project
        VERSION 0.0.1
        LANGUAGES CXX
)

set(QRCAT_CERTUM_CLOUD_CERT_MD1_THUMBPRINT "" CACHE STRING
        "Thumbprint of a Certum Cloud Certificate to sign binaries on Windows."
)

string(LENGTH "${QRCAT_CERTUM_CLOUD_CERT_MD1_THUMBPRINT}" THUMB_LENGTH)
if ("${QRCAT_CERTUM_CLOUD_CERT_MD1_THUMBPRINT}" STREQUAL "")
    set(SIGN_BINARIES OFF)
elseif ("${QRCAT_CERTUM_CLOUD_CERT_MD1_THUMBPRINT}" MATCHES "^[0-9A-Fa-f]*$" AND ${THUMB_LENGTH} EQUAL 40)
    set(SIGN_BINARIES ON)
else ()
    message(FATAL_ERROR "QRCAT_CERTUM_CLOUD_CERT_MD1_THUMBPRINT cache variable is not set to a 40 bytes hexadecimal string")
endif ()

find_package(OpenCV CONFIG REQUIRED)
find_library(ZBAR_LIB zbar REQUIRED)
#message(STATUS ${ZBAR_LIB})

# Print all CMake variables
# https://stackoverflow.com/a/9328525/27298874
#get_cmake_property(_variableNames VARIABLES)
#list (SORT _variableNames)
#foreach (_variableName ${_variableNames})
#    message(STATUS "${_variableName}=${${_variableName}}")
#endforeach()

#set(ZBAR_DIR "C:/Program Files (x86)/ZBar")

add_executable(qrcat qrcat.cpp)
set_target_properties(
        qrcat
        PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/bin
)
if (UNIX AND NOT APPLE)
    set_target_properties(
            qrcat
            PROPERTIES
            INSTALL_RPATH $ORIGIN/../lib
    )
endif ()
#target_include_directories(qrcat PRIVATE ${ZBAR_DIR}/include)
#target_link_directories(qrcat PRIVATE ${ZBAR_DIR}/lib)
target_link_libraries(qrcat PRIVATE ${OpenCV_LIBS} ${ZBAR_LIB})

set(PRE_EXCLUDE_REGEXES)
set(POST_EXCLUDE_REGEXES)
set(RUNTIME_DEPS_DIRS)

#list(APPEND RUNTIME_DEPS_DIRS ${OpenCV_DIR}/${OpenCV_ARCH}/${OpenCV_RUNTIME}/bin)
#list(APPEND RUNTIME_DEPS_DIRS ${ZBAR_DIR}/bin)

if (WIN32)
    list(APPEND PRE_EXCLUDE_REGEXES "^api-ms-.*$" "^ext-ms-.*$")
    list(APPEND POST_EXCLUDE_REGEXES "^.*system32/.*$")
    list(APPEND RUNTIME_DEPS_DIRS ${CMAKE_SYSTEM_LIBRARY_PATH})
elseif (UNIX AND NOT APPLE)
    list(APPEND PRE_EXCLUDE_REGEXES "^libc\\.so.*$" "^ld-linux-.*\\.so.*$")
endif ()

install(TARGETS qrcat
        RUNTIME_DEPENDENCIES
        DIRECTORIES ${RUNTIME_DEPS_DIRS}
        PRE_EXCLUDE_REGEXES ${PRE_EXCLUDE_REGEXES}
        POST_EXCLUDE_REGEXES ${POST_EXCLUDE_REGEXES}
)
if (UNIX AND NOT APPLE)
    configure_file(
            ${CMAKE_CURRENT_SOURCE_DIR}/scripts/set_libs_runpath.cmake.in
            ${CMAKE_CURRENT_BINARY_DIR}/scripts/set_libs_runpath.cmake
            @ONLY
    )
    install(SCRIPT ${CMAKE_CURRENT_BINARY_DIR}/scripts/set_libs_runpath.cmake)
endif ()
if (WIN32 AND ${SIGN_BINARIES})
    configure_file(
            ${CMAKE_CURRENT_SOURCE_DIR}/scripts/sign_binaries_windows.cmake.in
            ${CMAKE_CURRENT_BINARY_DIR}/scripts/sign_binaries_windows.cmake
            @ONLY
    )
    install(SCRIPT ${CMAKE_CURRENT_BINARY_DIR}/scripts/sign_binaries_windows.cmake)
endif ()
set(CPACK_PACKAGE_NAME QRCat)
set(CPACK_SOURCE_IGNORE_FILES
        /cmake-build-.*/
        /build/
        /\\\\.git/
        /\\\\.gitignore
        /\\\\.idea/
)
set(CPACK_PACKAGE_CHECKSUM SHA256)
include(CPack)
