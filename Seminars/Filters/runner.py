from headers import *


class Runner:
  def run_lena1(self):
    viewer = ImageProcessingViewer('./data/Lena01.jpg', ImageFilter())
    viewer.apply("blur", {'size': (3,3)})
    plt.show()

  def run_lena2(self):
    viewer = ImageProcessingViewer('./data/Lena02.jpg', ImageFilter())
    viewer.apply("gaussian_blur", {'size': (5,5), 'sigmaX': 0})
    plt.show()

  def run_lena3(self):
    viewer = ImageProcessingViewer('./data/Lena03.jpg', ImageFilter())
    viewer.set_plot_options({"sharex": False, "sharey": True})
    viewer.apply("sharper", {'size': (3,3), 'alpha': 3, 'sigmaX': 0})
    plt.show()

  def run_lena4(self):
    viewer = ImageProcessingViewer('./data/Lena04.jpg', ImageFilter())
    viewer.set_plot_options({"sharex": True, "sharey": True})
    viewer.apply("median_blur", {'ksize': 7})
    plt.show()

  def run_lena5(self):
    viewer = ImageProcessingViewer('./data/Lena05.jpg', ImageFilter())
    viewer.apply("anti_glass", {})
    plt.show()

  def run_lena6(self):
    viewer = ImageProcessingViewer('./data/Lena06.GIF', ImageFilter())
    viewer.apply("gauss_and_median_blur", {
      'size': (3,3), 'sigmaX': 0, 'ksize': 5
    })
    plt.show()

  def run_lena7(self):
    viewer = ImageProcessingViewer('./data/Lena07.GIF', ImageFilter())
    viewer.apply("erode_and_median", {'kernel': np.ones((7,7), np.uint8),
    'iters': 3, 'ksize': 9})
    plt.show()

  def run_all(self):
    for i in range(1,8):
      getattr(Runner(), "run_lena" + str(i))()
