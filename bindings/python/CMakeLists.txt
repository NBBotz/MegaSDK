find_package(SWIG REQUIRED)
set(UseSWIG_MODULE_VERSION 2)
include(UseSWIG)

if(DEFINED PYTHON3_EXECUTABLE AND NOT DEFINED Python3_EXECUTABLE)
    set(Python3_EXECUTABLE "${PYTHON3_EXECUTABLE}" CACHE FILEPATH "Python 3 interpreter" FORCE)
endif()

find_package(Python3 REQUIRED COMPONENTS Interpreter Development.Module)

# Set the output directory for generated Python files
set(PYTHON_OUTPUT_DIR ${CMAKE_BINARY_DIR}/bindings/python)

# Define the interface file and its properties
set(SWIG_INTERFACE_FILE ${CMAKE_CURRENT_LIST_DIR}/../megaapi.i)
set_source_files_properties(${SWIG_INTERFACE_FILE} PROPERTIES
    CPLUSPLUS ON
)
set_property(SOURCE ${SWIG_INTERFACE_FILE} PROPERTY SWIG_USE_TARGET_INCLUDE_DIRECTORIES TRUE)

set(SWIG_COMPILE_OPTIONS -c++;-py3;-USWIGJAVA)
if(ENABLE_SYNC)
    list(APPEND SWIG_COMPILE_OPTIONS -DENABLE_SYNC)
endif()

if(USE_LIBUV)
    list(APPEND SWIG_COMPILE_OPTIONS -DHAVE_LIBUV)
endif()

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

set(SDKPYTHON_SWIG_DEFINES)
if(ENABLE_SYNC)
    list(APPEND SDKPYTHON_SWIG_DEFINES ENABLE_SYNC)
endif()

if(USE_LIBUV)
    list(APPEND SDKPYTHON_SWIG_DEFINES HAVE_LIBUV)
endif()

set_property(TARGET SDKPythonBindings PROPERTY SWIG_COMPILE_DEFINITIONS ${SDKPYTHON_SWIG_DEFINES})

set_property(TARGET SDKPythonBindings PROPERTY SWIG_INCLUDE_DIRECTORIES
    ${CMAKE_CURRENT_LIST_DIR}/../../include
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