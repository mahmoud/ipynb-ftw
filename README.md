## IPYNB-FTW
_A collection of IPython Notebooks_

This is a collection of IPython notebooks automatically uploaded (using incron) from my server.

The code in the ipynb files is going to be messy and incomplete, and there are probably going to be lots of them and lots of commits, if I do this right. I'm sorry. I promise to write lots of educational blogposts on [Python Does What](http://pythondoeswhat.blogspot.com).

If you're interested in IPython notebooks, [see here](http://ipython.org/ipython-doc/dev/interactive/htmlnotebook.html).

If you're interested in incron, see [here](http://makuro.wordpress.com/2009/10/16/less-and-incron/) and [here](http://www.cyberciti.biz/faq/linux-inotify-examples-to-replicate-directories/).

-----
Command to run: `ipython notebook --script --pprint --no-browser --ip='0.0.0.0' --port='3389' --pylab inline --logappend='ipy_log.txt' --log-level='INFO' 2>> ipy_stderr.txt &`

Notes on setting up the shared repo for auto commits:

  * umask 002
  * git init --shared (using ipy group)
  * find . -type d -exec chmod u+s,g+s {} \; # add guid/suid to directories (suid ignored on directories in Linux)