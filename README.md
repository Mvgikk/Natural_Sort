Description of the method used.

I used natural merge sort with the 2+1 scheme. Two tapes are used for distribution and one for merging. Operations are performed through simulation of block access.
Each pass begins with a distribution phase, in which series of 3 tapes are distributed on tape 1 and 2, respectively, in increasing order.
After the distribution phase, the merging phase follows, in which corresponding pairs of series are merged. As a result, the total number of series after each pass is reduced by approximately half, because it is possible to automatically merge series in which the records are already sorted.
Subsequent passes are repeated until all records are in the correct order on tape 3.

Record Type.

Complex Numbers.
Ordered according to the rule: complex number z1 is greater than complex number z2 if the modulus of z1 is greater than the modulus of z2.

Test file format specification

The program offers the possibility to generate records - complex numbers, with values (-100, 100) of the real and imaginary parts.
In the test file, records are separated by a new line. Each of them is a complex number.
Files are saved in text format.

Program output

Before sorting, we can decide on the source of the records. We can generate the contents of the file to be sorted or provide our own file with records.
Then, the input records are displayed along with the sorting criterion.
The program offers the possibility to display the contents of each tape at each sorting phase.
After the program finishes, the number of disk operations and the number of sorting passes are displayed.


Experiment on 10 test files with the number of records ranging from 50 to 50,000 was conducted. The buffer size for each test was set to 512.


![image](https://user-images.githubusercontent.com/67462828/235176699-7fbebda0-12d5-4748-a7f8-9cea30c9f51f.png)

