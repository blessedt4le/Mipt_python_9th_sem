from exception import Empty_file_path
from image_container import Color_image, Monochrom_image, Black_white_image

if __name__ == "__main__":
  err_f = 0
  try:
    img_1 = Color_image("test_data/bw.avif")
  except Empty_file_path as err:
    print(err.get_err_mess())
    err_f = 1

  if err_f == 0:
    print(img_1.get_size())
    print(img_1.get_img())