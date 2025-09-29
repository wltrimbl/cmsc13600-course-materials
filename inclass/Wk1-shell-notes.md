# Some shell data tricks; slicing and dicing text files: 

# wc -l           # count the lines in the input
# grep <pattern>  # output lines from the input that match pattern
# sort            # sorts lines in lexicographic order
# uniq            # output only unique lines (when input is sorted)
# uniq -c         # count number of adjacent, identical lines
# cat  <filename> # dump contents of <filename> to terminal
# cat  <filename>  | grep <pattern>    # sent output of cat as input of grep
# cut             # filter columns:
# cut -d , -f 5   # retain only the 5th column (using commas as separator) 

# to analyze this for questions like "how many 4th years are there" or
# "How many biosci majors are ther", we could select rows (with grep)

$ cat roster.csv | grep Data |wc -l 
      19

$ cat roster.csv | wc -l 
      70
# or we can slice by columns with cut

$ cut -d , -f 5 roster.csv 
Dept
"UGD: Economics"
"UGD: College International Exchange"
"UGD: Computer Science"
"UGD: Economics"
"UGD: Data Science"
"UGD: Computer Science"
"UGD: Data Science"
"UGD: History"
"UGD: Statistics"
"UGD: Economics"
"UGD: Economics"
"UGD: Biological Sciences"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Computer Science"
"UGD: Cognitive Science"
"UGD: Common Year"
"UGD: Computer Science"
"UGD: Data Science"
"UGD: Biological Sciences"
"UGD: Economics"
"UGD: Data Science"
"UGD: Computer Science"
"UGD: Economics"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Common Year"
"UGD: Economics"
"UGD: Economics"
"UGD: Data Science"
"UGD: Economics"
"UGD: Sociology"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Computer Science"
"UGD: Data Science"
"UGD: Economics"
"UGD: Data Science"
"UGD: Economics"
"UGD: Computer Science"
"UGD: Economics"
"UGD: Economics"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Economics"
"UGD: Neuroscience"
"UGD: Computer Science"
"UGD: Sociology"
"UGD: Economics"
"UGD: Economics"
"UGD: Data Science"
"UGD: Economics"
"UGD: College International Exchange"
"UGD: Economics"
"UGD: Chemistry"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Common Year"
"UGD: Computer Science"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Economics"
"UGD: Data Science"
"UGD: Mathematics"
"UGD: Biological Sciences"

# sorting these will get us closer to a histogram:
$ cut -d , -f 5 roster.csv | sort 
"UGD: Biological Sciences"
"UGD: Biological Sciences"
"UGD: Biological Sciences"
"UGD: Chemistry"
"UGD: Cognitive Science"
"UGD: College International Exchange"
"UGD: College International Exchange"
"UGD: Common Year"
"UGD: Common Year"
"UGD: Common Year"
"UGD: Computer Science"
"UGD: Computer Science"
"UGD: Computer Science"
"UGD: Computer Science"
"UGD: Computer Science"
"UGD: Computer Science"
"UGD: Computer Science"
"UGD: Computer Science"
"UGD: Computer Science"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Data Science"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: Economics"
"UGD: History"
"UGD: Mathematics"
"UGD: Neuroscience"
"UGD: Sociology"
"UGD: Sociology"
"UGD: Statistics"
Dept

# | sort | uniq will get us to number of unique majors:
$ cut -d , -f 5 roster.csv | sort  | uniq 
"UGD: Biological Sciences"
"UGD: Chemistry"
"UGD: Cognitive Science"
"UGD: College International Exchange"
"UGD: Common Year"
"UGD: Computer Science"
"UGD: Data Science"
"UGD: Economics"
"UGD: History"
"UGD: Mathematics"
"UGD: Neuroscience"
"UGD: Sociology"
"UGD: Statistics"
Dept
$ cut -d , -f 5 roster.csv | sort  | uniq  -c 
   3 "UGD: Biological Sciences"
   1 "UGD: Chemistry"
   1 "UGD: Cognitive Science"
   2 "UGD: College International Exchange"
   3 "UGD: Common Year"
   9 "UGD: Computer Science"
  19 "UGD: Data Science"
  25 "UGD: Economics"
   1 "UGD: History"
   1 "UGD: Mathematics"
   1 "UGD: Neuroscience"
   2 "UGD: Sociology"
   1 "UGD: Statistics"
   1 Dept
$ cut -d , -f 6 roster.csv | sort  | uniq  -c 
   2 00
   4 02
  12 03
  51 04
   1 YearOfStudy
$ cut -d , -f 7 roster.csv | sort  | uniq  -c 
  22 
  26 He/Him/His
   1 PronounsOfReference
  20 She/Her/Hers
   1 They/Them/Theirs
$ 
# Note here that the empty field is the second-most-common value, and
# that the column header ends up in the histogram.
