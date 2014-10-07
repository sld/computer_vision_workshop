from headers import *

class GrayImgProcessingViewer:
  def __init__(self, image_path, image_processor):
    self.img = self.__open_image(image_path)
    self.image_processor = image_processor
    self.image_path = image_path
    self.set_plot_options()

  def apply(self, function_name, kwargs):
    if kwargs:
      image = getattr(self.image_processor, function_name)(self.img, kwargs)
    else:
      image = getattr(self.image_processor, function_name)(self.img)

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
      return plt.imread(image_path, 0)
    else:
      return cv2.imread(image_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)

  def __plot(self, processed_img, plot_name=''):
    f, (plt1, plt2) = plt.subplots(1, 2, **self.get_plot_options())
    plt1.set_title(plot_name)
    plt1.imshow(self.img, cmap='gray')
    plt2.imshow(processed_img, cmap='gray')

