# selenium-booking
Python version 3.6.2
Chrome version 60.0.3112.113

Argparse working with default arguments, because of different site structure (class names etc.) with different arguments.
Did not realize different site structure in this version.

Search in Samara, Samarskaya oblast, Russia from current date to date after 4 days with 1 room, 2 adults and 0 children args.
Choose Samara in the second page.

Loop through the all available hotels on all pages and if
1. Hotel has price.
2. Price for 1 night less or equal than 6800 rub.
3. Hotel has score.
write it to the dictionary with hotel URL.

After that compare score.
Finally open best hotel URL and screen.
