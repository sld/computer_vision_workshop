from headers import *

class Runner:
  def run_magnitude(self):
    viewer = GrayImgProcessingViewer('./data/saturn.jpg', FourierTransform())
    viewer.apply("magnitude_spectrum", {})
    plt.show()

  def run_phase(self):
    viewer = GrayImgProcessingViewer('./data/saturn.jpg', FourierTransform())
    viewer.apply("phase_spectrum", {})
    plt.show()

  def run_magnitude_spectrum_without_min(self):
    viewer = GrayImgProcessingViewer('./data/saturn.jpg', FourierTransform())
    viewer.apply("magnitude_spectrum_without_min", {'thresh': 7})
    plt.show()

  def run_magnitude_spectrum_without_max(self):
    viewer = GrayImgProcessingViewer('./data/saturn.jpg', FourierTransform())
    viewer.apply("magnitude_spectrum_without_max", {'thresh': 5})
    plt.show()

  def run_without_min_spectrum(self):
    viewer = GrayImgProcessingViewer('./data/saturn.jpg', FourierTransform())
    viewer.apply("img_without_min_spectrum", {'thresh': 7})
    plt.show()

  def run_without_max_spectrum(self):
    viewer = GrayImgProcessingViewer('./data/saturn.jpg', FourierTransform())
    viewer.apply("img_without_max_spectrum", {'thresh': 5})
    plt.show()

  def run_all(self):
    self.run_magnitude()
    self.run_phase()
    self.run_magnitude_spectrum_without_min()
    self.run_magnitude_spectrum_without_max()
    self.run_without_min_spectrum()
    self.run_without_max_spectrum()
