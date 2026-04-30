# Possible improvements to the QueryVlcb project
## Filters to receiveMessage() 
Apply a filter to reduce the amount of messages that need to be processed.

## Higher level function that looks at response #0
Where the 0th response contains a response count we can return when that number
of responses has been received. 
No need for a timeout that slows down things.

## More testing with mocks.