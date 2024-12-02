# newoopyproj


This project is a text-driven adventure game surrounding the mystery of a stolen necklace within a Grand mansion.

This game was started originally as a group project, but out of curiousity and as an attempt to learn more about OOP principles, I rewrote our group's code from the ground up. This was an attempt to make the game much more polymorphic and generally adhere to OOP principles as I felt that our group was suffering from scope creep.

This project was a bit of a nightmare at first but I think I began to understand OOP concepts much more by doing this. A big change in my understanding happened about halfway through the codign where I essentially underwent an entire revision of the logic. Speaking of revisions, I have been trying to familiarsie myself more with Git and Git bash and was using it to enable version control. I have much to learn in terms of branches and HEAD as the current commit history is actually incorrect. When I checked my github the morning after the submission I realised the code here was several commits behind, this confused me as I had been successfully committing and pushing code the entire day onto the main branch. For whatever reason this was all lost and when I opened bash the HEAD was detached. 

It took a fair bit of work and googling but I managed to use the zipped submission to restore the commit history and forcefully push this on top of the main branch, updating the code to the current state but deleting a few files including this README that you are currently reading! This is now the second time I have written it, but now fit with the tragic story of my version control failures. Alas it is all an experience and I think this will scar me for a long time.

In the future I think it is more appropriate to have rebased the code as opposed to force pushing it on top, that way I would have combined the commit history I believe?

Anyway the game is pretty cool feel free to check it out.

Within the game you can examine clues in rooms, talk to important characters or npcs, investigate cabinets and other objects of interest. The main problem I found was trying to save the state of these and tie it do my room classes, initially I solved this was by creating a dictionary. This was then improved by tying all the information directly to the crimeScene classes and creating objects of the crimescene class for each Room in the mansion.

Once you're ready, the player can accuse whoever they like based on the clues they received, but only one suspect is correct. I think this implementation is pretty fun as it allows people to accuse whoever they like once they feel they have come to a conclusion, not forcing them to find every single thing in the house and have the answer more obvious.

Anyway there is always much to learn and I hope to eventually look back at this code and see how much can be improved.

