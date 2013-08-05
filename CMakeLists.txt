project(bunsan_binlogs_python)

include(${CMAKE_SOURCE_DIR}/system-config.cmake OPTIONAL)

cmake_minimum_required(VERSION 2.8)

include(BunsanCommon)

bunsan_use_boost(system filesystem python thread)
bunsan_use_bunsan(binlogs)

set(Python_ADDITIONAL_VERSIONS "2.7" "2.6" "2.5")
find_package(PythonLibs)
include_directories(${PYTHON_INCLUDE_DIRS})
bunsan_use(${PYTHON_LIBRARIES})

bunsan_add_shared_library(${PROJECT_NAME}
    src/lib/Header.cpp
    src/lib/LogReader.cpp

    src/python/Header.cpp
)

bunsan_install_headers()
bunsan_install_targets(${PROJECT_NAME})

bunsan_include_tests()
