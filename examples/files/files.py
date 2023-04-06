'''Notes on how to manipulate files in Python.

-- How Files Work in Linux(-like) systems 

POSIX file permissions are a set of permissions that are used to control access to files and directories on 
Unix and Unix-like systems. POSIX is a set of standards that defines how Unix-like operating systems should 
behave, and it specifies the file permissions that are used on these systems.

There are three types of permissions that can be set for a file or directory: read, write, and execute. Each of 
these permissions can be set for three different types of users: the owner of the file or directory, members of 
the group that the file or directory belongs to, and all other users.

The read permission allows a user to view the contents of a file or directory. The write permission allows a user 
to modify the contents of a file or directory, including creating and deleting files. The execute permission allows 
a user to run a file as a program or to access a directory and its contents.

The permissions for each of these three types of users are represented by three sets of three bits. The first set 
of three bits represents the permissions for the owner of the file, the second set represents the permissions for 
the group, and the third set represents the permissions for all other users. The bits can be either set (1) or unset 
(0), depending on whether the corresponding permission is allowed or not.

For example, the permissions "rwxr-xr--" would allow the owner of the file to read, write, and execute the file, 
members of the group to read and execute the file, and all other users to only read the file.
'''



'''Now, we'll get into python code. Here's how you write to files,
the code below opens a file for writing. "w" indicates that you are opening it for writing.
'''
fp = open('my_file','w')

'''You can only write to a file if you have "write" permission. fp is called a file pointer, 
to write data to this file you can run:
'''
fp.write('my data')

'''After you are done writing you should close the file 
'''
fp.close()

'''An equivalent way of expressing the same syntax above (but more readable) is:
'''
with open('my_file','w') as fp:
    fp.write('my data')

'''writing fully replaces the contents of a file
'''


'''You can also "append" to a file, which adds the new data to the end. "a" indicates
you are opening it for appending
'''
fp = open('my_file','a')

'''You can only append to a file if you have "write" permission. fp is called a file pointer, 
to write data to this file you can run:
'''
fp.write('my data')

'''After you are done writing you should close the file 
'''
fp.close()


'''Reading from a file is similar as well
'''
fp = open('my_file','r')

'''You can only read from a file if you have "read" permission, the following code takes the
data and stores it in string
'''
data = fp.read()

'''After you are done writing you should close the file 
'''
fp.close()

'''or equivalently
'''
with open('my_file','r') as fp:
    data = fp.read()
