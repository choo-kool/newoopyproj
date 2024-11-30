# CMPU 2016 Object-Oriented Programming - Semester 1 Assignment
# TU857-2
# Group: Josh's Group
#
# Members:
#   1. Joshua Stanley (C23443452).
#   2. Andrew Ugweches (C23767071).
#   3. Donal Harcourt (C23375883).
#   4. Christian Bagrin ().
#   5. Max Doyle ().
#  Date: November 16, 2024
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
    def __init__(self, location, stuff, objects, checked):
        self.location = location
        self.__clues = []
        self.__stuff = stuff
        self.__objects = objects
        self.__checked = checked
        self.__investigated = False

    @property
    def investigated(self):
        return self.__investigated

    @investigated.setter
    def investigated(self, value):
        self.__investigated = value

    def add_clue(self, clue):
        self.__clues.append(clue)

    def examined(self):
        return self.__stuff

    @property
    def checked(self):
        return self.__checked

    @checked.setter
    def checked(self, i):
        self.__checked[i] = True

    def review_clues(self):
        """At the moment there are no checks on who can see the clues. We
        might need some further protection here."""
        return self.__clues

"""
class TrapRoom(CrimeScene):
    def __init__(self, location):
        super().__init__(location, )
        #self.trapped = trapped
        self.investigated = False
        self.clues = []
"""


#class for combination lock, attributes code and if the lock has been solved or not
class CombinationLock:
    def __init__(self):
        self.code =  "ibqjbblr"
        self.solved = False

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code):
        self._code = code

    @property
    def solved(self):
        return self._solved

    @solved.setter
    def solved(self, solved):
        self._solved = solved

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
        super().interact()
        return "\nI know nothing!"

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
        self.__characters_interacted = False  # no double interactions
        self.__npcs_interacted = False # no double interactions

        self.__room_state = {
            "Mansion's Drawing Room": {"clue": "Torn piece of fabric", "found": False, "spoken": False,
                        "objects": ["cabinet", "drawer", "mouse"],
                        "checked":[False, False, False],
                        "notable": ["a bloody spoon", "an old receipt", "nothing"]},
            "Upstairs": {"clue": "Cigarette box", "found": False, "spoken": False,
                         "objects": ["The carpet", "The balcony", "The ladder"],
                         "checked":[False, False, False],
                         "notable": ["ash", "nothing", "nothing"]},
        }


        self.__crime_scene = CrimeScene("Mansion's Drawing Room",
                                        self.__room_state["Mansion's Drawing Room"]["clue"],
                                        self.__room_state["Mansion's Drawing Room"]["objects"],
                                        self.__room_state["Mansion's Drawing Room"]["checked"])

        self.__suspect = Suspect("Mr. Smith", "I was in the library all "
                                            "evening.", "Confirmed by the butler.")
        self.__witness = Witness("Ms. Parker", "I saw someone near the window "
                                             "at the time of the incident.",
                               "Suspicious figure in dark clothing.")

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
                "ACTIONS:\n'q' to quit, 'c' to continue, \n's' to speak"
                "\n'e' to examine clues, 'r' to review clues from this room, \n'l' to look around, "
                "or 'n' to open your notepad\n: ")

            if player_input.lower() == "q":
                self.__running = False
            elif player_input.lower() == "c":
                self.continue_game()
            elif player_input.lower() == "s":
                self.interact_with_characters()
            elif player_input.lower() == "e":
                self.examine_clues()
            elif player_input.lower() == "l":
                self.look_around()
            elif player_input.lower() == "r":
                clues = self.__crime_scene.review_clues()
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

        room_name = self.__crime_scene.location


        print("You decide to interact with the characters in the room.")
        character = int(input("If you want to speak to the witness and a "
                           "suspect, "
                        "choose 1. \nIf you'd like to speak to other people in "
                        "the "
                        "room, choose 2: "))

        if character == 1:
            if not self.__room_state[room_name]["spoken"]:
                self.__logger.log("Interacting with suspects and witnesses.")
                print(
                    "You decide to interact with the witness and suspect in "
                    "the room:")

                clue_suspect = self.__suspect.interact()
                #self.__crime_scene.add_clue(clue_suspect)
                print(clue_suspect)  # keep the outputs going

                suspect_alibi = self.__suspect.provide_alibi()
                self.__crime_scene.add_clue(suspect_alibi)
                print(suspect_alibi)

                # use the new abstract method
                print(self.__suspect.perform_action())

                clue_witness = self.__witness.interact()
                #self.__crime_scene.add_clue(clue_witness)
                print(clue_witness)

                witness_observation = self.__witness.share_observation()
                self.__crime_scene.add_clue(witness_observation)
                print(witness_observation)

                # use the new abstract method
                print(self.__witness.perform_action())

                self.__room_state[room_name]["spoken"] = True
            else:
                print(
                    "You have already interacted with the characters. They no "
                    "longer wish to speak to you.")
        elif character == 2:
            if not self.__npcs_interacted:
                self.__logger.log("Interacting with people standing about.")
                # Creating and interacting with characters
                print("You decide to speak to other people in the room:")
                indifferent_npc = NPC("Beatrice", "How do you do.")
                friendly_npc = NPC("Seamus", "Welcome to our village.")
                hostile_npc = NPC("Evil Goblin", "Leave this place!")

                characters = [indifferent_npc, friendly_npc, hostile_npc]

                for character in characters:
                    print(character.interact())
                    print(character.perform_action())

                self.__crime_scene.add_clue("Three people are hanging around the "
                                          "scene who have nothing to do with the "
                                          "crime.")

                self.__npcs_interacted = True
            else:
                print("People in the room are tied of you. They no longer "
                      "want to speak to you.")
        else:
            print("This was not an option.")

    def examine_clues(self):
        # ...
        self.__logger.log("Examination of clues happening")
        # ...
        room_name = self.__crime_scene.location

        # from before...
        print("You decide to examine the clues at the crime scene.")
        if not self.__room_state[room_name]["found"]:
            print(f"Looking around, you find a ... {self.__room_state[room_name]['clue']}")
            self.__crime_scene.add_clue(self.__room_state[room_name]["clue"])
            self.__room_state[room_name]["found"] = True  # Update room state
            self.__logger.log(f"Clue found in {room_name}: {self.__room_state[room_name]['clue']}")
        else:
            print("You've already examined the crime scene clues.")

    """
    def trapped_room(self):

        # Instances of Trap Room class
        trapped_room = TrapRoom("Kitchen")
        clues_undiscovered = True

        trapped_clue1 = TrapRoom("Cupboards")
        trapped_clue2 = TrapRoom("Counter")
        trapped_clue3 = TrapRoom("Fridge")

        lock = CombinationLock()

        self.__logger.log("Player gets trapped in the kitchen")

        print(f"You are now trapped in the kitchen, you must figure out the combination for the lock")
        print(f"You decide to look around for clues on how to solve the lock")

        # While statement to keep asking user to make sure they check all the clues finished once they found all the clues

        while not lock.solved:
            lock_choice = int(input(
                "To try guess the lock combination enter 1, to think about the clues you have been given enter 2: "))

            if lock_choice == 1:
                user_guess = str(input("Enter the combination for the lock: "))
                if user_guess == lock.code:
                    print("You have solved the cypher")
                    # Lock has been solved, instance of lock solved attribute changed to True
                    lock.solved = True
                else:
                    print("The combination you tried was incorrect")

            if lock_choice == 2:
                print(trapped_clue1.review_clues())
                print(trapped_clue2.review_clues())
                print(trapped_clue3.review_clues())



        # once condition is met after lock has been solved the user breaks out of method with return
        if lock.solved:
            print(f"You have escaped the {trapped_room.location}!")
            return
    """

    def look_around(self):
        # ...
        self.__logger.log("Player checking surroundings: ")
        # ...
        room_name = self.__crime_scene.location

        print("You decide to check around to see if you can find anything:")

        # nice output to show which door leads to what.
        # human friendly output starts with 1, default would be 0.
        for i, objects in enumerate(self.__room_state[room_name]["objects"], start=1):
            print(f"{i}. {objects}")

        objects_choice = int(input("Enter the number of where you want to investigate deeper: "))

        if 0 < objects_choice < len(self.__room_state[room_name]["objects"])+1: # for valid entry check
            if objects_choice == 1:
                if not self.__room_state[room_name]["checked"][0]:
                    if self.__room_state[room_name]["notable"][0] != "nothing":
                        print(f"You decide to investigate the {self.__room_state[room_name]["objects"][0]} "
                              f"with a little work you find ... {self.__room_state[room_name]["notable"][0]} ")
                        self.__crime_scene.add_clue(f"{self.__room_state[room_name]["notable"][0]} "
                                                    f"in {self.__room_state[room_name]["objects"][0]}")
                    else:
                        print("You find nothing")
                    self.__room_state[room_name]["checked"][0] = True
                    self.__logger.log(f"{self.__room_state[room_name]["objects"][objects_choice-1]} was investigated.")
                else:
                    print("You already checked this out")
                    self.__logger.log(f"{self.__room_state[room_name]["objects"][objects_choice-1]}"
                                      f"already investigated. No access.")
            elif objects_choice == 2:
                if not self.__room_state[room_name]["checked"][1]:
                    if self.__room_state[room_name]["notable"][1] != "nothing":
                        print(f"You decide to investigate the {self.__room_state[room_name]["objects"][1]} "
                              f"with a little work you find ... {self.__room_state[room_name]["notable"][1]} ")
                        self.__crime_scene.add_clue(f"{self.__room_state[room_name]["notable"][1]} "
                                                    f"in {self.__room_state[room_name]["objects"][1]}")
                    else:
                        print("You find nothing")
                    self.__room_state[room_name]["checked"][1] = True
                    self.__logger.log(f"{self.__room_state[room_name]["objects"][objects_choice-1]} was investigated.")
                else:
                    print("You've checked this already.")
                    self.__logger.log(f"{self.__room_state[room_name]["objects"][objects_choice-1]}"
                                      f"already investigated. No access.")
            elif objects_choice == 3:
                if not self.__room_state[room_name]["checked"][2]:

                    """
                    print("You open the kitchen door. You step into the room and the door behind slams shut "
                          " you turn around in time and see a lock on the door slip shut.  "
                          " You inspect the lock. The lock is an advanced with a digital screen and a keyboard"
                          " to enter the combination, the keyboard has the letters of the alphabet on it")

                    
                    self.trapped_room()
                    """
                    if self.__room_state[room_name]["notable"][2] != "nothing":
                        print(f"You decide to investigate the {self.__room_state[room_name]["objects"][2]} "
                              f"with a little work you find ... {self.__room_state[room_name]["notable"][2]} ")
                        self.__crime_scene.add_clue(f"{self.__room_state[room_name]["notable"][2]} "
                                                    f"in {self.__room_state[room_name]["objects"][2]}")
                    else:
                        print("You find nothing")

                    self.__room_state[room_name]["checked"][2] = True
                    self.__logger.log(f"{self.__room_state[room_name]["objects"][objects_choice-1]} was investigated.")
                else:
                    print("You've checked this out already.")
                    self.__logger.log(f"{self.__room_state[room_name]["objects"][objects_choice-1]}"
                                      f"already investigated. No access.")
        else:
            print("You stare out into space.")
            self.__logger.log("An invalid object was selected")

    def continue_game(self):
        print("You continue your investigation, determined to solve the mystery...")
        # ...
        self.__logger.log("Continuing the game.")
        print("You decide to take a new angle, checking a different room of the mansion")

        # ...
        if self.__crime_scene.location == "Mansion's Drawing Room":
            print("You have moved upstairs, the mansion is littered with countless rooms")
            self.__crime_scene.location = "Upstairs"
            self.update_room_state()


        else:
            print("You went back downstairs, you find yourself again in the grand drawing room")
            self.__crime_scene.location = "Mansion's Drawing Room"
            self.update_room_state()
        # Additional game content and interactions could go here

    def update_room_state(self):
        self.__logger.log("Finding room state.")

        room_name = self.__crime_scene.location
        self.__crime_scene = CrimeScene(room_name, self.__room_state[room_name]["clue"],
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




# Testing the Enhanced Game
if __name__ == "__main__":
    game = Game()
    game.run()

    # Using the logger
    print("\nGame Logs:")
    for log in game.log.logs:
        print(log)
    game.log.write_to_file("logs.txt")