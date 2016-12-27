import sys

# argv = [fade.py, input.ppm, blur_factor]

def main(argv):
   check_args(argv)
   infile = get_in_file(argv)
   
   (pixel_grid, width, height) = process_infile(infile)
   infile.close()

   new_grid = get_new_grid(pixel_grid, argv)

   outfile = get_out_file()
   output_grid(new_grid, outfile)
   outfile.close()
   
   print "... DONE"
   sys.exit(0)

   
def check_args(argv):
   try:
      int(argv[2])
   except ValueError as e:
      print >> sys.stderr, e
      print >> sys.stderr, "usage: python blur.py <input.ppm> <int blur factor>"
      sys.exit(1)
   except IndexError as e:
      print >> sys.stderr, "Using default blur factor"
      
def get_in_file(argv):
   try:
      return open(argv[1], "rb")
   except IOError as e:
      print >> sys.stderr, e
      print >> sys.stderr, "usage: python blur.py <input.ppm> <int blur factor>"
      sys.exit(1)
   
   
def get_out_file():
   return open("blurred.ppm", "w")
   
   
def process_infile(infile):
   line1 = infile.readline()
   line2 = infile.readline()
   line3 = infile.readline()
   (width, height) = check_ppm_header(line1, line2, line3)
   
   
   whole_file = infile.read()
   pixel_list = get_pixel_list(whole_file)
   pixel_grid = get_pixel_grid(pixel_list, width, height)
   return (pixel_grid, width, height)
   
   
def check_ppm_header(l1, l2, l3):
   try:
      if "P3" not in l1:
         raise IOError(".ppm header l1 not formatted properly")
      l2list = l2.split()
      if len(l2list) != 2:
         raise IOError(".ppm header l2 not formatted properly")
      (width, height) = (int(l2list[0]), int(l2list[1]))
      if "255" not in l3:
         raise IOError(".ppm header l3 not formatted properly.")
      return (width, height)
   except Exception as e:
      print e
      exit(1)
      
      
def get_pixel_list(longstring):
   nums_spaces = del_non_nums(longstring)
   pixel_list = groups_of_3(nums_spaces.split())
   return pixel_list


def del_non_nums(string):
   result = ''
   for c in string:
      if c.isdigit():
         result = result + c
      else:
         result = result + ' '
   return result
   
   
def groups_of_3(numlist): # 01234567
   newlist = []
   for n in range(int((len(numlist) / 3)) + 1):
      if n * 3 + 1 <= len(numlist):
         newlist.append([int(numlist[n * 3]),
                         int(numlist[n * 3 + 1]),
                         int(numlist[n * 3 + 2])])
   
   return newlist   
   
   
def get_pixel_grid(pixel_list, width, height):
   result = []
   for y in range(height):
      result.append([])
      for x in range(width):
         result[y].append(pixel_list[(width * y) + x])
   return result

   
def get_new_grid(grid, argv):
   height = len(grid)
   width = len(grid[0])
   result = []
   
   for y in range(height):
      result.append([])
      for x in range(width):
         (r, g, b) = do_pixel_calc(grid, x, y, int(argv[2]))
         result[y].append([r, g, b])
   return result
         
         
def do_pixel_calc(grid, x, y, reach):
   width = len(grid[0])
   height = len(grid)
   
   min_x = max(x - reach, 0)
   max_x = min(x + reach, width - 1)
   min_y = max(y - reach, 0)
   max_y = min(y + reach, height - 1)
   
   rsum = 0
   gsum = 0
   bsum = 0
   total = 0
   for y in range(min_y, max_y + 1):
      for x in range(min_x, max_x + 1):
         pixel = grid[y][x]
         rsum += pixel[0]
         gsum += pixel[1]
         bsum += pixel[2]
         total += 1
   r = rsum / total
   g = gsum / total
   b = bsum / total
   return (r, g, b)
   
   
def output_grid(grid, outfile):
   print >> outfile, "P3"
   print >> outfile, len(grid[0]), len(grid)
   print >> outfile, "255"
   for row in grid:
      for pixel in row:
         for val in pixel:
            print >> outfile, val
   

   
if __name__ == "__main__":
   main(sys.argv)