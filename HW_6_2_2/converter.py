import cv2
import numpy as np

class Im_converter:
  def statistical_correction(self, img):
    p1, p99 = np.percentile(img, (1, 99))
    res_img = np.clip((img - p1) / (p99 - p1) * 255, 0, 255).astype(np.uint8)
    return res_img

  def channelization_correction(self, img):
    b, g, r = cv2.split(img)
    for ch in (b, g, r):
      p1, p99 = np.percentile(ch, (1, 99))
      ch = np.clip((ch - p1) / (p99 - p1) * 255, 0, 255).astype(np.uint8)
    res_img = cv2.merge([b, g, r])
    return res_img

  def binary_to_binary(self, img, threshold=None):
    if threshold is not None:
      _, res_img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    else:
      res_img = img

    return res_img

  def color_to_grayscale(self, img, level=3):
    b, g, r = cv2.split(img)
    res_img = cv2.merge([(b+g+r)/level])
    res_img = res_img.astype(np.uint8)
    return res_img

  def grayscale_to_color(self, img, palette):
    if len(palette) != 256:
      raise ValueError("Палитра должна содержать 256 цветов")
    indexed_img = img.astype(np.uint8)
    res_img = palette[indexed_img]
    return res_img

  def grayscale_to_binary(self, img, threshold=127, method='simple'):
    if method == "simple":
      _, res_img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    elif method == "otsu":
      _, res_img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY \
        + cv2.THRESH_OTSU)
    else:
      raise ValueError("Некорректный метод бинаризации")

    return res_img

  def binary_to_grayscale(self, img):
    inverted_img = cv2.bitwise_not(img)
    dist_transform = cv2.distanceTransform(inverted_img, cv2.DIST_L2, 5)
    cv2.normalize(dist_transform, dist_transform, 0, 255, cv2.NORM_MINMAX)
    res_img = np.uint8(dist_transform)
    return res_img

  def color_to_binary(self, img, threshold=127, level=3, method="simple"):
    return self.grayscale_to_binary(self.color_to_grayscale(img, level), \
      threshold, method)

  def binary_to_color(self, img, pallete):
    return self.grayscale_to_color(self.binary_to_grayscale(img), pallete)

if __name__ == "__main__":
  converter = Im_converter()
  img = cv2.imread("test_im/color.jpg")
  img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  res_img = converter.grayscale_to_binary(img_grey)
  cv2.imwrite("test_im/conv_color.jpg", res_img)