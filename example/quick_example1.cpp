#include <iostream>
#include <fstream>
#include <sstream> 
#include <glog/logging.h>
#include "TOPPInstance.hpp"

int read_topp_input(std::string& trajectory_string, std::string& constraint_string) {
  std::ifstream ft("../trajectory_string");
  std::stringstream ft_ss;
  ft_ss << ft.rdbuf();
  ft.close();
  trajectory_string = ft_ss.str();
  // LOG(INFO) << ft_ss.str();
  std::ifstream fc("../constraint_string");
  std::stringstream fc_ss;
  fc_ss << fc.rdbuf();
  fc.close();
  constraint_string = fc_ss.str();
  return 0;
}

int write_topp_output(const std::string& resprofilesliststring, const std::string& switchpointsliststring, const std::string& restrajectorystring) {
  std::ofstream fp("../profiles_list");
  fp.write(resprofilesliststring.c_str(), resprofilesliststring.size());
  fp.close();
  std::ofstream fs("../switchpoints_list");
  fs.write(switchpointsliststring.c_str(), switchpointsliststring.size());
  fs.close();
  std::ofstream fr("../result_trajectory");
  fr.write(restrajectorystring.c_str(), restrajectorystring.size());
  fr.close();
  return 0;
}

int solve_topp_example1() {
  int ret = 0;
  std::string trajectory_string, constraint_string;
  read_topp_input(trajectory_string, constraint_string);
  TOPPInstance ti("QuadraticConstraints", constraint_string, trajectory_string);
  ret = ti.RunComputeProfiles(0, 0);
  LOG(INFO) << ret;
  ret = ti.ReparameterizeTrajectory();
  LOG(INFO) << ret;
  ti.WriteProfilesList();
  ti.WriteSwitchPointsList();
  ti.WriteResultTrajectory();
  write_topp_output(ti.resprofilesliststring, ti.switchpointsliststring, ti.restrajectorystring);
  return 0;
}

// int solve_topp3() {
//   int ret = 0;
//   std::string trajectory_string, constraint_string;
//   read_topp_input(trajectory_string, constraint_string);

// }

int main() {
  int ret = 0;
  solve_topp_example1();
  return 0;
}