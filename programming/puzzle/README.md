    At last, we've found you!
    We must solve this puzzle, and according to the prophecy - you are the one to solve it.

    This puzzle is weird. It consists of a board with 10 columns and 10 rows, so there are 100 pieces.Yet, each piece is weird! It has four 'slices' - a top slice, a right slice, a bottom slice and a left slice.
    Each slice consists of a number. For example, consider this piece:
------------
|  \ 12 /  |
| 5 \  / 3 |
|   /  \   |
|  / 4  \  |
------------

Its top is 12, its right is 3, its bottom is 4 and its left is 5.
For the puzzle to be solved, all pieces must be sorted into the board, where each slice is equal to its adjacent slice.
In addition, a slice that has no adjacent slice (that is, the slice is a part of the board's border), must be 0. Other slices are never 0.
For example, the following board (with 4 pieces) is valid:
------------------------
|  \ 0  /  ||  \ 0  /  |
| 0 \  / 9 || 9 \  / 0 |
|   /  \   ||   /  \   |
|  / 17 \  ||  / 11 \  |
------------------------
------------------------
|  \ 17 /  ||  \ 11 /  |
| 0 \  / 6 || 6 \  / 0 |
|   /  \   ||   /  \   |
|  / 0  \  ||  / 0  \  |
------------------------

In the board above, all the border slices are equal to 0.
Consider the top-left piece. Its right slice is equal to 9, and its adjacent slice (the left slice of the top-right piece) also equals 9.

Unfortunately, we have the pieces in a shuffled order. They are given in the following format:
cube_id, [slices]; cube_id, slices; ... cube_id, slices
Where cube_id is a number from 0 to 99, and slices include the numbers in the order: top, right, bottom, left.

For instance, consider the following shuffled board:
------------------------------------
|  \ 0  /  ||  \ 0  /  ||  \ 5  /  |
| 18\  / 12|| 19\  / 7 || 19\  / 0 |
|   /  \   ||   /  \   ||   /  \   |
|  / 2  \  ||  / 6  \  ||  / 0  \  |
------------------------------------
------------------------------------
|  \ 6  /  ||  \ 14 /  ||  \ 7  /  |
| 10\  / 2 || 10\  /  0|| 0 \  / 12|
|   /  \   ||   /  \   ||   /  \   |
|  / 9  \  ||  / 5  \  ||  / 0  \  |
------------------------------------
------------------------------------
|  \ 0  /  ||  \ 0  /  ||  \ 0  /  |
| 7 \  / 0 || 7 \  / 17|| 17\  / 0 |
|   /  \   ||   /  \   ||   /  \   |
|  / 18 \  ||  / 9  \  ||  / 14 \  |
------------------------------------

A string describing the above board is the following one:
'0,[0, 12, 2, 18]; 1,[0, 7, 6, 19]; 2,[5, 0, 0, 19]; 3,[6, 2, 9, 10]; 4,[14, 0, 5, 10]; 5,[7, 12, 0, 0]; 6,[0, 0, 18, 7]; 7,[0, 17, 9, 7]; 8,[0, 0, 14, 17]'

We need you to solve the puzzle!

Provide us a string that looks exactly as follows:
cube_id, times_to_rotate_clockwise; cube_id, times_to_rotate_clockwise;... cube_id, times_to_rotate_clockwise

For example, a solution string will look like this:
2,2; 1,0; 6,0; 4,2; 3,0; 0,1; 8,2; 7,2; 5,3

The above string corresponds to the following (valid) puzzle:
------------------------------------
|  \ 0  /  ||  \ 0  /  ||  \ 0  /  |
| 0 \  / 19|| 19\  / 7 || 7 \  / 0 |
|   /  \   ||   /  \   ||   /  \   |
|  / 5  \  ||  / 6  \  ||  / 18 \  |
------------------------------------
------------------------------------
|  \ 5  /  ||  \ 6  /  ||  \ 18 /  |
| 0 \  / 10|| 10\  / 2 || 2 \  / 0 |
|   /  \   ||   /  \   ||   /  \   |
|  / 14 \  ||  / 9  \  ||  / 12 \  |
------------------------------------
------------------------------------
|  \ 14 /  ||  \ 9  /  ||  \ 12 /  |
| 0 \  / 17|| 17\  / 7 || 7 \  / 0 |
|   /  \   ||   /  \   ||   /  \   |
|  / 0  \  ||  / 0  \  ||  / 0  \  |
------------------------------------

Consider the top-left piece. In the string, it corresponds to '2,2', as we take cube number 2 from the input:
2,[5, 0, 0, 19]
But we rotate it clock-wise, twice, so we get [0,19,5,0].

Now consider the top-middle piece. In the string, it corresponds to '1,0'. That is, we take cube number 1 from the input:
1,[0, 7, 6, 19]
And we don't rotate it at all (that is, rotate it 0 times) - as it's already in the right direction.

Got it?
Help us solve the puzzle!
The puzzle we have is:


Good luck!