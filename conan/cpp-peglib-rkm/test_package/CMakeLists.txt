cmake_minimum_required(VERSION 3.14 FATAL_ERROR)
project("rkm-cpp-peglib-test_package" LANGUAGES CXX)

find_package("cpp-peglib" REQUIRED)
add_executable("testapp" "test.cc")
target_link_libraries("testapp" "cpp-peglib")
