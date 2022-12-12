import numpy as np

class VectorField():
    """Vector field class to store direction field
    of deformation """
    def __init__(self, vectors):
        # vectors is a np array of 2d vectors
        self.vectors = vectors

    def get_avg_vector(self):
        # Gets the resultant vector
        return sum(self.vectors)/max(1, len(self.vectors))
    
    def get_magnitude(self):
        # Gets overall magnitude of vector field
        avg_vector = self.get_avg_vector()
        return self.interpolate_data(avg_vector.T @ avg_vector)

    def interpolate_data(self, num):
        # Interpolates data to f/t data readings
        intercept = -1.29
        coef = -0.89
        return intercept + coef*np.log(num)
    
    def get_direction(self):
        # Get normalized direction of resultant vector
        unit_vector = self.get_avg_vector()/self.get_magnitude()
        return unit_vector