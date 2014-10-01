from headers import *


class ImageFilter:
  def blur(self, img, kwargs={'size': (3,3)}):
    return cv2.blur(img, kwargs['size'])

  def gaussian_blur(self, img, kwargs={'size': (3,3), 'sigmaX': 0}):
    return cv2.GaussianBlur(img, kwargs['size'], kwargs['sigmaX'])

  def sharper(self, img, kwargs={'size': (3,3), 'alpha': 1, 'sigmaX': 0}):
    borders = img - self.gaussian_blur(img, kwargs)
    sharped = img + kwargs['alpha']*borders
    return sharped

  def median_blur(self, img, kwargs={'ksize': 3}):
    return cv2.medianBlur(img, kwargs['ksize'])

  def gauss_and_median_blur(self, img, kwargs={
    'size': (3,3), 'sigmaX': 0, 'ksize': 5
    }):
    g_blured = self.gaussian_blur(img, kwargs)
    m_blured = self.median_blur(g_blured, kwargs)
    return m_blured

  def dilate(self, img, kwargs={"kernel": np.ones((5,5), np.uint8), "iters": 1}):
    return cv2.dilate(img, kwargs["kernel"], kwargs["iters"])

  def erode(self, img, kwargs={'kernel': np.ones((5,5), np.uint8), 'iters': 1}):
    return cv2.erode(img, kwargs['kernel'], kwargs['iters'])

  def opening(self, img, kwargs={"kernel": np.ones((5,5), np.uint8)}):
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kwargs["kernel"])

  def closing(self, img, kwargs={"kernel": np.ones((5,5), np.uint8)}):
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kwargs["kernel"])

  def erode_and_median(self, img, kwargs={'kernel': np.ones((5,5), np.uint8),
    'iters': 2, 'ksize': 3}):
    eroded_img = self.erode(img, kwargs)
    return self.median_blur(eroded_img, kwargs)

  def anti_glass(self, img, kwargs={}):
    medianed = self.median_blur(img, {'ksize': 7})
    blured = self.gaussian_blur(medianed, {'size': (3,3), 'sigmaX': 0})
    borders = blured - medianed
    mask =  self.opening(borders, {"kernel": np.ones((2,2), np.uint8)})
    sharped = blured + 2*mask
    return self.median_blur(sharped, {'ksize': 3})
