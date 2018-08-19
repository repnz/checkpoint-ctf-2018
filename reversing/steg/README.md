### Bowsers Secret Message

We uncovered Bowser’s old laptop!

Everything was wiped except for 3 files, he must have used them to send his evil henchmen --Steganos & Graphein-- a secret message.

Help us!

+--------------------------+  
+-------¦¦¦¦¦¦¦¦¦¦¦¦-------¦  
+-----¦¦            ¦¦¦¦---¦  
+---¦¦                  ¦¦-¦  
+---¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦---¦  
+-¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦-¦  
+-¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦-¦  
+---¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦---¦  
+-----¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦-----¦  
+---¦¦    ¦¦¦¦    ¦¦-------¦  
+-¦¦        ¦¦¦¦    ¦¦-----¦  
+-¦¦        ¦¦¦¦¦¦¦¦¦¦-----¦  
+---¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦-----¦  
+---¦¦¦¦¦¦      ¦¦¦¦¦¦-----¦  
+-----¦¦          ¦¦-------¦  
+-----¦¦¦¦¦¦¦¦¦¦¦¦¦¦-------¦  
+--------------------------+  

## Solution

1) reverse the enc.py script
2) find out that the file contains a steganography hide function to hide the meessage in a gif file this way:
	- put ''.join(set(map(string.upper, flag))) in a comment block in the beginning of the file
	- Now, start hiding indexes to this set:
	- for each block in the file, if it is a GraphicsControlBlock change the delay if there are more characters to hide
	- if a block is ImageDescriptorBlock, add a GraphicsControlBlock and another ImageDescriptor block containing the character info
	- The is_upper is hidden in the transparent_color_index of that GraphicsControlBlock
	- The index of the character is hidden in x, y, w, h of the ImageDescriptor
3) Now write an extraction function

	