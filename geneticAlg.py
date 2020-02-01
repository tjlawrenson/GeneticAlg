#Create generations of images, selecting children for each successive generation based on their similarity to a given image

from PIL import Image,ImageDraw
import random
import copy


#set the location and base file name of the images
out_image_file_path = 'C:\\GenAlgImageData\\2020_01_31_pointy_haired_boss\\boss'

#set the maximum initial characteristic size as a percentage of the original image width
characteristic_percent = 8


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

            #if y == 1:
            #    print(str(sum), flush=True)

    return sum

def drawTheOrganism(local_organism, local_width, local_height):

    #create an image variable with the given type, width, and height
    local_image = Image.new('RGB', (local_width, local_height), color = (255,255,255))

    #create a draw variable
    draw = ImageDraw.Draw(local_image)

    for item in range(len(local_organism.characteristic_list)):

        #if this characteristic is a triangle, draw it
        if local_organism.characteristic_list[item].shape == "triangle":
            draw.polygon([(local_organism.characteristic_list[item].point_1_x, \
            local_organism.characteristic_list[item].point_1_y), \
            (local_organism.characteristic_list[item].point_2_x, \
            local_organism.characteristic_list[item].point_2_y), \
            (local_organism.characteristic_list[item].point_3_x, \
            local_organism.characteristic_list[item].point_3_y)], \
            fill=(local_organism.characteristic_list[item].r, \
            local_organism.characteristic_list[item].g, \
            local_organism.characteristic_list[item].b), \
            outline=(local_organism.characteristic_list[item].r, \
            local_organism.characteristic_list[item].g, \
            local_organism.characteristic_list[item].b))


        #if this characteristic is an ellipse, draw it
        elif local_organism.characteristic_list[item].shape == "ellipse":
            draw.ellipse((local_organism.characteristic_list[item].point_1_x, \
            local_organism.characteristic_list[item].point_1_y, \
            local_organism.characteristic_list[item].point_2_x, \
            local_organism.characteristic_list[item].point_2_y), \
            fill=(local_organism.characteristic_list[item].r, \
            local_organism.characteristic_list[item].g, \
            local_organism.characteristic_list[item].b), \
            outline=(local_organism.characteristic_list[item].r, \
            local_organism.characteristic_list[item].g, \
            local_organism.characteristic_list[item].b))
 


    return local_image


#class for defining characteristics of organisms
class Characteristic:
    
    #initialize the instance of the characteristic
    #a triangle, with a randomly chosen position, size, and color
    def __init__(self, total_image_width, total_image_height):

        self.shape_list = ["triangle", "ellipse"]

        #randomly choose a shape
        self.shape = random.choice(self.shape_list)
        
        #select the color
        self.r = random.randint(0,255)
        self.g = random.randint(0,255)
        self.b = random.randint(0,255)

        if self.shape == "triangle":
            #select x,y coordinates for each of the three points of the triangle
            self.point_1_x = random.randint(0,total_image_width)
            self.point_1_y = random.randint(0,total_image_height)

            #ensure that this starts off as a small shape by keeping the other points close by
            self.point_2_x = random.randint((self.point_1_x - max_initial_characteristic_pixels), (self.point_1_x + max_initial_characteristic_pixels))
            while self.point_2_x not in range (total_image_width):
                #choose another random point until we are inside the organism/image
                self.point_2_x = random.randint((self.point_1_x - max_initial_characteristic_pixels), (self.point_1_x + max_initial_characteristic_pixels))
            
            self.point_2_y = random.randint((self.point_1_y - max_initial_characteristic_pixels), (self.point_1_y + max_initial_characteristic_pixels))
            while self.point_2_y not in range (total_image_height):
                self.point_2_y = random.randint((self.point_1_y - max_initial_characteristic_pixels), (self.point_1_y + max_initial_characteristic_pixels))

            self.point_3_x = random.randint((self.point_1_x - max_initial_characteristic_pixels), (self.point_1_x + max_initial_characteristic_pixels))
            while self.point_3_x not in range (total_image_width):
                self.point_3_x = random.randint((self.point_1_x - max_initial_characteristic_pixels), (self.point_1_x + max_initial_characteristic_pixels))

            self.point_3_y = random.randint((self.point_1_y - max_initial_characteristic_pixels), (self.point_1_y + max_initial_characteristic_pixels))
            while self.point_3_y not in range (total_image_height):
                self.point_3_y = random.randint((self.point_1_y - max_initial_characteristic_pixels), (self.point_1_y + max_initial_characteristic_pixels))

        if self.shape == "ellipse":
            #select x,y coordinates for the top-left and lower-right corners of the bounding box
            #the upper left of this shape should not be in the far lower right
            self.point_1_x = random.randint(0,(total_image_width - max_initial_characteristic_pixels))
            self.point_1_y = random.randint(0,(total_image_height - max_initial_characteristic_pixels))

            #ensure that the ellipse does not start off too large
            self.point_2_x = random.randint((self.point_1_x + 1), (self.point_1_x + max_initial_characteristic_pixels))
            self.point_2_y = random.randint((self.point_1_y + 1), (self.point_1_y + max_initial_characteristic_pixels))


    def characteristic_mutation(self, total_image_width, total_image_height):
        #shall the red color change?
        if random.random() < .30:
            self.r = random.randint(0,255)

        #shall the green color change?
        if random.random() < .30:
            self.g = random.randint(0,255)

        #shall the blue color change?
        if random.random() < .30:
            self.b = random.randint(0,255)

        if self.shape == "triangle":
            #shall point_1_x change?
            if random.random() < .20:
                self.point_1_x = random.randint((self.point_1_x - 10), (self.point_1_x + 10))
                #if this point is not within the organism/image, try again
                while self.point_1_x not in range (total_image_width):
                    self.point_1_x = random.randint((self.point_1_x - 10), (self.point_1_x + 10))

            #shall point_1_y change?
            if random.random() < .20:
                self.point_1_y = random.randint((self.point_1_y - 10), (self.point_1_y + 10))
                #if this point is not within the organism/image, try again
                while self.point_1_y not in range (total_image_height):
                    self.point_1_y = random.randint((self.point_1_y - 10), (self.point_1_y + 10))

            #shall point_2_x change?
            if random.random() < .20:
                self.point_2_x = random.randint((self.point_1_x - 10), (self.point_1_x + 10))
                #if this point is not within the organism/image, try again
                while self.point_2_x not in range (total_image_width):
                    self.point_2_x = random.randint((self.point_1_x - 10), (self.point_1_x + 10))

            #shall point_2_y change?
            if random.random() < .20:
                self.point_2_y = random.randint((self.point_1_y - 10), (self.point_1_y + 10))
                #if this point is not within the organism/image, try again
                while self.point_2_y not in range (total_image_height):
                    self.point_2_y = random.randint((self.point_1_y - 10), (self.point_1_y + 10))

            #shall point_3_x change?
            if random.random() < .20:
                self.point_3_x = random.randint((self.point_1_x - 10), (self.point_1_x + 10))
                #if this point is not within the organism/image, try again
                while self.point_3_x not in range (total_image_width):
                    self.point_3_x = random.randint((self.point_1_x - 10), (self.point_1_x + 10))

            #shall point_3_y change?
            if random.random() < .20:
                self.point_3_y = random.randint((self.point_1_y - 10), (self.point_1_y + 10))
                #if this point is not within the organism/image, try again
                while self.point_3_y not in range (total_image_height):
                    self.point_3_y = random.randint((self.point_1_y - 10), (self.point_1_y + 10))


        if self.shape == "ellipse":
            #for ellipses, if the organism called for a mutation, mutate the whole location and size
            self.point_1_x = random.randint((self.point_1_x - 10), (self.point_1_x + 10))
            #if this point is not within the organism/image, try again
            while self.point_1_x not in range ((total_image_width - 10)):
                self.point_1_x = random.randint((self.point_1_x - 10), (self.point_1_x + 10))

            self.point_1_y = random.randint((self.point_1_y - 10), (self.point_1_y + 10))
            #if this point is not within the organism/image, try again
            while self.point_1_y not in range ((total_image_height - 10)):
                self.point_1_y = random.randint((self.point_1_y - 10), (self.point_1_y + 10))

            #stay within 30 pixels of the upper left x bound
            self.point_2_x = random.randint((self.point_1_x + 1), (self.point_1_x + 30))
            #if this point is not within the organism/image, try again
            while self.point_2_x not in range (total_image_width):
                self.point_2_x = random.randint((self.point_1_x + 1), (self.point_1_x + 30))

            #stay within 30 pixels of the upper left y bound
            self.point_2_y = random.randint((self.point_1_y + 1), (self.point_1_y + 30))
            #if this point is not within the organism/image, try again
            while self.point_2_y not in range (total_image_height):
                self.point_2_y = random.randint((self.point_1_y + 1), (self.point_1_y + 30))


class Organism:

    def __init__(self, organism_width, organism_height):
        #create a characteristic list for this organism
        self.characteristic_list = []

        #the organism should know it's own dimensions
        self.width = organism_width
        self.height = organism_height

        #give the organism three initial characteristics
        for i in range(0,3):
            self.characteristic_list.append(Characteristic(self.width, self.height))


    #iterate through the characteristics, deciding whether to mutate
    def mutate(self):
        #iterate through the characteristics, potentially mutating them
        #mutate a smaller percentage of characteristics if the number of characteristics is high
        for index in range(len(self.characteristic_list)):
            if len(self.characteristic_list) > 100:
                if random.random() < .01:
                    self.characteristic_list[index].characteristic_mutation(self.width, self.height)
        else:
            if random.random() < .10:
                    self.characteristic_list[index].characteristic_mutation(self.width, self.height)


        #shall a characteristic be added?
        if random.random() < .75:
            self.characteristic_list.append(Characteristic(self.width, self.height))

        #shall a characteristic be removed?
        if random.random() < .25:
            self.characteristic_list.remove(random.choice(self.characteristic_list))


#assign target image variable
target_image = Image.open("c:/temp/target.jpg")

#get the dimensions of the target image
target_image_width, target_image_height = target_image.size

print("Image size is " + str(target_image_width) + " wide by ", str(target_image_height) + " high.")

#calculate the max initial characteristic size in pixels based on width
max_initial_characteristic_pixels = int(round(target_image_width/100 * characteristic_percent))

parent_organism = Organism(target_image_width, target_image_height)


#create an image in memory
parent_organism_image = drawTheOrganism(parent_organism, target_image_width, target_image_height)

#save the parent image to disk
parent_organism_image.save('C:\\temp\\_original_parent_organism.jpg')

#find the initial difference
current_parent_difference = get_difference(parent_organism_image,target_image)

#create an image number variable that will be used for file names 
#for the sanity of the app creating the video, this cannot equal the generation since we're not saving all generations
image_number = 0

#loop through the generations
for y in range(50000):

    #create three children
    child1_organism = copy.deepcopy(parent_organism)
    child2_organism = copy.deepcopy(parent_organism)
    child3_organism = copy.deepcopy(parent_organism)

    #mutate the children
    child1_organism.mutate()
    child2_organism.mutate()
    child3_organism.mutate()

    #create images (in memory) of the children
    child1_organism_image = drawTheOrganism(child1_organism, target_image_width, target_image_height)
    child2_organism_image = drawTheOrganism(child2_organism, target_image_width, target_image_height)
    child3_organism_image = drawTheOrganism(child3_organism, target_image_width, target_image_height)

    #find how similar these images are to the target image (lower number is better)
    list_of_sums = []
    list_of_sums.append(get_difference(target_image,child1_organism_image))
    list_of_sums.append(get_difference(target_image,child2_organism_image))
    list_of_sums.append(get_difference(target_image,child3_organism_image))


    #find the organism closest to the target
    #if the first child is most similar to the target
    if list_of_sums[0] <= list_of_sums[1] and list_of_sums[0] <= list_of_sums[2] and list_of_sums[0] <= current_parent_difference:
        #make this the parent of the next generation
        parent_organism = child1_organism #pointing the parent_organism variable to this object
        
        #re-assign the current sum of differences        
        new_parent_difference = list_of_sums[0]

    #if the second child is most similar to the target
    elif list_of_sums[1] <= list_of_sums[0] and list_of_sums[1] <= list_of_sums[2] and list_of_sums[1] <= current_parent_difference:
        #make this the parent of the next generation
        parent_organism = child2_organism #pointing the parent_organism variable to this object

        #re-assign the current sum of differences   
        new_parent_difference = list_of_sums[1]

    #if the third child is most similar to the target    
    elif list_of_sums[2] <= list_of_sums[0] and list_of_sums[2] <= list_of_sums[1] and list_of_sums[2] <= current_parent_difference:
        #make this the parent of the next generation
        parent_organism = child3_organism #pointing the parent_organism variable to this object
        
        #re-assign the current sum of differences   
        new_parent_difference = list_of_sums[2]

    else: #the parent survives to have another generation of children!
        new_parent_difference = current_parent_difference

    #if a child has become the parent of the next generation
    if new_parent_difference < current_parent_difference:

        #create an image in memory to save to disk
        parent_organism_image = drawTheOrganism(parent_organism, target_image_width, target_image_height)

        #save the image used for an ongoing visual
        parent_organism_image.save('C:\\temp\\current_parent_organism.jpg')

        #create a file path string and save the image to disk (for later video creation)
        file_path_string = out_image_file_path + str(image_number).zfill(5) + '.jpg'
        parent_organism_image.save(file_path_string)

        #increment the image number
        image_number += 1

        #reset the current_parent_difference
        current_parent_difference = new_parent_difference
        

    #report some stats occasionally
    if y % 5 == 0:
        #calculate highest possible color difference
        max_color_difference = (target_image_width * target_image_height) * (255 * 3)
        color_percentage_reached = 100 * (max_color_difference - current_parent_difference) / max_color_difference
        print("Gen: " + str(y) + \
            "  Characteristics: " + str(len(parent_organism.characteristic_list)) + \
            "  Color percentage reached: " + str(color_percentage_reached), flush=True)



