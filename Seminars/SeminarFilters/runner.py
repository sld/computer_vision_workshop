from headers import *


class Runner:
  def run_lena1(self):
    viewer = ImageFilteringViewer('./data/Lena01.jpg')
    viewer.apply_filter("blur", {'size': (3,3)})
    plt.show()

  def run_lena2(self):
    viewer = ImageFilteringViewer('./data/Lena02.jpg')
    viewer.apply_filter("gaussian_blur", {'size': (5,5), 'sigmaX': 0})
    plt.show()

  def run_lena3(self):
    viewer = ImageFilteringViewer('./data/Lena03.jpg')
    viewer.set_plot_options({"sharex": False, "sharey": True})
    viewer.apply_filter("sharper", {'size': (3,3), 'alpha': 3, 'sigmaX': 0})
    plt.show()

  def run_lena4(self):
    viewer = ImageFilteringViewer('./data/Lena04.jpg')
    viewer.set_plot_options({"sharex": True, "sharey": True})
    viewer.apply_filter("median_blur", {'ksize': 7})
    plt.show()

  def run_lena5(self):
    viewer = ImageFilteringViewer('./data/Lena05.jpg')
    viewer.apply_filter("anti_glass", {})
    plt.show()

  def run_lena6(self):
    viewer = ImageFilteringViewer('./data/Lena06.GIF')
    viewer.apply_filter("gauss_and_median_blur", {
      'size': (3,3), 'sigmaX': 0, 'ksize': 5
    })
    plt.show()

  def run_lena7(self):
    viewer = ImageFilteringViewer('./data/Lena07.GIF')
    viewer.apply_filter("erode_and_median", {'kernel': np.ones((7,7), np.uint8),
    'iters': 3, 'ksize': 9})
    plt.show()

  def run_all(self):
    for i in range(1,8):
      getattr(Runner(), "run_lena" + str(i))()
