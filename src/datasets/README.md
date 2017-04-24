This folder includes all the various methods we've tried for storing
and accessing the input data. The winner was CDictDataset with CFlight
They are written in Cython and to use them, you need to run build.sh [bash] first.
That compiles the modules as shared libraries which you can then import into
standard python code.

We have found out that compiling the original python code with Cython reduces
it's runtime to 50 - 30% of the original, even though very little functional
changes were made.

Cython would be able to load the data even much faster, but unfortunately not
when we wanted to use Python strings as dict keys.
