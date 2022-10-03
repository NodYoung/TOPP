cmake_minimum_required(VERSION 3.10)
project(TOPP)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -pthread")

#glog
set(glog_INCLUDE_DIRS "/usr/include")
set(glog_LIBRARY_DIRS "/usr/lib/x86_64-linux-gnu")
set(glog_LIBS "glog")
include_directories(${glog_INCLUDE_DIRS})

#boost
find_package(Boost COMPONENTS system filesystem date_time)
message("boost include path: ${Boost_INCLUDE_DIRS}")
message("boost libraries: ${Boost_LIBRARIES}")
include_directories(${Boost_INCLUDE_DIRS})


include_directories(../src)
set (TOPP_CODE ../src/Errors.h ../src/KinematicLimits.h ../src/KinematicLimits.cpp ../src/TorqueLimits.h ../src/TorqueLimits.cpp 
              ../src/PolygonConstraints.h ../src/PolygonConstraints.cpp ../src/Trajectory.h ../src/Trajectory.cpp 
              ../src/TOPP.h ../src/TOPP.cpp TOPPInstance.hpp TOPPInstance.cpp)

add_library(TOPP SHARED ${TOPP_CODE} )
add_executable(quick_example1 quick_example1.cpp)
target_link_libraries(quick_example1 TOPP ${glog_LIBS} ${Boost_LIBRARIES})

