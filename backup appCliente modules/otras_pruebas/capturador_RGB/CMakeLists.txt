cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

project(openniViewer)

find_package(PCL 1.2 REQUIRED)


include_directories(${PCL_INCLUDE_DIRS})
include_directories(${GTEST_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})
add_compile_options(-lgtest)

#Agregado Rodrigo
list(REMOVE_ITEM PCL_LIBRARIES "vtkproj4")

add_executable (openniViewer openniViewer.cpp)
target_link_libraries (openniViewer ${PCL_LIBRARIES})