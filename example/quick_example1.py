import logging
import numpy as np
import os, sys
sys.path.insert(0, os.path.join('..', 'src'))
from python import TOPPpy
from python import Trajectory
from python import Utilities

def save_topp_input(trajectorystring, constraintstring):
  with open('trajectory_string', 'w') as f:
    f.write(trajectorystring)
  with open('constraint_string', 'w') as f:
    f.write(constraintstring)

def load_topp_output():
  with open('profiles_list', 'r') as f:
    profiles_list = TOPPpy.ProfilesFromString(f.read())
  with open('switchpoints_list', 'r') as f:
    switchpoints_list = TOPPpy.SwitchPointsFromString(f.read())
  with open('result_trajectory', 'r') as f:
    traj1 = Trajectory.PiecewisePolynomialTrajectory.FromString(f.read())
  return profiles_list, switchpoints_list, traj1

# reference: [Kinematic limits (initial trajectory specified by via-points)](https://github.com/quangounet/TOPP/wiki/Quick-examples)
class QuickExample1(object):
  def __init__(self):
    # A two-dof path going through 5 viapoints (0,1) - (1,1) - (5,1) - (3,2) - (5,4)
    path = np.array([[0,1,5,3,5],[1,1,1,2,4]])
    self.traj0 = Utilities.InterpolateViapoints(path) # Interpolate using splines
    # Constraints
    self.vmax = 2*np.ones(self.traj0.dimension)  # Velocity limits
    self.amax = 10*np.ones(self.traj0.dimension) # Acceleration limits
    self.profiles_list = None
    self.switchpoints_list = None
    self.traj1 = None

  def save_traj_constrain(self):
    trajectorystring = str(self.traj0)
    discrtimestep = 0.005
    constraintstring = str(discrtimestep)
    constraintstring += "\n" + ' '.join([str(v) for v in self.vmax])
    constraintstring += TOPPpy.ComputeKinematicConstraints(self.traj0, self.amax, discrtimestep)
    save_topp_input(trajectorystring, constraintstring)
  
  def plot_topp_result(self):
    profiles_list, switchpoints_list, traj1 = load_topp_output()
    TOPPpy.PlotProfiles(profiles_list, switchpoints_list, 4)
    dtplot = 0.01
    TOPPpy.PlotKinematics(self.traj0, traj1, dtplot, self.vmax, self.amax)


# reference: [Kinematic limits (initial trajectory specified by trajectorystring)](https://github.com/quangounet/TOPP/wiki/Quick-examples)
class QuickExample2(object):
  def __init__(self):
    ndof = 5
    trajectorystring = """1.0
    5
    -0.495010 1.748820 -2.857899 1.965396
    0.008319 0.004494 1.357524 -1.289918
    -0.354081 1.801074 -1.820616 0.560944
    0.221734 -1.320792 3.297177 -2.669786
    -0.137741 0.105246 0.118968 -0.051712
    1.0
    5
    0.361307 1.929207 -4.349490 2.275776
    0.080419 -1.150212 2.511645 -1.835906
    0.187321 -0.157326 -0.355785 0.111770
    -0.471667 -2.735793 7.490559 -4.501124
    0.034761 0.188049 -1.298730 1.553443"""
    self.traj0 = Trajectory.PiecewisePolynomialTrajectory.FromString(trajectorystring)
    # Constraints
    self.vmax = 2*np.ones(ndof)  # Velocity limits
    self.amax = 10*np.ones(ndof) # Acceleration limits

  def save_traj_constrain(self):
    trajectorystring = str(self.traj0)
    discrtimestep = 0.01
    constraintstring = str(discrtimestep)
    constraintstring += "\n" + ' '.join([str(v) for v in self.vmax])
    constraintstring += TOPPpy.ComputeKinematicConstraints(self.traj0, self.amax, discrtimestep)
    save_topp_input(trajectorystring, constraintstring)
  
  def plot_topp_res(self):
    profiles_list, switchpoints_list, traj1 = load_topp_output()
    TOPPpy.PlotProfiles(profiles_list, switchpoints_list, 4)
    dtplot = 0.01
    TOPPpy.PlotKinematics(self.traj0, traj1, dtplot, self.vmax, self.amax)

class QuickExample3(object):
  def __init__(self):
    trajstr = """0.500000
      3
      0.0 0.0 -35.9066153846 47.930797594
      0.0 0.0 -0.645566686001 1.11351913336
      0.0 0.0 8.3609538376 -11.3580450529
      0.500000
      3
      0.0 0.1 -0.159247917034 0.0789972227119
      0.0 0.1 -32.7720979649 43.5627972865
      0.0 0.1 0.958473557774 -1.41129807703"""
    self.traj0 = Trajectory.PiecewisePolynomialTrajectory.FromString(trajstr)
    self.vmax = np.ones(3)
    self.accelmax = np.ones(3)

  def save_traj_constrain(self):
    trajectorystring = str(self.traj0)
    inertia = np.eye(3)
    discrtimestep = 1e-3
    constraintstring = str(discrtimestep)
    constraintstring += "\n" + ' '.join([str(a) for a in self.accelmax])
    for v in inertia:
      constraintstring += "\n" + ' '.join([str(i) for i in v])
    save_topp_input(trajectorystring, constraintstring)



if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO, format="%(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
  # qe1 = QuickExample1()
  # qe1.save_traj_constrain()
  # qe1.plot_topp_result()
  qe2 = QuickExample2()
  # qe2.save_traj_constrain()
  qe2.plot_topp_res()
  # qe3 = QuickExample3()
  # qe3.save_traj_constrain()
  
