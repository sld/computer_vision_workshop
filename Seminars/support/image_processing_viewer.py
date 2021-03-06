from headers import *


class ImageProcessingViewer:
  def __init__(self, image_path, image_processor):
    self.bgr_img = self.__open_image(image_path)
    self.rgb_img = self.__rgb_img(self.bgr_img)
    self.image_processor = image_processor
    self.image_path = image_path
    self.set_plot_options()

  def apply(self, function_name, kwargs):
    if kwargs:
      image = getattr(self.image_processor, function_name)(self.bgr_img, kwargs)
    else:
      image = getattr(self.image_processor, function_name)(self.bgr_img)

    plot_title = function_name + ' ' + self.image_path + ' ' + str(kwargs)
    self.__plot(image, plot_title)

  def set_plot_options(self, options={}):
    if options:
      self.plot_options = options
    else:
      self.plot_options = {"sharey": True, "sharex": True}

  def get_plot_options(self):
    return self.plot_options

  def __open_image(self, image_path):
    if image_path.split(".")[-1].lower() == "gif":
      return plt.imread(image_path)
    else:
      return cv2.imread(image_path)

  def __plot(self, bgr_img, plot_name=''):
    f, (plt1, plt2) = plt.subplots(1, 2, **self.get_plot_options())
    plt1.set_title(plot_name)
    plt1.imshow(self.rgb_img)
    plt2.imshow(self.__rgb_img(bgr_img))

  def __rgb_img(self, bgr_img):
    return cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)

