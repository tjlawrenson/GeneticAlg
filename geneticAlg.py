#Create generations of images, selecting children for each successive generation based on their similarity to a given image

from PIL import Image
import random

#compare two images, getting a sum of the differences in color
def get_difference(local_image1, local_image2):
    
    #get the size, assuming both images are the same size
    local_image1_width, local_image1_height = local_image1.size
    
    #create a local sum variable
    sum = 0

    #loop through all the pixels
    for x in range(local_image1_width):
        for y in range(local_image1_height):
            #get the color values for this pixel
            r1,g1,b1 = local_image1.getpixel((x,y))
            r2,g2,b2 = local_image2.getpixel((x,y))

            #get the absolute value of the differences, and add it to the sum
            sum = sum + abs(r1-r2)
            sum = sum + abs(g1-g2)
            sum = sum + abs(b1-b2)

            if y == 1:
                print(str(sum), flush=True)

#class for defining characteristics of organisms
class Characteristic:
    
    #initialize the instance of the characteristic
    #a triangle, with a randomly chosen position, size, and color
    def __init__(self, total_image_width, total_image_height):

        #select x,y coordinates for each of the three points of the triangle
        self.point_1_x = random.randint(0,total_image_width)
        self.point_1_y = random.randint(0,total_image_height)
        self.point_2_x = random.randint(0,total_image_width)
        self.point_2_y = random.randint(0,total_image_height)
        self.point_3_x = random.randint(0,total_image_width)
        self.point_3_y = random.randint(0,total_image_height)

        #select the color
        self.r = random.randint(0,255)
        self.g = random.randint(0,255)
        self.b = random.randint(0,255)

    def characteristic_mutation(self):
        #shall the red color change?
        if random.random() < .20:
            self.r = random.randint(0,255)

        #shall the green color change?
        if random.random() < .20:
            self.g = random.randint(0,255)

        #shall the blue color change?
        if random.random() < .20:
            self.b = random.randint(0,255)

        

class Organism:

    def __init__(self, organism_width, organism_height):
        #create a characteristic list for this organism
        self.characteristic_list = []

        #give the organism three initial characteristics
        for i in range(0,3):
            self.characteristic_list.append(Characteristic(organism_width, organism_height))


    #iterate through the characteristics, deciding whether to mutate
    def mutate(self):
        #the characteristic below needs to be a reference in a list of characteristics
        for item in self.characteristic_list:
            pass


image1 = Image.open("elmerFudd.jpg")
image2 = Image.open("elmerFuddExplode.jpg")

#get_difference(image1, image2)

print(str(random.random()))

