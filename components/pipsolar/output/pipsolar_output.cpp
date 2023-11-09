#include "pipsolar_output.h"
#include "esphome/core/log.h"
#include "esphome/core/helpers.h"
// #include <regex>

namespace esphome {
namespace pipsolar {

static const char *const TAG = "pipsolar.output";

void PipsolarOutput::write_state(float state) {
  char tmp[20];
  char cmdType = this->set_command_.back();

  if (cmdType != 'f') {
    sprintf(tmp, this->set_command_.c_str(), (int)state);
  } else {
    sprintf(tmp, this->set_command_.c_str(), state);
  }

  if (std::find(this->possible_values_.begin(), this->possible_values_.end(), state) != this->possible_values_.end()) {
    ESP_LOGI(TAG, "Will write: %s out of value %f / %03.1f", tmp, state, state);
    this->parent_->switch_command(std::string(tmp));
  } else {
    ESP_LOGI(TAG, "Will not write: %s as it is not in list of allowed values", tmp);
  }
}

void PipsolarOutput::write_complex_state(std::string state) {
  // std::regex p("([0-9]{2},[0-9]{2})");
  // if (not std::regex_match(state, p)) {
  //   ESP_LOGD(TAG, "Will not write state: %s, command mismatched.", state.c_str());
  //   return;
  // }

  ESP_LOGD(TAG, "Received complex state: %s", state.c_str());

  int tmp1, tmp2;
  sscanf(state.c_str(), "%d,%d", &tmp1, &tmp2);
  if (std::find(this->possible_values_.begin(), this->possible_values_.end(), tmp1) == this->possible_values_.end()) {
    ESP_LOGI(TAG, "Will not write, first complex: %s is out of allowed values.", tmp1);
    return;
  }
  if (std::find(this->possible_values_.begin(), this->possible_values_.end(), tmp2) == this->possible_values_.end()) {
    ESP_LOGI(TAG, "Will not write, second complex: %s is out of allowed values.", tmp2);
    return;
  }

  char command[20];
  sprintf(command, this->set_command_.c_str(), tmp1, tmp2);
  this->parent_->switch_command(std::string(command));
  ESP_LOGI(TAG, "Will write: %s out of value %d | %d", command, tmp1, tmp2);
}


}  // namespace pipsolar
}  // namespace esphome
