import numpy as np


class SDE():
	"""
	Calculates Drift and Diffusion derrived from 
	general form of Stochastic Differential Equation

	Input params
	------------
	X : list, numpy.ndarray
		time series data 
	t_int : float
		time step in time series
	dt : float
		analysis time step
	inc = 0.01 : float
		max increment for binning thae data

	returns:
	----------
	diff : numpy.ndarray
		diffusion in time series
	drift : numpy.ndarray
		drift in time series
	avgdiff : numpy.ndarray
		avarage diffusion
	avgdrift : numpy.ndarray
		average drift
	"""
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)

	def _drift(self, X, t_int, dt):
		"""
		Calculate Diffusion.

		Input params:
		-------------
		X : list, numpy.ndarray
			Time Series data
		t_int : float
			time step in time series data
		dt : float	
			analysis time step

		returns:
		------------
		diff : numpy.ndarray
			Diffusion in time series
		"""
		return np.array([b - a for a, b in zip(X, X[dt:])]) / (t_int * dt)

	def _diffusion(self, X, t_int, delta_t=1):
		"""
		Calculates Drift

		Input params:
		-------------
		X : list, numpy.ndarray
			time series data 
		t_int : float
			time step in time series
		dt : float
			analysis time step

		retruns:
		-------------
		drift : numpy.ndarray
			Drift in time series
		"""
		return np.square(np.array([b - a for a, b in zip(X, X[delta_t:])
								   ])) / (t_int * delta_t)

	def _diffusion_xy(self, vel_x, vel_y, t_int, delta_t):
		return np.array([(b - a) * (d - c) for a, b, c, d in zip(
			vel_x, vel_x[delta_t:], vel_y, vel_y[delta_t:])
						 ]) / (delta_t * t_int)

	def _drift_and_diffusion(self, X, t_int, dt, delta_t=1, inc=0.01):
		"""
		Calcualtes drift, diffusion, average drift and avarage difussion.

		Input params:
		--------------
		X : list, numpy.ndarray
			time series data
		t_int : float
			time step in time series
		dt : float
			analysis time step
		inc = 0.01 : float
			max increment for binning thae data

		returns:
		--------------
		diff : numpy.ndarray
			diffusion in time series
		drift : numpy.ndarray
			drift in time series
		avgdiff : numpy.ndarray
			avarage diffusion
		avgdrift : numpy.ndarray
			average drift
		"""
		#op = np.arange(-1,1,inc)
		op = np.arange(min(X), max(X), inc)
		avgdiff, avgdrift = [], []
		drift = self._drift(X, t_int, dt)
		diff = self._diffusion(X, t_int, delta_t=delta_t)
		X = X[0:-max(dt, delta_t)]
		for b in op:
			i = np.where(np.logical_and(X < (b + inc), X >= b))[0]
			avgdiff.append(diff[i].mean())
			avgdrift.append(drift[i].mean())
		return diff, drift, np.array(avgdiff), np.array(avgdrift), op

	"""
	def _scalar_drift(self, X, t_int, dt, inc=0.01):
		op = np.arange(min(X), max(X), inc)
		avgdrift = []
		drift = self._drift(X, t_int, dt)
		X = X[0:-dt]
		for b in op:
			i = np.where(np.logical_and(X < (b + inc), X >= b))[0]
			avgdrift.append(drift[i].mean())
		return [avgdrift, op]

	def _scalar_diff(self, X, t_int, delta_t, inc=0.01):
		op = np.arange(min(X), max(X), inc)
		avgdiff = []
		diff = self._diffusion(X, t_int, delta_t=delta_t)
		X = X[0:-delta_t]
		for b in op:
			i = np.where(np.logical_and(X < (b + inc), X >= b))[0]
			avgdiff.append(diff[i].mean())
		return [avgdiff, op]
	"""

	def _vector_drift_diff(self,
						   vel_x,
						   vel_y,
						   inc_x=0.1,
						   inc_y=0.1,
						   t_int=0.12,
						   dt=40,
						   delta_t=1):
		op_x = np.arange(min(min(vel_x), min(vel_y)), max(max(vel_x), max(vel_y)), inc_x)
		op_y = np.arange(min(min(vel_x), min(vel_y)), max(max(vel_x), max(vel_y)), inc_y)
		#op_x = np.arange(-1, 1, inc_x)
		#op_y = np.arange(-1, 1, inc_y)

		driftX = self._drift(vel_x, t_int, dt)
		driftY = self._drift(vel_y, t_int, dt)
		diffusionX = self._diffusion(vel_x, t_int, delta_t)
		diffusionY = self._diffusion(vel_y, t_int, delta_t)
		diffusionXY = self._diffusion_xy(vel_x, vel_y, t_int, delta_t)

		avgdriftX = np.zeros((len(op_x), len(op_y)))
		avgdriftY = np.zeros((len(op_x), len(op_y)))
		avgdiffX = np.zeros((len(op_x), len(op_y)))
		avgdiffY = np.zeros((len(op_x), len(op_y)))
		avgdiffXY = np.zeros((len(op_x), len(op_y)))

		m = 0
		vel_x_, vel_y_ = vel_x[0:-max(dt, delta_t)], vel_y[0:-max(dt, delta_t)]
		for bin_x in op_x:
			n = 0
			for bin_y in op_y:
				i = np.where(
					np.logical_and(
						np.logical_and(vel_x_ < (bin_x + inc_x),
									   vel_x_ >= bin_x),
						np.logical_and(vel_y_ < (bin_y + inc_y),
									   vel_y_ >= bin_y)))[0]
				avgdriftX[n, m] = np.nanmean(driftX[i])
				avgdriftY[n, m] = np.nanmean(driftY[i])
				avgdiffX[n, m] = np.nanmean(diffusionX[i])
				avgdiffY[n, m] = np.nanmean(diffusionY[i])
				avgdiffXY[n, m] = np.nanmean(diffusionXY[i])
				n = n + 1
			m = m + 1
		return avgdriftX, avgdriftY, avgdiffX, avgdiffY, avgdiffXY, op_x, op_y

	"""
	def _vector_drift(self,
					  vel_x,
					  vel_y,
					  inc_x=0.1,
					  inc_y=0.1,
					  t_int=0.12,
					  dt=40):
		op_x = np.arange(-1, 1, inc_x)
		op_y = np.arange(-1, 1, inc_y)

		driftX = self._drift(vel_x, t_int, dt)
		driftY = self._drift(vel_y, t_int, dt)

		avgdriftX = np.zeros((len(op_x), len(op_y)))
		avgdriftY = np.zeros((len(op_x), len(op_y)))

		m = 0
		vel_x_, vel_y_ = vel_x[0:-dt], vel_y[0:-dt]
		for bin_x in op_x:
			n = 0
			for bin_y in op_y:
				i = np.where(
					np.logical_and(
						np.logical_and(vel_x_ < (bin_x + inc_x),
									   vel_x_ >= bin_x),
						np.logical_and(vel_y_ < (bin_y + inc_y),
									   vel_y_ >= bin_y)))[0]
				avgdriftX[n, m] = np.nanmean(driftX[i])
				avgdriftY[n, m] = np.nanmean(driftY[i])
				n = n + 1
			m = m + 1
		return [avgdriftX, avgdriftY, op_x, op_y]

	def _vector_diff(self,
					 vel_x,
					 vel_y,
					 inc_x=0.1,
					 inc_y=0.1,
					 t_int=0.12,
					 delta_t=1):
		op_x = np.arange(-1, 1, inc_x)
		op_y = np.arange(-1, 1, inc_y)

		diffusionX = self._diffusion(vel_x, t_int, delta_t)
		diffusionY = self._diffusion(vel_y, t_int, delta_t)

		avgdiffX = np.zeros((len(op_x), len(op_y)))
		avgdiffY = np.zeros((len(op_x), len(op_y)))

		m = 0
		vel_x_, vel_y_ = vel_x[0:-delta_t], vel_y[0:-delta_t]
		for bin_x in op_x:
			n = 0
			for bin_y in op_y:
				i = np.where(
					np.logical_and(
						np.logical_and(vel_x_ < (bin_x + inc_x),
									   vel_x_ >= bin_x),
						np.logical_and(vel_y_ < (bin_y + inc_y),
									   vel_y_ >= bin_y)))[0]
				avgdiffX[n, m] = np.nanmean(diffusionX[i])
				avgdiffY[n, m] = np.nanmean(diffusionY[i])
				n = n + 1
			m = m + 1
		return [avgdiffX, avgdiffY, op_x, op_y]
	"""

	def __call__(self, X, t_int, dt, delta_t=1, inc=0.01, **kwargs):
		"""
		Calcualtes drift, diffusion, average drift and avarage difussion.

		Input params:
		--------------
		X : list, numpy.ndarray
			time series data
		t_int :float
			time step in time series
		dt : float
			analysis time step
		inc = 0.01 : float
			max increment for binning thae data

		returns:
		--------------
		diff : numpy.ndarray
			diffusion in time series
		drift : numpy.ndarray
			drift in time series
		avgdiff : numpy.ndarray
			avarage diffusion
		avgdrift : numpy.ndarray
			avaerage drift
		"""
		self.__dict__.update(kwargs)
		return self._drift_and_diffusion(X, t_int, dt, inc)
