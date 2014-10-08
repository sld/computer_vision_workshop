from headers import *
import math

class PathFinder:
  def __init__(self, image_path):
    self.image = cv2.imread(image_path)

  def draw(self):
    binary_image = self.__filtered_binary_image()
    self.__connected_components_in_image(binary_image)
    self.__draw_plot()

  def __draw_plot(self):
    plt.imshow(self.image, cmap='gray')
    plt.show()

  def __filtered_binary_image(self):
    gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray_image, 250, 1, cv2.THRESH_BINARY)
    binary = ImageFilter().dilate(binary, {"kernel": np.ones((7,7), np.uint8), "iters": 1})
    return binary

  #TODO: Refactor this fat function
  def __connected_components_in_image(self, binary):
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hierarchy = hierarchy[0]

    print "contours count is " + str(len(contours))

    for component in zip(contours, hierarchy, range(0, len(contours))):
      current_contour = component[0]
      current_hierarchy = component[1]
      ind = component[2]

      is_child = current_hierarchy[2] < 0
      is_parent = current_hierarchy[3] < 0

      if is_child:
        ellipse = cv2.fitEllipse(current_contour)
        cv2.ellipse(self.image,ellipse,(33,11,33))
      elif is_parent:
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

        i_contours = self.__intersection(x2, y2, contours, hierarchy)
        print [ind, i_contours]

        x1, y1 = int(x1), int(y1)

        cv2.line(self.image,(x1,y1),(x2,y2),(33,111,11),3)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(self.image,str(ind),(x1,y1), font, 1,(233,10,44),2)
        ind += 1


  def __intersection(self, x_, y_, contours, hierarchy):
    result = []
    for component in zip(contours, hierarchy, range(0, len(contours))):
      current_contour = component[0]
      current_hierarchy = component[1]
      ind = component[2]

      is_parent = current_hierarchy[3] < 0
      if is_parent:
        cnt = current_contour
        current_contour = cv2.approxPolyDP(cnt,10,True)
        is_in_poly = cv2.pointPolygonTest(current_contour, (x_,y_), False)

        if is_in_poly != -1:
          result.append([ind, is_in_poly])
    return result

pf = PathFinder('./data/Klad00.jpg')
pf.draw()
