find_package(SWIG REQUIRED)
set(UseSWIG_MODULE_VERSION 2)
include(UseSWIG)

find_package(Python3 REQUIRED COMPONENTS Interpreter Development.Module)

# Set the output directory for generated Python files
set(PYTHON_OUTPUT_DIR ${CMAKE_BINARY_DIR}/bindings/python)

# Define the interface file and its properties
set(SWIG_INTERFACE_FILE ${CMAKE_CURRENT_LIST_DIR}/../megaapi.i)
set_source_files_properties(${SWIG_INTERFACE_FILE} PROPERTIES
    CPLUSPLUS ON
)
set_property(SOURCE ${SWIG_INTERFACE_FILE} PROPERTY SWIG_USE_TARGET_INCLUDE_DIRECTORIES TRUE)

# Set SWIG flags for generating Python code
if(ENABLE_SYNC)
    list(APPEND ADDITIONAL_SWIG_DEFINES -DENABLE_SYNC)
endif()

if(USE_LIBUV)
    list(APPEND ADDITIONAL_SWIG_DEFINES -DHAVE_LIBUV)
endif()

set(SWIG_COMPILE_OPTIONS -c++;-py3;-DPY3)
list(APPEND SWIG_COMPILE_OPTIONS ${ADDITIONAL_SWIG_DEFINES})
set_property(SOURCE ${SWIG_INTERFACE_FILE} PROPERTY SWIG_COMPILE_OPTIONS ${SWIG_COMPILE_OPTIONS})

# Generate Python bindings
swig_add_library(SDKPythonBindings
    TYPE MODULE
    LANGUAGE python
    SOURCES ${SWIG_INTERFACE_FILE}
    OUTPUT_DIR ${PYTHON_OUTPUT_DIR}
)

set_target_properties(SDKPythonBindings PROPERTIES
    POSITION_INDEPENDENT_CODE ON
    LIBRARY_OUTPUT_DIRECTORY ${PYTHON_OUTPUT_DIR}
    RUNTIME_OUTPUT_DIRECTORY ${PYTHON_OUTPUT_DIR}
    ARCHIVE_OUTPUT_DIRECTORY ${PYTHON_OUTPUT_DIR}
    SWIG_USE_SWIG_DEPENDENCIES ON
)

target_include_directories(SDKPythonBindings
    PRIVATE
    ${Python3_INCLUDE_DIRS}
    ${CMAKE_CURRENT_LIST_DIR}/../../include
)

target_link_libraries(SDKPythonBindings
    PRIVATE
    Python3::Module
    MEGA::SDKlib
)

# Generate Python wheel
set(SETUP_PYTHON_FILE ${CMAKE_CURRENT_LIST_DIR}/setup.py)

add_custom_target(build_wheel
    COMMAND ${Python3_EXECUTABLE} ${SETUP_PYTHON_FILE} bdist_wheel
    WORKING_DIRECTORY ${PYTHON_OUTPUT_DIR}
    DEPENDS SDKPythonBindings
    COMMENT "Building Python wheel..."
)