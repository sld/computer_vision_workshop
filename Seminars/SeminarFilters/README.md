# Computer vision seminar #1
## Image filtering

### Tested on:
- Anaconda 2.0.1
  - Python 2.7.8
  - Ipython 2.2.0
  - [OpenCV 2.4.9](https://binstar.org/jjhelmus/opencv)

### Available filters:
- blur,
- gaussian_blur,
- sharper,
- median_blur,
- gauss_and_median_blur,
- erode,
- opening,
- erode_and_median,
- anti_glass.


### Usage examples:
ImageFilter:

    import matplotlib.pyplot as plt
    import cv2
    from image_filter import ImageFilter

    image_path = './data/Lena01.jpg'
    image = cv2.imread(image_path)

    imf = ImageFilter()
    blured = imf.blur(image, {'size': (3,3)})

Also you can use ImageFilteringViewer to view how filter working:

    from image_filtering_viewer import ImageFilteringViewer

    viewer = ImageFilteringViewer('./data/Lena01.jpg')
    viewer.apply_filter("blur", {'size': (3,3)})
    plt.show()

To run all examples:

    from runner import Runner
    Runner().run_all()
