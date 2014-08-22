#ifndef FIRST_DEVICE_DRIVER_H_
#define FIRST_DEVICE_DRIVER_H_

#include <pluginlib/class_list_macros.h>
#include <tug_plugin_manager/plugin_base.h>
#include <tug_device_driver/tug_device_driver_base.h>
//#include <tug_controlled_device_driver/tug_controlled_device_driver_base.h>
//#include <tug_preprocessor/tug_preprocessor_base.h>
//#include <tug_postprocessor/tug_postprocessor_base.h>

namespace plugin_test_device_driver
{

class FirstDeviceDriver: public tug_device_driver::DeviceDriver
{
public:
  FirstDeviceDriver();

  virtual void initialize(std::string name);
  virtual std::string getName();

private:
  std::string temp_data_;
};
}

#endif
