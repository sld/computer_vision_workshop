from headers import *

class FourierTransform:
  def magnitude_spectrum(self, img):
    log_magnitude = self.__get_log_magnitude(img)
    return self.__normalize(log_magnitude)

  def phase_spectrum(self, img):
    fourier_centered = self.__centered_fourier(img)
    angles_of_the_complex = np.angle(fourier_centered)
    return angles_of_the_complex

  def img_without_min_spectrum(self, img, kargs={'thresh': 5}):
    thresh = kargs['thresh']
    fourier_centered = self.__centered_fourier(img)
    log_magnitude = self.__get_log_magnitude(img)
    min = log_magnitude.min()
    fourier_centered[(log_magnitude >= min) & (log_magnitude <= min+thresh)] = 0
    return self.__inverse_fourier(fourier_centered)

  def img_without_max_spectrum(self, img, kargs={'thresh': 5}):
    thresh = kargs['thresh']
    fourier_centered = self.__centered_fourier(img)
    log_magnitude = self.__get_log_magnitude(img)
    max = log_magnitude.max()
    fourier_centered[(log_magnitude <= max) & (log_magnitude >= max-thresh)] = 0
    return self.__inverse_fourier(fourier_centered)

  def magnitude_spectrum_without_max(self, img, kargs={'thresh': 5}):
    thresh = kargs['thresh']
    log_magnitude = self.__get_log_magnitude(img)
    max = log_magnitude.max()
    log_magnitude[(log_magnitude <= max) & (log_magnitude >= max-thresh)] = 0
    return self.__normalize(log_magnitude)

  def magnitude_spectrum_without_min(self, img, kargs={'thresh': 5}):
    thresh = kargs['thresh']
    log_magnitude = self.__get_log_magnitude(img)
    min = log_magnitude.min()
    log_magnitude[(log_magnitude >= min) & (log_magnitude <= min+thresh)] = 0
    return self.__normalize(log_magnitude)

  def __centered_fourier(self, img):
    ft = np.fft.fft2(img)
    return np.fft.fftshift(ft)

  def __inverse_fourier(self, fourier_centered):
    fourier = np.fft.ifftshift(fourier_centered)
    inversed_fourier = np.fft.ifft2(fourier)
    result_img = np.abs(inversed_fourier)
    return result_img

  def __normalize(self, arr):
    return cv2.normalize(arr, 0, 1, cv2.NORM_MINMAX)

  def __get_log_magnitude(self, img):
    fourier_centered = self.__centered_fourier(img)
    magnitude = np.abs(fourier_centered)
    magnitude_without_zero = 1 + magnitude
    return np.log(magnitude_without_zero)
