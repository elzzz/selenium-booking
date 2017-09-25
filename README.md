# booking.com UI test
booking.com UI test case:

Search for the best fit hotel in the specified region.

### Steps to Reproduce:
1. Navigate to the web-site http://booking.com
2. Fill the filter fields with the values:
  * region: "Самара, Самарская область, Россия".
  * duration: 4 days starting from today.
  * number of rooms: 2.
  * number of adults: 1.
  number of kids: 0.
3. Press "Начнем!" button.
4. Iterate through all the pages.
5. Collect entire resultant hotels list:
  * Exclude non-priced hotels from the list.
  * Price does not exceed 6800 roubles.
  * Hotel has scores to compare.
6. Iterate through hotels list and get the top scored hotel selected.
7. Store the screenshot of the chosen hotel.

Expected result:
Hotel "Bristol" will be selected.
________________________________________________________
### How to run the test:
1. Make sure prerequisites are installed:
  * Python 3.6
  * PIP 9.0.1
2. Install the libraries:
  > pip -r requirements.txt
3. Run the test itself:
  > python booking.py -r=1 -a=2 -c=0
