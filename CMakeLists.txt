project(bunsan_binlogs_python)

include(${CMAKE_SOURCE_DIR}/system-config.cmake OPTIONAL)

cmake_minimum_required(VERSION 2.8)

include(BunsanCommon)

bunsan_use_boost(system filesystem python thread)
bunsan_use_bunsan(binlogs)
bunsan_use_python2_libs_minimum(2.6)

bunsan_add_shared_library(${PROJECT_NAME}
    src/lib/Header.cpp
    src/lib/LogReader.cpp

    src/python/binlogs.cpp
)

bunsan_install_headers()
bunsan_install_python_module_target(TARGET ${PROJECT_NAME} MODULE bunsan.binlogs._binlogs)
bunsan_install_python_module_init(INIT src/python/__init__.py MODULE bunsan.binlogs)

bunsan_include_tests()
