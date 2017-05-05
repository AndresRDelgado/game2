'''Mama World version 1.0, by Andres Delgado, Jorge Delgado, Tania Delgado'''
import random
class You:
    def __init__(self, fname, age, mshoesize, favcolor, location):
        self.name = fname
        self.age = age
        self.shoesize = mshoesize
        self.color = favcolor
        self.whistle = random.random()*100
        self.location = location

    def __str__(self):
        return (self.name)
    
    def move(self, directstr, yourWorld):
        go = direction(directstr)
        here = self.location
        futureloc = ((int(here[0]) + int(go[0])) ,(int(here[1]) + int(go[1])),(int(here[2]) + int(go[2])))
        for room in yourWorld.roomlist:
            if room.location == futureloc:
                self.location = futureloc
                for item in yourWorld.itemlist:
                    if item.possessed == True:
                        item.location = futureloc
                action("look",yourWorld)
                yourWorld.checkendgame(room.location)
                return
        else:
            print("The way is blocked.")

    def get(self, yourWorld, grabthis):
        for item in yourWorld.itemlist:
            if item.name.lower() == grabthis.lower():
                if item.possessed == False and item.location == yourWorld.protag.location:
                    item.possessed = True
                    print("You collect a "+ item.name+".") #add a better description for the object (shorter) when you pick something up
                    return
                elif item.possessed == True:
                    print("You already have that.")
                    return
                elif item.location != yourWorld.protag.location:
                    print("You don't see that here.")
                    return
        print("Grabbing "+grabthis+" is not going to work.")

    def inventory(self, yourWorld):
        haveitems = ""
        itemct = 0
        for item in yourWorld.itemlist:
            if item.possessed == True:
                if itemct == 0:
                    haveitems += item.name
                else:
                    haveitems += ", and a " +item.name
                itemct += 1
        if itemct == 0:
            print("You don't have nothin'")
        else:
            print("You have a "+haveitems+".")
        return 


class NPC(You):
    def __init__(self, fname, age, mshoesize, favcolor, location, description, responses, activator):
        super().__init__(fname, age, mshoesize, favcolor, location)
        self.description = description
        self.responses = responses
        self.activator = activator
        self.activated = False

    def conversation(self, talkto, yourWorld):
        if self.location == yourWorld.protag.location:
            for dialogue in yourWorld.dialoguelist:
                if dialogue.name == self.name:
                    print(dialogue.opener)
                    input("Press enter to continue")
                    print(dialogue.attention)
                    input("Press enter to continue")
                    print(dialogue.prompt)
                    speech = input("Select a letter (A-C)")
                    print (self.name+": "+self.responses[speech[0].upper()])
                    if speech.lower() == self.activator.lower():
                        self.activated = True
                        self.location = yourWorld.finalroom
            return
        elif self.location != yourWorld.protag.location:
            print("That one is not within earshot.")
            return
    def examine(self, lookat, yourWorld):
        if self.location == yourWorld.protag.location:
            print(self.description)
        elif self.location != yourWorld.protag.location:
            print("That's not here.")

class Dialogue:
    def __init__(self, name, opener, attention, prompt):
        self.name = name
        self.opener = opener
        self.attention = attention
        self.prompt = prompt

class Room:
    def __init__(self, rname, rlocation, rdescription, ractivedesc):
        self.name = rname
        self.location = rlocation
        self.description = rdescription
        self.firstencounter = 0
        self.activedesc = ractivedesc
        self.activated = False

    def __str__(self):
        return (self.name)

class Item:
    def __init__(self, iname, ilocation, idescription, activedesc):
        self.name = iname
        self.location = ilocation
        self.description = idescription
        self.possessed = False
        self.activated = False
        self.activedesc = activedesc
    
    def examine(self,lookat, yourWorld):#try it without the lookat and yourWorld parameters
        if self.location == yourWorld.protag.location:
            if self.activated == False:
                print(self.description)
                return
            elif self.activated == True:
                print(self.activedesc)
        elif self.location != yourWorld.protag.location:
            print("That's not here.")
    
    def use(self, useit, yourWorld):
        if self.location == yourWorld.protag.location:
            if self.possessed == True:
                if self.activated == False:
                    print("You use the "+self.name+".")
                    self.activated = True
                    yourWorld.checkprogress(self.name)
                elif self.activated == True:
                    print("You've used it once already.")
            elif self.possessed == False:
                print("You'll need to pick that up first.")
        elif self.location != yourWorld.protag.location:
            print("That is not here.")

# class Weapon(Item):
#     def __init__(self, iname, ilocation, idescription):
#         super().__init__(iname, ilocation, idescription)
#         atkstr = 10

class World:
    def __init__(self, things):
        self.things =things
        self.dialoguelist = []
        self.roomlist = []
        self.itemlist = []
        self.npclist = []
        self.finalroom = (2,3,0)
        self.finalitem = "candle"
        self.finaltext = "You hear a faint rumbling."
        self.finalactivatedroom = (3,3,0)
        for i in things:
            if i[0] ==4:
                self.dialoguelist += [Dialogue(i[1],i[2],i[3],i[4])]
            if i[0] == 3:
                self.npclist += [NPC(i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8])]
            if i[0] == 2:
                self.itemlist += [Item(i[1],i[2],i[3],i[4])]
            if i[0] == 1:
                self.roomlist += [Room(i[1],i[2],i[3],i[4])]
            elif i[0] == 0:
                self.protag = You(i[1],i[2],i[3],i[4],i[5])
    def checkprogress(self, itemname):
        if self.finalitem == itemname:
            for room in self.roomlist:
                if room.location == self.finalactivatedroom:
                    if room.activated == False:
                        print(self.finaltext)
                        room.activated = True
    def checkendgame(self, roomchk):
        if roomchk == self.finalroom:
            print("***********************\n****Happy Birthday,****\n*********Mama!*********\n***********************\n\n You beat the game!")
            exit()


def direction(directstr):
    if directstr == "north":
        return (0,1,0)
    elif directstr == "east":
        return (1,0,0)
    elif directstr == "south":
        return (0,-1,0)
    elif directstr == "west":
        return (-1,0,0)

def action(next, yourWorld):
    #have another format available for user input
    nextlist = next.split()
    if len(nextlist) == 0:
        return
    if nextlist[0].lower() == "help":
        print("Welcome to Mama World! \nYou can LOOK, GET ITEMS and EXAMINE ITMES that your encounter, TALK TO people that you meet.  See what you're carrying by typing CHECK INVENTORY.  GO or WALK in different directions to see the world.\nTo see these instructions at any time, type HELP.")
        return
    
    #look in your bag
    if nextlist[0].lower() =="check":
        if len(nextlist) == 2:
            if nextlist[1].lower() == "inventory":
                yourWorld.protag.inventory(yourWorld)
                return

    #talk to an NPC
    if nextlist[0].lower() == "talk":
        if len(nextlist) == 1:
            print("Talk to whom?")
            return
####begin papa's free form convo model####THIS SECTION IS DEAD VIA THE RETURN IN THE ABOVE LINE UNTIL I FIGURE
#OUT HOW TO DIVORCE THE DIALOGUE FROM THE LOOK FUNCTION - BC IT IS "LOOKING" TWICE WHEN A PERSON TYPES LOOK
            # npcs = ""
            # npcsct = 0
            # for i in yourWorld.npclist:
            #     if i.location == yourWorld.protag.location:
                    
            #         for ii in yourWorld.npclist:
            #             if ii.location == yourWorld.protag.location:# and ii.visible is True: (would like to create a way to call Panther & make her visible)
            #                 if npcsct == 0:
            #                     npcs += " " + ii.name
            #                     npcsct += 1
            #                 else:
            #                     npcs += ", and "+ ii.name
            #         if i.location[0]==0 and i.location[1]==2 and i.location[2]==0: # in black room

            #             response=input("Hi, what's up?\n")
            #             endless_conversation=True
            #             while endless_conversation == True:
            #                 conv=response.split()
            #                 for keyword in conv :
            #                     if keyword.lower() == "doing" :
            #                         response=input("'Doing?' I'm just chilling.  How about that cake, ey?\n>")
            #                     elif keyword.lower() == "why" :
            #                         response=input("'Why?' Why not?.\n>")
            #                     elif keyword.lower() == "where" :
            #                         response=input("'Where?' I'm not sure.\n>")
            #                     else:
            #                         print("Hmmm. Follow your instincts.\n>")
            #                         endless_conversation=False

            #         if i.location[0]==0 and i.location[1]==1 and i.location[2]==0: # in red room

            #             response=input("Panther looks you right in the eye and opens his mouth...\n")
            #             endless_conversation=True
            #             while endless_conversation == True:
            #                 conv=response.split()
            #                 for keyword in conv :
            #                     if keyword.lower() == "doing" :
            #                         response=input("mew?\n>")
            #                     elif keyword.lower() == "why" :
            #                         response=input("meow?\n>")
            #                     elif keyword.lower() == "where" :
            #                         response=input("Meow, meow?'\n>")
            #                     else:
            #                         print("Purrrr.\n>")
            #                         endless_conversation=False
            # return
####end papa free form convo model####

        elif len(nextlist) == 2 and nextlist[1].lower() != "to":
            talkto = nextlist[1]
            for character in yourWorld.npclist:
                if character.name.lower() == talkto.lower():
                    character.conversation(talkto, yourWorld)
                    return
            else:
                print(talkto+" couldn't hear you if you did.")
                return
        elif len(nextlist) == 3 and nextlist[1].lower() == "to":
            talkto = nextlist[2]
            for character in yourWorld.npclist:
                if character.name.lower() == talkto.lower():
                    character.conversation(talkto, yourWorld)
                    return
            else: 
                print(talkto+" couldn't hear you if you did.")
                return
        else:
            print("Talk to whom?")


        return

    #examine an item
    if nextlist[0].lower() == "examine":
        if len(nextlist) == 1:
            print("Examine what?")
            return
        elif len(nextlist) == 2:
                lookat = nextlist[1]
                for character in yourWorld.npclist:
                    if character.name.lower() == lookat.lower():
                        character.examine(lookat, yourWorld)
                        return
                for item in yourWorld.itemlist:
                    if item.name.lower() == lookat.lower():
                        item.examine(lookat, yourWorld)
                        return
                else:
                    print("It doesn't look like anything to me.")
                    return

    #use an item
    if nextlist[0].lower() == "use":
        if len(nextlist) == 1:
            print("Use what?")
            return
        elif len(nextlist) == 2:
                useit = nextlist[1]
                for character in yourWorld.npclist:
                    if character.name.lower() == useit.lower():
                        print("That's not nice.")
                        return
                for item in yourWorld.itemlist:
                    if item.name.lower() == useit.lower():
                        item.use(useit, yourWorld)
                        return
                else:
                    print("It doesn't look like anything to me.")
                    return        


    #check your surroundings action
    if next.find("look") > -1: #might be good to incude a dictionary and run through the keys
        npcs = ""
        npcsct = 0
        for i in yourWorld.npclist:

            if i.location == yourWorld.protag.location:
                if npcsct == 0:
                    npcs += " " + i.name
                    npcsct += 1
                else:
                    npcs += ", and "+ i.name
        items = ""
        itemct = 0
        for i in yourWorld.roomlist:
            if i.location == yourWorld.protag.location:
                for ii in yourWorld.itemlist:
                    if ii.location == yourWorld.protag.location and ii.possessed is False:
                        if itemct == 0:
                            items += "a " + ii.name
                            itemct += 1
                        else:
                            items += ", and a "+ ii.name
                if itemct > 0 and npcsct > 0:
                    if i.activated == False:
                        print(i.description+" You see " +items+"."+npcs+" is here.")
                        return
                    elif i.activated == True:
                        print(i.activedesc+" You see " +items+"."+npcs+" is here.")
                        return
                elif itemct > 0:
                    if i.activated == False:
                        print(i.description+" You see " +items+".")
                        return
                    elif i.activated == True:
                        print(i.activedesc+" You see "+items+".")
                        return
                elif npcsct > 0:
                    if i.activated == False:
                        print(i.description+npcs+" is here.")
                        return
                    elif i.activated == True:
                        print(i.activedesc+npcs+" is here.")
                        return
                else:
                    if i.activated == False:
                        print(i.description)
                        return
                    elif i.activated == True:
                        print(i.activedesc)
                        return
        return

    #travel around the map action
    directionskey = {"n":"north", "north":"north", "s":"south", "south":"south", "w":"west", "west":"west", "e":"east", "east":"east"}
    if nextlist[0].lower() == "go" or nextlist[0].lower() == "walk":
        if len(nextlist)==1:
            print("Which way should I go?")
        elif len(nextlist)==2:
            yourWorld.protag.move(directionskey.get(nextlist[1].lower()),yourWorld)
        return
    if (directionskey.get(nextlist[0].lower()) != None) and len(nextlist) == 1:
        yourWorld.protag.move(directionskey[nextlist[0].lower()],yourWorld)
        return

    #retrieve object
    for i in range(len(nextlist)-1):
        if nextlist[i] == "get":
            yourWorld.protag.get(yourWorld, nextlist[i+1])
            return    

    #if they don't give you something you can do
    else: 
        print("It's a good idea to "+next.lower()+".")



def main():
    yourWorld = World ([
        
    [0,"Andres",33,9,"blue",(0,0,0)], #first paramater tells if it's You, room, item, NPC, or dialogue

    # [1,"blueroom", (0,0,0), "It's blue, and there's a path to the north.",""],
    # [1,"redroom", (0,1,0),"It's red in here, and there's a path to the south. A big stone partially blocks the way north.","It's red in here, with a path to the south and one to the north."],
    # [1,"lobby", (0,0,1), "The front room at NetEffects.  A red ribbon lines this room in celebration of Christmas.",""],
    # [1,"celebrationroom", (0,3,0), "You found us!  A room filled with familiar faces and delicious food, all in one place for you!",""],
    # [1,"blackroom", (0,2,0),"It's black in here, and there's a path to the south.",""],

    [1,"backyard", (0,0,0),"To the east there is view of the corner of a 2-story house. To the north stand several young trees in front of a white wall. Looking west, the way is blocked by profusion of trees and thorny bushes. To the north, you realize you are on a hill that slopes down in this direction. You can go north or south.","I"],
    [1,"southofhouse5", (1,0,0),"To the east a pair of evergreen bushes frame a footpath.  You are at the corner of the house.  Looking down to the north, you gaze at the garden adorning the base of the house. You catch a glimpse of a stone winged guardian. There is a fragrance of mint in the air.  To the south is a white fence. You can go east and west.","I"],
    [1,"southofhouse4", (2,0,0),"To the east a trellis arch adorns a flagstone path. Look north toward the house, your attention is captured by the fragrant flowers in the garden at the base of the walls. To the west two rounded evergreen shrubs frame a footpath. You can go east or west.","I"],
    [1,"southofhouse3", (3,0,0),"To one side of the path you see an inviting white wrought iron bench nestled between 2 towering trees.  The trees are ringed with flowers.  You are surrounded by greenery.  To the west a trellis shaped like and arch frames a path. You can go east or west.","I"],
    [1,"southofhouse2", (4,0,0),"You find yourself in a tranquil garden of fragrant flowers and luxuriantly green ground cover.  A flagstone path beckons. You can go east or west.","I"],
    [1,"southofhouse", (5,0,0),"You make your way toward the corner of the garage.  Here is another garden of fragrant flowers.  A double-gated wrought iron entryway beckons.  You can go east or west.","I"],
    [1,"sidegarden", (6,0,0),"In front of you is a lovingly tended garden of colorful, fragrant flowers that borders a driveway.  Overhead, the branches of a gum tree catch a soft breeze. You can go west or north.","I"],
    [1,"backyard2", (0,1,0),"West of you there is a thickly wooded area with a decided perfume of pinetree in the air. Looking east, you can see the back of the 2-story house with a beautiful bay window. south of you is a path sloping uphill.  To the north the path continues downhill. ","I"],
    [1,"backyard3", (0,2,0),"Thick woods are west of you. They provide homes to various birds and squirrels.  Looking closely you can see someone has stacked firewood in this secluded area.  Turning to look at the house you see a beautiful tall deck. south of you is a path sloping uphill.  To the north the path continues downhill. ","I"],
    [1,"backyard4", (0,3,0),"To the west the woods are breaking up into view of a gently sloping valley with an oak tree in the distance.  Looking east at the house, it now looks like a 3-story house! There is a walk-out under the giant deck. south of you is a path sloping uphill.  To the north the path continues downhill. ","I"],
    [1,"panthersgrave", (0,4,0),"To the west there is view of a gently sloping valley with an oak tree and a weeping willow in the distance.  Looking east at the house, you gaze up at the deck and can only imagine its view of this same valley.  Directly in front of you is a shallow pit ringed by bricks. south of you is a path sloping uphill.  To the north the path continues downhill. ","I"],
    [1,"steephill", (0,5,0),"To the west there is a steep hill. Even here there are flowers planted just out of the reach of the woods looming on the right.  South of you is a path sloping uphill.  To the north the path is blocked by a profusion of trees and flowers. Looking east at the corner of the house, you see a sturdy white trellis allowing passage through surrounding woods and flowers ","I"],
    [1,"northofhouse5", (1,5,0),"To the west there is a white trellis providing a pathway through the foliage.  To the north of you is a very steep hill sloping down.  To the south the white house is decorated by some short evergreens in a garden at its base. To the east the path continues.  You can go east or west.","I"],
    [1,"northofhouse4", (2,5,0),"To the west there is a path.  To the north of you is a parklike setting with a wrought iron bench reposing beneath a tree.  To the south the white house is decorated by some short evergreens in a garden at its base. To the east the path continues. You can go east or west.","I"],
    [1,"northofhouse3", (3,5,0),"To the west is a view of woods as they approach the house. To the south of you is a parklike setting, a meadow surrouded by trees.  To the south the white house is decorated by some short evergreens in a garden at its base. To the east the path continues. You can go east or west.","I"],
    [1,"northofhouse2", (4,5,0),"There is a path to the west where you can see a view of woods as they approach the house. To the south of you is a parklike setting, a meadow surrouded by trees.  To the south the white house is decorated by some short evergreens in a garden at its base. To the east the path continues uphill. You can go east or west.","I"],
    [1,"northofhouse",(5,5,0),"The way is open to the west and the east. A pine tree appears to the east.",""],
    [1,"pinetree",(6,5,0),"There is a huge pine tree here.  I bet it was just a small sapling at one point.  You can proceed west or south.",""],
    [1,"frontyard", (6,1,0),"You pass in front of a white-doored garage framed with brick..  Over the door you notice even the vent has been tastefully painted and trimmed with a rich brown.","I"],
    [1,"frontyard2", (6,2,0),"You're standing in front of a 2 -story house.  It's white with brown accents.  The front porch is beautifully tiled.","I"],
    [1,"frontyard3",(6,3,0),"You're looking at a very nice house, indeed.  Large fluffy flowers surround you, and your path leads to the north or the south.",""],
    [1,"frontyard4",(6,4,0),"You're in the corner of the front yard of a pretty house.  If you go further north, you will reach a pine tree and to the south is more front yard.",""],
    [1,"livingroom",(3,2,0),"Now this is living.  A nice fireplace and soft carpeting mark this room, which you can leave to the north and east.",""],
    [1, "gameroom",(4,2,0),"A dark room that seems designed for playing video games.  A piano is in here, and you can exit to the north, east, or west.", ""],
    [1, "fronthall",(5,2,0),"This is the entryway of a very welcoming house.  It is still under construction, but the new flooring leads west, further into the house.",""],
    [1,"PARTYROOM",(2,3,0),"This is what it's all about!  Everyone is here to wish you a happy birthday!  Love you! (The kitchen lies back to the east.)",""],
    [1,"kitchen",(3,3,0),"Smells wonderful in here.  There's lots of light and granite. You can leave to the south and the east.","Smells wonderful in here.  There's lots of light and granite, and you can leave to the north, east ... and now to the west???"],
    [1,"bathroom",(4,3,0),"The most coveted spot in the house: the bathroom.  You can leave to the west or the south.",""],


    [2,"lamp", (0,1,0), "It's a tired old lamp.","The lamp shines brilliantly."],
    [2,"candle", (0,0,0), "It's a handsome red candle.", "The candle is festively lit."],
    [2,"Cake", (0,2,0), "It says Happy Birthday Mama!.", "The cake is a delicious memory."],

    [3,"Panther",12,.5,"black",(0,4,0),"A mingui-looking black cat.", {"A":"meow","B":"meow meow","C":"purr!\nPanther scampers off, stumbling a little as she goes.  Drooling."},"C"],
    [3,"Papa",60, 8.5,"black",(5,2,0),"A mingui-looking vato.", {"A":"Orale! \nAnd Papa books it out.","B":"what the heck","C":"Ask Andres - he knows!"},"A"],
    [3,"Snake",20,0,"green",(0,0,0),"The ancient ball python.", {"A":"sss","B":"sss \n(slithers away)","C":"sss"},"B"],
    [3,"Gerardo",20,0,"green",(4,2,0),"He's about 28 and looks very agreeable.", {"A":"No.","B":"I guess so.","C":"For suah.\nGerardo ducks out."},"C"],
    [3,"Tania",20,0,"green",(4,3,0),"Tania commands the room.", {"A":"Nyeah.","B":"Sort of.","C":"Maybe.\nSuddenly you realize you haven't seen Tania for a while."},"C"],
    [3,"Andres",20,0,"green",(4,2,0),"He looks like he's up to something.", {"A":"Duh.","B":"(audible sigh)\nAndres fades into the background.","C":"Yes, Mama.  You need to GET the CANDLE. Then USE it.  Then find your party room."},"B"],
    [3,"Ernie",20,0,"green",(3,2,0),"Ernie adorns this room perfectly.", {"A":"God do'd it!","B":"Where's the cake? \nErnie throws a smoke bomb and vanishes.","C":"I think so."},"B"],
    [3,"Mom",20,0,"green",(3,2,0),"Mom is dressed to celebrate.", {"A":"Claro que si.","B":"Claro que no. \nMom mira por todas partes y quietly tiptoes away.","C":"Me da narnias."},"B"],
    [3,"Gabe",20,0,"green",(3,3,0),"Gabe looks worried.", {"A":"Look man...","B":"The weather looks bad. \nGabe looks both ways and darts away.","C":"Of course!"},"B"],
    [3,"Andrea",20,0,"green",(3,3,0),"Andrea is a trooper.", {"A":"Sure, Coc'!","B":"Yes!  \nAndrea quickly ducks out.","C":"OK."},"B"],



    [4,"Papa", "You say: \nPapito?", "Papa looks at you quizzically.", "What do you say to him? \nA. Did you know it's my birthday? \nB. I want to paint the house dark brown, white and red. \nC. Papito, how do I solve the game?"],
    [4, "Panther", "You say: \nYo, Panther", "Panther vaguely turns in your direction.", "You continue: \nA. Did you build a toilet yet? \nB. You were really dead, right? \nC. It's a special day today."],
    [4, "Snake", "Hi, snake.","The snake stirs.","What do you say to a snake? \nA. Got enough water? \nB. Are you hungry? \nC. Does your cage need cleaning?"],
    [4, "Gerardo", "Mijo, Gerardo!","Gerardo looks up.","What do you say? \nA. Did you get your oil changed? \nB. Are you hungry? \nC. Will you be here for Christmas?"],
    [4, "Tania", "Mija!","What?","What do you say to your daughta? \nA. Are you hungry, mija? \nB. Are you sleepy? \nC. Want to go to the movies?"],
    [4, "Andres", "Jorge-Andres!","Si, Mama?","What do you say? \nA. It's kind of cold. \nB. Are you busy, mijo? \nC. Mijo, do you know how to solve the game?"],
    [4, "Ernie", "Ern!","Heyy!","What do you say? \nA. Oh no, this game is so long! \nB. Are you hungry? \nC. Are you having a good time?"],
    [4, "Mom", "Hola Mom!","Hola, mija!","What do you say? \nA. Le gusta kequi? \nB. Sabes donde esta el kequi? \nC. Haz visto la vibora?"],
    [4, "Gabe", "Hey man!","Coco!","What do you say? \nA. How long are you staying? \nB. What's on your mind? \nC. Did you know it's my birthday?"],
    [4, "Andrea", "Andrea!","Coc'!","What do you say? \nA. Are you doing good? \nB. Want to play monopoly? \nC. Let's hang out?"],

    ])
    print("Welcome to Mama World! version 1.0 \n(C) Delgado Productions 12/18/2016 \nYou can LOOK, GET ITEMS and EXAMINE ITMES that your encounter, TALK TO people that you meet.  See what you're carrying by typing CHECK INVENTORY.  GO or WALK in different directions to see the world.\nTo see these instructions at any time, type HELP.")
    gameend=False
    moves = 0
    while(gameend == False):
        next = input("What would you like to do?")
        action(next.lower(),yourWorld)
    # if moves > 6:
    #     gameend = True
    #     print("Oops, you're out of moves")
    # moves += 1
    exit()

main()
