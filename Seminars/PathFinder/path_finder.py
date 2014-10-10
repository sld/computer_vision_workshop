from headers import *

class PathFinder:
  def __init__(self, image_path):
    self.image = cv2.imread(image_path)

  def find_and_draw(self):
    binary_image = self.filtered_binary_image(self.image)
    contours, hierarchy = self.find_contours(binary_image)
    graph = self.build_connection_graph(contours, hierarchy)

    start_arrow_point = self.start_arrow_point(self.image)
    start_arrow_contour = self.find_contour_by_point(start_arrow_point, contours, hierarchy)
    path = self.build_path(graph, start_arrow_contour)
    self.visualize_path(path, contours)
    self.draw()

  def visualize_path(self, path, contours):
    for verticle in zip(path, range(1, len(path)+1)):
      contour_ind = verticle[0]
      show_ind = verticle[1]
      contour = contours[contour_ind]

      # Start arrow
      if show_ind == 1:
        cv2.ellipse(self.image, cv2.fitEllipse(contour), (0,255,200), 3)

      # Treasure
      if show_ind == len(path):
        cv2.ellipse(self.image, cv2.fitEllipse(contour), (11,11,200), 3)

      (x,y) = self.fit_ellipse(contour)

      # Path
      font = cv2.FONT_HERSHEY_SIMPLEX
      cv2.putText(self.image, str(show_ind), (int(x)+10,int(y)), font, 1, (11,184,134), 2)

  def build_path(self, graph, start_ind):
    cur_ind = graph[start_ind][0]
    path = [start_ind, cur_ind]
    while (cur_ind != []):
      cur_ind = graph[cur_ind]
      if cur_ind == []:
        break
      else:
        cur_ind = cur_ind[0]
      path.append(cur_ind)
    return path

  def draw(self):
    rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
    plt.imshow(rgb_image)
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

        # very_magic_const helps to continue using of simple if condition
        # in LinePoint#scale
        very_magic_const = 0.79
        is_up_direction = (x1+very_magic_const > x2)

        line_point = LinePoint((x2,y2), angle, is_up_direction)

        x1, y1 = int(x1), int(y1)

        intersection_ind = self.intersection(line_point, contours, hierarchy)
        intersections[ind] = intersection_ind
        if intersection_ind and (intersection_ind[0] == ind):
          raise Exception("The same verticle in line intersection!")
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
        # Scale line from (x2, y2) to (x2+length,y2+length) with angle
        # to find intersection between two contours
        for scale_val in range(0,20):
          length = 62 + scale_val
          scaled_point = self.scale_point(line_point, length)
          if self.is_in_approx_poly(current_contour, scaled_point):
            result.append(ind)
            break

    if len(result) > 1:
      raise Exception("More than one intersection in arrows")
    return result

  def find_contour_by_point(self, point, contours, hierarchy):
    for component in zip(contours, hierarchy, range(0, len(contours))):
      current_contour = component[0]
      current_hierarchy = component[1]
      ind = component[2]

      is_parent = current_hierarchy[3] < 0
      if is_parent and self.is_in_approx_poly(current_contour, point):
        return ind

  def is_in_approx_poly(self, contour, point):
    approx_contour = cv2.approxPolyDP(contour, 10, True)
    is_in_poly = cv2.pointPolygonTest(approx_contour, point, False)
    return (is_in_poly != -1)

  def scale_point(self, line_point, length):
    scaled = line_point.scale(length)
    return scaled.point


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

# PathFinder('./data/Klad01.jpg').find_and_draw()
