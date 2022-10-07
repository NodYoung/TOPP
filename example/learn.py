import logging
import numpy as np
import os, sys
sys.path.insert(0, os.path.join('..', 'src'))
import matplotlib.pyplot as plt
from scipy.interpolate import splev, splrep
from python.Trajectory import Polynomial, Chunk, PiecewisePolynomialTrajectory

# Utilities.InterpolateViapoints
def InterpolateViapoints():
  x = np.linspace(0, 10, 10)
  y = np.sin(x)
  tck = splrep(x, y, s=0.0)
  logging.info(tck)
  t = tck[0]
  chunkslist = []
  for i in range(len(t)-1):
    polylist = []
    if abs(t[i+1]-t[i])>1e-5:
      a = 1/6. * splev(t[i],tck,der=3)
      b = 0.5 * splev(t[i],tck,der=2)
      c = splev(t[i],tck,der=1)
      d = splev(t[i],tck,der=0)
      polylist.append(Polynomial([d,c,b,a]))
      # logging.info('d={}, c={}, b={}, a={}'.format(d, c, b, a))
      # logging.info(polylist[0].degree)
      chunkslist.append(Chunk(t[i+1]-t[i],polylist))
  # logging.info('len(chunkslist)={}'.format(len(chunkslist)))
  traj = PiecewisePolynomialTrajectory(chunkslist)
  logging.info('traj={}'.format(str(traj)))
  logging.info('traj={}'.format(traj.export_json()))
  xs = np.linspace(0, 10, 200)
  y_spl = splev(xs, tck)
  y_poly = [traj.Eval(x) for x in xs]
  plt.plot(x, y, 'o', color='r')
  plt.plot(xs, y_spl, color='g')
  plt.plot(xs, y_poly, color='b')
  plt.savefig('InterpolateViapoints.png')

if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO, format="%(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
  InterpolateViapoints()

    


