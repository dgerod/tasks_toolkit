cmake_minimum_required(VERSION 2.8.3)
project(tasks_toolkit)

find_package(catkin REQUIRED COMPONENTS
  rospy
)

catkin_python_setup()

catkin_package(
  LIBRARIES ${PROJECT_NAME}
  CATKIN_DEPENDS rospy
  DEPENDS
)
