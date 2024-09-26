cmake_minimum_required(VERSION 3.22)
project(QRCat_cmake_project)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

find_package(OpenCV REQUIRED CONFIG)
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
endif ()

install(TARGETS qrcat
        RUNTIME_DEPENDENCIES
        DIRECTORIES ${RUNTIME_DEPS_DIRS}
        PRE_EXCLUDE_REGEXES ${PRE_EXCLUDE_REGEXES}
        POST_EXCLUDE_REGEXES ${POST_EXCLUDE_REGEXES}
)
include(CPack)
