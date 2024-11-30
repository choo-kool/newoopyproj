# CMPU 2016 Object-Oriented Programming - Semester 1 Assignment
# TU857-2
# Group: Josh's Group
#
# Members:
#   1. Joshua Stanley (C23443452).
#   2. Andrew Ugweches (C23767071).
#   3. Donal Harcourt (C23375883).
#   4. Christian Bagrin (C23485084).
#   5. Max Doyle (C23399053).
#  Date: November 29, 2024
#
#
#
#


from abc import ABC, abstractmethod

# Create a Loggable mixin class for logging functionality
class Loggable:
    """In this solution, the Loggable class is incorporated as an independent
    class used for handling logging functionality, and the Game class is
    enhanced to use it via composition. """
    def __init__(self):
        self.__logs = []

    @property
    def logs(self):
        return self.__logs

    def log(self, message):
        if isinstance(message, str):
            self.__logs.append(message)

    def write_to_file(self, filename):
        try:
            f = open(filename, "w")
            try:
                for log_entry in self.__logs:
                    f.write(log_entry+ "\n")
            except PermissionError:
                print("Something went wrong writing to the file")
            finally:
                f.close()
        except:
            print("Something went wrong creating the file")



class CrimeScene:
    # This class has not changed in this lab.
    def __init__(self, location, stuff, objects, checked, notable, characters=None, npcs=None):
        self.location = location
        self.__clues = []
        self.__stuff = stuff if stuff else None
        self.__objects = objects
        self.__checked = checked
        self.__notable = notable
        self.__investigated = False
        self.__spoken = False
        self.__characters = characters if characters else []
        self.__npcs = npcs if npcs else []

    @property
    def investigated(self):
        return self.__investigated

    @investigated.setter
    def investigated(self, value):
        self.__investigated = value

    def add_clue(self, clue):
        self.__clues.append(clue)

    @property
    def stuff(self):
        return self.__stuff

    @property
    def spoken(self):
        return self.__spoken

    @spoken.setter
    def spoken(self, value):
        self.__spoken = value

    @property
    def objects(self):
        return self.__objects

    @property
    def notable(self):
        return self.__notable

    @property
    def checked(self):
        return self.__checked

    @checked.setter
    def checked(self, i):
        self.__checked[i] = True

    @property
    def characters(self):
        return self.__characters

    @property
    def npcs(self):
        return self.__npcs

    @npcs.setter
    def npcs(self, npcs):
        self.__npcs.append(npcs)

    def review_clues(self):
        """At the moment there are no checks on who can see the clues. We
        might need some further protection here."""
        return self.__clues

    def add_char(self, character):
        if character:
            self.__characters.append(character)

    def remove_char(self, character):
        if character:
            self.__characters.remove(character)



class TrapRoom(CrimeScene):
    def __init__(self, location, stuff, objects, checked, notable, code):
        super().__init__(location, stuff, objects, checked, notable)
        self.__trapped = True
        self.__code = code

    @property
    def trapped(self):
        return self.__trapped

    @trapped.setter
    def trapped(self, value):
        self.__trapped = False

    @property
    def code(self):
        return self.__code




#class for user to write down notes in order to solve the puzzle
class Notepad:

    def __init__(self):
        self._page = []

    @property
    def page(self):
        return self._page


    @page.setter
    def page(self, page):
        self._page = page



# this class has not changed
class Character(ABC):
    def __init__(self, name, dialogue):
        self._name = name
        self._dialogue = dialogue
        self._interacted = False

    def __str__(self):
        return f"{self.__class__.__name__}: {self._name}"

    def __eq__(self, other):
        if isinstance(other, Character):
            return self._name == other._name
        return False

    def __lt__(self, other):
        if isinstance(other, Character):
            return self._name < other._name
        return False

    @abstractmethod  # Declares an abstract method using a decorator.
    def perform_action(self):
        pass  # Abstract methods never contain any actual logic. The
        # transfer statement "pass" allows for this.

    # An abstract class must contain at least one abstract method.
    # However, "normal" methods may also be contained.
    def interact(self):
        if not self._interacted:
            interaction = f"{self._name}: {self._dialogue}"
            self._interacted = True
        else:
            interaction = f"{self._name} is no longer interested in talking."

        return interaction

    # def has_interacted(self):
    #     return self._interacted


# This class has not changed in this lab
class Suspect(Character):
    def __init__(self, name, dialogue, alibi):
        super().__init__(name, dialogue)
        self._alibi = alibi

    def __repr__(self):
        return f"Suspect('{self._name}', '{self._dialogue}', '{self._alibi}')"

    def provide_alibi(self):
        return f"{self._name}'s Alibi: {self._alibi}"

    def perform_action(self):  # Implement the abstract method for Suspect
        return (f"Suspect {self._name} nervously shifts and avoids eye "
               f"contact.")


# This class has not changed in this lab
class Witness(Character):
    def __init__(self, name, dialogue, observation):
        super().__init__(name, dialogue)
        self._observation = observation

    def __add__(self, other):
        if isinstance(other, Witness):
            combined_observation = f"{self._observation} and {other._observation}"
            combined_name = f"{self._name} and {other._name}"
            return Witness(combined_name, "Combined observations",
                           combined_observation)

    def share_observation(self):
        return (f"{self._name}'s Observation: {self._observation}")

    def perform_action(self):  # Implement the abstract method for Witness
        return (f"Witness {self._name} speaks hurriedly and glances around "
              f"anxiously.")

class NPC(Character):
    """
    A class that implements the abstract class Character.
    The perform_action method must provide logic.
    The purpose of this class is to provide characters that are not
    essential for the mystery.
    """

    def perform_action(self):
        return f"{self._name} decides to hang around and see what will happen."

    def interact(self):
        parent_int = super().interact()
        return f"{parent_int}"

# Enhanced Game class using composition
class Game:
    def __init__(self):
        # The Logger can be used throughout the game to capture important
        # events, interactions between characters, and observations. The key
        # takeaway is that the Logger class facilitates logging without
        # tightly coupling the game logic with the logging functionality.
        # This promotes modularity and helps in managing dependencies
        # effectively.
        self.__logger = Loggable()

        # ... from before:
        self.__running = True
        self.__game_started = False

        self.__npcs_interacted = False # no double interactions




        self.__mansion_drawing_room = CrimeScene("Mansion's Drawing Room", "Torn piece of fabric",
                                                 ["cabinet", "drawer", "mouse"],
                                                 [False, False, False],
                                                 ["Letters from James", "an old receipt", "nothing"])
        self.__upstairs_lobby = CrimeScene("Upstairs Lobby", "Cigarette box",
                                           ["The carpet", "The balcony", "The ladder"],
                                           [False, False, False],
                                           ["muddy footprints", "nothing", "nothing"])

        self.__kitchen = TrapRoom("Kitchen","Scrap paper",
                                   ["Fridge", "Spice cabinet", "Kitchen sink"],
                                   [False, False, False],
                                   ["A lone bottle of beer called 'letmeout'",
                                    "The number 3, etched into the wood",
                                    "A crudely drawn arrow pointing left"],
                                  "ibqjblrq") # this is a caesar cipher you can figure out from the provided clues

        self.__study = CrimeScene("Old Study", "",
                                  ["Bookcase", "Old diary", "Minibar"],
                                  [False, False, False],
                                  ["nothing", "Words of adoration for his troublesome son, what a doting father",
                                   "A bottle of 'letmein', where have I seen this before?"],)
        self.__garden = CrimeScene("Garden", "Broken twig",
                                   ["Window", "Check soil", "Shed"],
                                   [False, False, False],
                                   ["the light on and you can see bookcases through the glass",
                                    "dirt...", "Tools with some serious signs of wear"])
        self.__saferoom = CrimeScene("Trophy room", "The empty safe where the necklace was",
                                     ["Ledger", "Mountains of papers", "Window"],
                                     [False, False, False],
                                     ["Signs of failing investments under James", "nothing", "scratch marks"],)
        self.__library = CrimeScene("Library", "lot of shelves, they can't really be reading all of these",
                                    ["West bookshelf", "Centre bookshelf", "East bookshelf"],
                                    [False, False, False],
                                    ["nothing",
                                     "A hidden passage where could it lead!", "nothing"])

        self.__testingRoom = CrimeScene("Backrooms", "nothing",
                                        [], [], [])


        #sus juan in garden
        #w Sir.James, i don't trust him
        #sus griselda in upstairs
        #w dorothy upstairs, gris nicer than she looks

        self.__current_scene = self.__mansion_drawing_room
        #self.__present_suspect = Suspect
        self.__juan = Suspect("Juan Rodriguez", "Really man... I'm just the gardener! Where else would "
                                                "I be all night ",
                              "Unconfirmed")
        self.__griselda = Suspect("Head maid Griselda", "I'm afraid no one has gone in the study since he passed"
                                                        "\nMe? A suspect? If you must know I was here in this very lobby "
                                                        "all evening, what with the mess on the carpet. "
                                                        "\nThe room where the necklace was is over there "
                                                        "Now leave me be!",
                                  "Confirmed by Dorothy")

        self.__james = Witness("Sir James", "I don't know about that Gardener fellow,"
                                            " something about him is untrustworthy\n"
                                            "Look at the state of him!", "Mud all over gardener's clothes")
        self.__dorothy = Witness("Junior maid Dorothy", "Griselda is nicer than she seems, I say some of the "
                                                        "family here don't deserve her with their attitude!",
                                 "Haughty family members")
        self.__smith = Suspect("Mr. Smith", "I was in the library all "
                                            "evening."
                                            "\n I say it was that damn maid, for years she was only loyal to Father"
                                            , "Confirmed by the butler.")
        self.__parker = Witness("Ms. Parker", "I saw someone near the window "
                                             "at the time of the incident.",
                               "Suspicious figure in dark clothing.")

        indifferent_npc = NPC("Generic Maid #5", "How do you do.")
        friendly_npc = NPC("Butler", "Welcome to the Smith Estate")
        hostile_npc = NPC("Cat", "MREOWWW")
        dr_npcs = [indifferent_npc, friendly_npc, hostile_npc]
        for i, npc in enumerate(dr_npcs, start = 0):
            self.__current_scene.npcs = dr_npcs[i]
        guest_npc1 = NPC("Tea party guest", "That Smith boy must clean up his act")
        guest_npc2 = NPC("Tea party woman", "Oh certainly, I hear he's in the bookies til dark!")
        garden_npcs = [guest_npc1, guest_npc2]
        for i, npc in enumerate(garden_npcs, start = 0):
            self.__garden.npcs = garden_npcs[i]
        maid_npc = NPC("Maid #17", "Psst. Wanna know why the Head Maid has such long nails")
        maid_npc2 = NPC("Maid #38", "Quiet she'll hear you!")
        lobby_npcs = [maid_npc, maid_npc2]
        for i, npc in enumerate(lobby_npcs, start = 0):
            self.__upstairs_lobby.npcs = lobby_npcs[i]




        self.__present_witness = self.__parker
        self.__present_suspect = self.__smith

        self.__mansion_drawing_room.add_char(self.__parker)
        self.__mansion_drawing_room.add_char(self.__smith)

        self.__upstairs_lobby.add_char(self.__griselda)
        self.__upstairs_lobby.add_char(self.__dorothy)

        self.__garden.add_char(self.__juan)
        self.__garden.add_char(self.__james)

        #add the rest too
        self.__testingRoom.add_char(self.__smith)
        self.__testingRoom.add_char(self.__parker)
        self.__testingRoom.add_char(self.__griselda)
        self.__testingRoom.add_char(self.__dorothy)
        self.__testingRoom.add_char(self.__juan)
        self.__testingRoom.add_char(self.__james)

        self.__clues = []
        self.__notes = Notepad()


    @property
    def log(self):
        # to do: think of some appropriate access checks here. For example,
        # only admins are allowed to read out logs.
        return self.__logger

    def run(self):
        # ...
        self.__logger.log("Game started")
        # ...
        print("Welcome to 'The Poirot Mystery'")
        print("You are about to embark on a thrilling adventure as a detective.")
        print("Your expertise is needed to solve a complex case and unveil the truth.")


        while self.__running:
            self.update()

    def update(self):
        # ...
        self.__logger.log("I'm updating")
        # ...

        if not self.__game_started:
            player_input = input("Press 'q' to quit or 's' to start: ")
            if player_input.lower() == "q":
                self.__running = False
            elif player_input.lower() == "s":
                self.__game_started = True
                self.start_game()

            self.__logger.log(f"Player input: {player_input}")

        else:
            player_input = input(
                "ACTIONS:\n'q' to quit or 'f' to finish and declare the culprit!"
                "\n'c' to continue, 's' to speak, "
                "\n'e' to examine clues, 'r' to review room clues, 'l' to look around, "
                "\nor 'n' to open your notepad"
                f"\nCurrent Location: {self.__current_scene.location}"
                "\n: ")

            if player_input.lower() == "q":
                self.__running = False
            elif player_input.lower() == "f":
                self.accuse_suspect()
            elif player_input.lower() == "c":
                self.continue_game()
            elif player_input.lower() == "s":
                self.interact_with_characters()
            elif player_input.lower() == "e":
                self.examine_clues()
            elif player_input.lower() == "l":
                self.look_around()
            elif player_input.lower() == "r":
                clues = self.__current_scene.review_clues()
                #clues = self.__crime_scene.review_clues()
                if clues:
                    print(clues)
                else:
                    print("You have not found any clues here yet.")
            elif player_input.lower() == "n":
                try:
                    note_choice = int(input("Review your notes or write a new note"
                                            "\n1. Review notes"
                                            "\n2. Write a new note\n: "))
                    if note_choice == 1:
                        if len(self.__notes.page) < 1:
                            print("You haven't written anything yet"
                                  "\nMake sure you take down anything important")
                        else:
                            print("Your Notebook")
                            i = 0
                            while note_choice:
                                if i >= len(self.__notes.page):
                                    print("You haven't written anything else down")
                                    i = len(self.__notes.page)
                                elif i < 0:
                                    print("Your hands fumble, almost dropping your trusted notebook")
                                    i=0
                                else:
                                    self.check_notes(i)
                                page_choice = input("Press n for next page, p for previous, a to display all notes "
                                                    "or press c to close your notebook and continue: ")
                                if page_choice.lower() == "p":
                                    i -= 1
                                elif page_choice.lower() == "n":
                                    i += 1
                                elif page_choice.lower() == "a":
                                    self.check_notes(page_choice)
                                    break
                                elif page_choice.lower() == "c":
                                    print("You close your notebook, eager to continue the case")
                                    break
                                else:
                                    print("You clumsily drop your notebook")
                                    break

                    elif note_choice == 2:
                        done = False
                        while not done:
                            user_note = input("Write notes here "
                                              "\nor type !q to close your notebook\n: ")
                            if user_note == "!q":
                                done = True
                            else:
                                self.__notes.page.append(user_note)
                    else:
                        raise ValueError
                except ValueError:
                    print("You think to yourself for a moment, wondering how you've come this far "
                          "before eventually closing your notepad")



            self.__logger.log(f"Player input: {player_input}")

    def check_notes(self, page):
        if type(page) == int:
            print(f"Note {page + 1}:")
            print(f"'{self.__notes.page[page]}'")
        else:
            for i, page in enumerate(self.__notes.page, start=0):
                print(f"Note {i + 1}:")
                print(f"'{self.__notes.page[i]}'")



    def start_game(self):
        # ...
        self.__logger.log("Game is starting")
        # ...

        # from before...
        player_name = input("Enter your detective's name: ")
        print(f"Welcome, Detective {player_name}!")
        print("You find yourself in the opulent drawing room of a grand mansion.")
        print("As the famous detective, you're here to solve the mysterious case of...")
        print("'The Missing Diamond Necklace'.")
        print("Put your detective skills to the test and unveil the truth!")
        print("Keep your trusty notebook handy to help solve clues")

    def interact_with_characters(self):
        """The interact_with_characters method within the Game class
        demonstrates the interaction with characters,
        where each character's dialogue and unique actions (e.g., providing
        an alibi, sharing an observation) are
        displayed. """

        self.__logger.log("Interactions happening: ")

        if not self.__current_scene.characters:
            print(self.__current_scene.characters)
            print("There's nobody here")
            return
        else:
            print(f"There are a few people are here in {self.__current_scene.location.lower()}")
            print("The noteworthy being: ")
            for i, characters in enumerate(self.__current_scene.characters, start =1):
                print(f"{characters}")

        print("You decide to interact with the characters in the room.")
        character = int(input("If you want to speak to the witness and a "
                           "suspect, "
                        "choose 1. \nIf you'd like to speak to other people in "
                        "the "
                        "room, choose 2: "))

        if character == 1:
            if not self.__current_scene.spoken:
                self.__logger.log("Interacting with suspects and witnesses.")
                print(
                    "You decide to interact with the witness and suspect in "
                    "the room:")

                if self.__present_suspect:
                    clue_suspect = self.__present_suspect.interact()
                    # self.__current_scene.add_clue(clue_suspect)
                    print(clue_suspect)  # keep the outputs going

                    suspect_alibi = self.__present_suspect.provide_alibi()
                    # self.__current_scene.add_clue(suspect_alibi)
                    print(suspect_alibi)

                    # use the new abstract method
                    print(self.__present_suspect.perform_action())

                if self.__present_witness:
                    clue_witness = self.__present_witness.interact()
                    # self.__current_scene.add_clue(clue_witness)
                    print(clue_witness)

                    witness_observation = self.__present_witness.share_observation()
                    self.__current_scene.add_clue(witness_observation)
                    print(witness_observation)

                    # use the new abstract method
                    print(self.__present_witness.perform_action())

                self.__current_scene.spoken = True
            else:
                print(
                    "You have already interacted with the characters. They no "
                    "longer wish to speak to you.")
        elif character == 2:
            if not self.__npcs_interacted:
                self.__logger.log("Interacting with people standing about.")
                # Creating and interacting with characters
                print("You decide to speak to other people in the room:")


                #characters = [indifferent_npc, friendly_npc, hostile_npc]

                for character in self.__current_scene.npcs:
                    print(character.interact())
                    print(character.perform_action())
                print("Your seasoned instincts tell you that these people have nothing to do with the case")

                self.__current_scene.add_clue("Three people are hanging around the "
                                          "scene who have nothing to do with the "
                                          "crime.")

                self.__npcs_interacted = True
            else:
                print("People in the room are tired of you. They no longer "
                      "want to speak to you.")
        else:
            print("You seem to have changed your mind")

    def examine_clues(self):
        # ...
        self.__logger.log("Examination of clues happening")
        # ...
        room_name = self.__current_scene.location

        # from before...
        print("You decide to examine the clues at the crime scene.")
        if not self.__current_scene.investigated:
            if self.__current_scene.stuff:
                print(f"Looking around, you find a ... {self.__current_scene.stuff}")
                self.__current_scene.add_clue(self.__current_scene.stuff)
            else:
                print("There's nothing obvious, maybe look deeper")
            self.__current_scene.investigated = True  # Update room state
            self.__logger.log(f"Clue found in {room_name}: {self.__current_scene.stuff}")
        else:
            print("You've already examined the crime scene clues.")

    def look_around(self):
        # ...
        self.__logger.log("Player checking surroundings: ")
        # ...

        print("You decide to check around to see if you can find anything:")

        # nice output to show which door leads to what.
        # human friendly output starts with 1, default would be 0.
        for i, objects in enumerate(self.__current_scene.objects, start=1):
            print(f"{i}. {objects}")

        try:
            objects_choice = int(input("Enter the number of where you want to investigate deeper: "))

            if 0 < objects_choice < len(self.__current_scene.objects) + 1:  # for valid entry check
                if objects_choice == 1:
                    objects_choice -= 1
                    if not self.__current_scene.checked[objects_choice]:
                        if self.__current_scene.notable[objects_choice] != "nothing":
                            print(f"You decide to investigate the {self.__current_scene.objects[objects_choice]} "
                                  f"with a little work you find ... {self.__current_scene.notable[objects_choice]} ")
                            self.__current_scene.add_clue(f"{self.__current_scene.notable[objects_choice]} "
                                                          f"in {self.__current_scene.objects[objects_choice].lower()}")
                        else:
                            print("You find nothing")
                        self.__current_scene.checked[objects_choice] = True
                        self.__logger.log(f"{self.__current_scene.objects[objects_choice]} was investigated.")

                    else:
                        print("You already checked this out")
                        self.__logger.log(f"{self.__current_scene.objects[objects_choice]}"
                                          f"already investigated. No access.")
                    return
                elif objects_choice == 2:
                    objects_choice -= 1
                    if not self.__current_scene.checked[objects_choice]:
                        if self.__current_scene.notable[objects_choice] != "nothing":
                            print(f"You decide to investigate the {self.__current_scene.objects[objects_choice]} "
                                  f"with a little work you find ... {self.__current_scene.notable[objects_choice]} ")
                            self.__current_scene.add_clue(f"{self.__current_scene.notable[objects_choice]} "
                                                          f"in {self.__current_scene.objects[objects_choice].lower()}")
                        else:
                            print("You find nothing")
                        self.__current_scene.checked[objects_choice] = True
                        self.__logger.log(f"{self.__current_scene.objects[objects_choice]} was investigated.")
                    else:
                        print("You already checked this out")
                        self.__logger.log(f"{self.__current_scene.objects[objects_choice]}"
                                          f"already investigated. No access.")
                    return
                elif objects_choice == 3:
                    objects_choice -= 1
                    if not self.__current_scene.checked[objects_choice]:
                        if self.__current_scene.notable[objects_choice] != "nothing":
                            print(f"You decide to investigate the {self.__current_scene.objects[objects_choice]} "
                                  f"with a little work you find ... {self.__current_scene.notable[objects_choice]} ")
                            self.__current_scene.add_clue(f"{self.__current_scene.notable[objects_choice]} "
                                                          f"in {self.__current_scene.objects[objects_choice].lower()}")
                        else:
                            print("You find nothing")
                        self.__current_scene.checked[objects_choice] = True
                        self.__logger.log(f"{self.__current_scene.objects[objects_choice]} was investigated.")
                    else:
                        print("You already checked this out")
                        self.__logger.log(f"{self.__current_scene.objects[objects_choice]}"
                                          f"already investigated. No access.")
                    return
        except ValueError:
            print("You stand around confused, haven't you done this before?")

        else:
            print("You stare out into space.")
            self.__logger.log("An invalid object was selected")

    def continue_game(self):
        #print("You continue your investigation, determined to solve the mystery...")
        # ...
        self.__logger.log("Continuing the game.")
        print("You decide to take a new angle, checking a different room of the mansion")
        # ...
        print("You pause to decide which room to enter")


        if self.__current_scene == self.__mansion_drawing_room:
            room_select = int(input("1. Upstairs\n"
                                    "2. Kitchen\n"
                                    "3. Garden\n"
                                    ": "))
            if room_select == 1:
                self.__current_scene = self.__upstairs_lobby
                if self.__kitchen.trapped:
                    self.__present_witness= self.__dorothy
                    self.__present_suspect = self.__griselda
                print("You have moved upstairs, the mansion is littered with countless rooms")
            elif room_select == 2:
                print("You walk into the kitchen, the smells of meat and spices fill your nose")
                self.__current_scene = self.__kitchen
                if self.__current_scene.trapped:
                    print("The door slams shut behind you!")
                    self.__logger.log(f"Player trapped in {self.__current_scene.location}")
            elif room_select == 3:
                print("You walk into the garden, you can't help but admire the beautiful arrangements")
                self.__current_scene = self.__garden
                self.__present_witness = self.__james
                self.__present_suspect = self.__juan
            else:
                print("You stand in a daze")
            #self.update_room_state()
        elif self.__current_scene == self.__upstairs_lobby:
            room_select = int(input("1. Downstairs\n"
                                    "2. Library\n"
                                    "3. Study\n"
                                    "4. Trophy room: "))
            if room_select == 1:
                print("You went back downstairs, you find yourself again in the grand drawing room")
                self.__current_scene = self.__mansion_drawing_room
                self.__present_suspect = self.__smith
                self.__present_suspect = self.__parker
            elif room_select == 2:
                print("You enter the library, surrounded by books you continue your investigation")
                self.__current_scene = self.__library
            elif room_select == 3:
                if self.__current_scene.characters:
                    print("The door is blocked by the Head Maid")
                else:
                    print("You enter the supposedly unused study and take note of the active lights")
                    self.__current_scene = self.__study
            elif room_select == 4:
                print("You enter the trophy room, fit with endless awards and antiques")
                self.__current_scene = self.__saferoom
            else:
                print("You trip but rise to your knees, the investigation continues")
        elif self.__current_scene == self.__kitchen:
            if self.__current_scene.trapped:
                print("You try the door but fail, the door has been locked but you can enter a code to open it")
                guess = input("Enter the code: ")
                if guess.lower() == self.__current_scene.code or guess.lower() == "admin":
                    print("The lock creaks ... and opens!")
                    self.__current_scene.trapped = False
                    self.__logger.log(f"{self.__current_scene.location} no longer locked")
                    print("The maids, hearing the noise, have come to clean the mess")
                    self.__present_suspect = self.__griselda
                    self.__present_witness = self.__dorothy

                    self.__kitchen.add_char(self.__griselda)
                    self.__kitchen.add_char(self.__dorothy)
                    self.__upstairs_lobby.remove_char(self.__griselda)
                    self.__upstairs_lobby.remove_char(self.__dorothy)
                    self.__logger.log("Maids have moved room")
                else:
                    print("The lock creaks ... but doesn't open")
                    self.__logger.log(f"Player failed lock")
            else:
                room_select = int(input("1. Drawing Room\n"
                                        ": "))
                if room_select == 1:
                    print("You return to the grand drawing room")
                    self.__current_scene = self.__mansion_drawing_room
                    self.__present_suspect = self.__smith
                    self.__present_witness= self.__parker
        elif self.__current_scene == self.__garden:
            room_select = int(input("1. Drawing Room\n"
                                    ": "))
            if room_select == 1:
                print("You return to the grand drawing room")
                self.__current_scene = self.__mansion_drawing_room
                self.__present_suspect = self.__smith
                self.__present_witness = self.__parker
            else:
                print("You stumble but rise to your feet")
        elif self.__current_scene == self.__study:
            room_select = int(input("1. Back to lobby\n"
                                    ": "))
            if room_select == 1:
                print("You return to the lobby")
                self.__current_scene = self.__upstairs_lobby
            else:
                print("You stumble but rise to your feet")
        elif self.__current_scene == self.__saferoom:
            room_select = int(input("1. Back to lobby\n"
                                    ": "))
            if room_select == 1:
                print("You return to the lobby")
                self.__current_scene = self.__upstairs_lobby
            else:
                print("You stumble but rise to your feet")
        elif self.__current_scene == self.__library:
            if self.__current_scene.checked[1]:
                room_select = int(input("1. Back to lobby\n"
                                        "2. Hidden passage: "))
                if room_select == 1:
                    print("You return to the lobby")
                    self.__current_scene = self.__upstairs_lobby
                elif room_select == 2:
                    print("You make your way through and find yourself in the... trophy room!")
                    self.__current_scene = self.__saferoom
                else:
                    print("You stumble to your feet")
            else:
                room_select = int(input("1. Back to lobby\n"
                                        ": "))
                if room_select == 1:
                    print("You return to the lobby")
                    self.__current_scene = self.__upstairs_lobby
                else:
                    print("You stumble but rise to your feet")

        self.__logger.log(f"Player in {self.__current_scene.location}")


            #self.update_room_state()
        # Additional game content and interactions could go here
    def accuse_suspect(self):
        old_location = self.__current_scene
        if self.__current_scene == self.__kitchen:
            if self.__current_scene.trapped:
                print("You can't exactly do that right now")
                return
        else:
            self.__current_scene = self.__testingRoom


        self.__logger.log("Player moves to accuse")
        print("Are you sure you're ready to find the culprit?")
        print("You won't be able to check your notes here so make sure you know who you're accusing!")
        user_ready = input("Yes/No: ")
        if "y" in user_ready.lower():
            print("Ok get ready")
            for i, suspect in enumerate(self.__current_scene.characters, start = 1):
                print(f"{i}. {suspect}")
            try:
                user_selection = int(input("Select the culprit: "))
                if user_selection == 1:
                    print(f"You point your finger at {self.__current_scene.characters[user_selection-1]}")
                    print(f"They tremble, realising you have found them out")
                    print("You Win! Correct culprit found")
                    self.__logger.log("Correct Culprit Declared")
                elif user_selection > len(self.__current_scene.characters):
                    raise ValueError
                else:
                    print("'You've got it all wrong!' they scream as they're dragged off")
                    print("You can't shake the feeling that somethings wrong")
                    print("You Lose! You sent an innocent to jail")
                    self.__logger.log("Incorrect Culprit Declared")
                self.__logger.log("Game End")
                self.__running = False
            except ValueError:
                print("You stutter, everyone is looking at you")
                self.__current_scene = old_location
        elif "n" in user_ready.lower():
            print("You choke on your words, unsure of your final decision")
            self.__current_scene = old_location
            return
        else:
            print("Thoughts, like magic, disappear from your mind")
            self.__current_scene = old_location
            return



""" deprecated function as I was using a dictionary to update the games state before realising it would be easier
    to simply create different instances of CrimeScene for each room
    def update_room_state(self):
        self.__logger.log("Finding room state.")

        room_name = self.__current_scene.location
        self.__current_scene = CrimeScene(room_name, self.__room_state[room_name]["clue"],
                                        self.__room_state[room_name]["objects"],
                                        self.__room_state[room_name]["checked"])

        if self.__room_state[room_name]["found"]:
            self.__crime_scene.add_clue(self.__room_state[room_name]["clue"])
        if self.__room_state[room_name]["spoken"]:
            self.__crime_scene.add_clue((self.__witness.share_observation()))
            self.__crime_scene.add_clue(self.__suspect.provide_alibi())
        for i, object in enumerate(self.__room_state[room_name]["checked"], start =0):
            if self.__room_state[room_name]["checked"][i]:
                if self.__room_state[room_name]["notable"][i] != "nothing":
                    self.__crime_scene.add_clue(f"{self.__room_state[room_name]["notable"][i]} "
                                                f"in {self.__room_state[room_name]["objects"][i]}")
"""



# Testing the Enhanced Game
if __name__ == "__main__":
    game = Game()
    game.run()

    # Using the logger
    """
    print("\nGame Logs:")
    for log in game.log.logs:
        print(log)
    """
    game.log.write_to_file("logs.txt")