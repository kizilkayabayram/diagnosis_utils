#include <plugin_test_preprocessor/first_preprocessor.h>

namespace plugin_test_preprocessor
{
FirstPreprocessor::FirstPreprocessor()
{
}

void FirstPreprocessor::initialize(tug_robot_control::RobotHardware* robot_hardware, const ros::NodeHandle & nh, std::string name)
{
}

bool FirstPreprocessor::process(const ros::Time& time, const ros::Duration& period)
{
//  ROS_INFO("preprocess()");
  return false;
}
}

PLUGINLIB_EXPORT_CLASS(plugin_test_preprocessor::FirstPreprocessor, tug_plugin_manager::RegularPlugin)
