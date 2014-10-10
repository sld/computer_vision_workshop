from headers import *
import math

class LinePoint:
  def __init__(self, point, angle, is_up_direction):
    self.point = point
    self.angle = angle
    self.is_up_direction = is_up_direction

  def scale(self, scale_val):
    (x, y) = self.point
    if self.is_up_direction:
      x = int(x - scale_val*math.cos(self.angle))
      y = int(y - scale_val*math.sin(self.angle))
    else:
      x = int(x + scale_val*math.cos(self.angle))
      y = int(y + scale_val*math.sin(self.angle))

    return LinePoint((x,y), self.angle, self.is_up_direction)


class PathFinder:
  def __init__(self, image_path):
    self.image = cv2.imread(image_path)

  def draw(self):
    binary_image = self.filtered_binary_image(self.image)
    self.start_arrow_point(self.image)

    contours, hierarchy = self.find_contours(binary_image)
    graph = self.build_connection_graph(contours, hierarchy)
    print graph
    # path_contours = self.build_path(start_point, graph)
    # self.visualize_path(path_contours)

    # self.__connected_components_in_image(binary_image)
    # self.__draw_plot()

  def __draw_plot(self):
    plt.imshow(self.image, cmap='gray')
    plt.show()

  def start_arrow_point(self, image):
    _,_,r = cv2.split(image)
    _, th251 = cv2.threshold(r, 251, 1, cv2.THRESH_BINARY)
    _, thn255 = cv2.threshold(r, 254, 1, cv2.THRESH_BINARY_INV)
    unfiltered = th251 & thn255
    binary = ImageFilter().erode(unfiltered, {"kernel": np.ones((7,7), np.uint8),
      "iters": 1})

    contours, _ = self.find_contours(binary)
    if len(contours) != 1:
      raise Exception("Start arrow should have only 1 contour")

    (x,y) = self.fit_ellipse(contours[0])
    return (int(x),int(y))

  def find_contours(self, binary):
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours, hierarchy[0]

  def fit_ellipse(self, contour):
     (x,y),(_,_),_ = cv2.fitEllipse(contour)
     return (x,y)

  def filtered_binary_image(self, image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, blobs = cv2.threshold(gray_image, 3, 1, cv2.THRESH_BINARY)
    _, start_circle = cv2.threshold(gray_image, 100, 1, cv2.THRESH_BINARY)
    _, arrows_with_circles = cv2.threshold(gray_image, 250, 1, cv2.THRESH_BINARY)
    binary = blobs & (cv2.bitwise_not(start_circle)) | arrows_with_circles

    binary = ImageFilter().dilate(binary, {"kernel": np.ones((7,7), np.uint8),
      "iters": 1})
    return binary

  def build_connection_graph(self, contours, hierarchy):
    intersections = {}
    for component in zip(contours, hierarchy, range(0, len(contours))):
      current_contour = component[0]
      current_hierarchy = component[1]
      ind = component[2]

      is_parent = current_hierarchy[3] < 0

      if is_parent:
        child_contour = contours[current_hierarchy[2]]
        (x1,y1) = self.fit_ellipse(current_contour)
        (x2,y2) = self.fit_ellipse(child_contour)
        angle = math.atan((y2-y1) / (x2-x1))

        is_up_direction = (x1+0.79 > x2)

        line_point = LinePoint((x2,y2), angle, is_up_direction)

        x1, y1 = int(x1), int(y1)

        intersection_ind = self.intersection(line_point, contours, hierarchy)
        intersections[ind] = intersection_ind
        ind += 1

    return intersections

  def intersection(self, line_point, contours, hierarchy):
    result = []
    for component in zip(contours, hierarchy, range(0, len(contours))):
      current_contour = component[0]
      current_hierarchy = component[1]
      ind = component[2]

      is_parent = current_hierarchy[3] < 0
      if is_parent:
        for scale_val in range(0,5):
          length = 65 + scale_val
          scaled_point = self.scale_point(line_point, length)
          if self.is_in_approx_poly(current_contour, scaled_point):
            result.append(ind)
            break

    if len(result) > 1:
      raise Exception("More than one intersection in arrows")
    return result


  def is_in_approx_poly(self, contour, point):
    approx_contour = cv2.approxPolyDP(contour, 15, True)
    is_in_poly = cv2.pointPolygonTest(approx_contour, point, False)
    return (is_in_poly != -1)

  def scale_point(self, line_point, length):
    scaled = line_point.scale(length)
    return scaled.point


  #TODO: Refactor this fat function
  def cconnected_components_in_image(self, binary):
    contours, hierarchy = self.find_contours(binary)

    graph = self.build_connection_graph(contours, hierarchy)
    path_contours = self.build_path(start_point, graph)
    self.visualize_path(path_contours)

    print "contours count is " + str(len(contours))

    intersections = {}
    for component in zip(contours, hierarchy, range(0, len(contours))):
      current_contour = component[0]
      current_hierarchy = component[1]
      ind = component[2]

      is_child = current_hierarchy[2] < 0
      is_parent = current_hierarchy[3] < 0

      if is_parent:
        x,y,w,h = cv2.boundingRect(current_contour)
        cv2.rectangle(self.image,(x,y),(x+w,y+h),(200,255,0),3)

        child_contour = contours[current_hierarchy[2]]
        (x1,y1),(_,_),_ = cv2.fitEllipse(current_contour)
        (x2,y2),(_,_),_ = cv2.fitEllipse(child_contour)
        angle = math.atan((y2-y1)/(x2-x1))

        #TODO: Remove this very magic constant
        # It needs to do correct direction for one arrow in Klad02.jpg
        scale = 70
        if x1+0.79 > x2:
          x2 = int(x2 - scale*math.cos(angle))
          y2 = int(y2 - scale*math.sin(angle))
        else:
          x2 = int(x2 + scale*math.cos(angle))
          y2 = int(y2 + scale*math.sin(angle))

        x1, y1 = int(x1), int(y1)

        cv2.line(self.image,(x1,y1),(x2,y2),(33,111,11),3)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(self.image,str(ind),(x1,y1), font, 1,(233,10,44),2)
        intersection_inds = self.__intersection(x2, y2, contours, hierarchy)
        intersections[ind] = set(intersection_inds)
        ind += 1
      elif is_child:
        ellipse = cv2.fitEllipse(current_contour)
        cv2.ellipse(self.image,ellipse,(33,11,33))

    # Need to find first verticle
    top = toposort_flatten(intersections, sort=True)
    top.reverse()
    print intersections
    print top

pf = PathFinder('./data/Klad00.jpg')
pf.draw()
