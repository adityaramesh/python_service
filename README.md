<!--
  ** File Name:	README.md
  ** Author:	Aditya Ramesh
  ** Date:	01/16/2014
  ** Contact:	_@adityaramesh.com
-->

# Introduction

The `python_service` library makes it easy to write init scripts conforming to
the conventions of various Linux distributions. If the daemon is to be written
in Python, the daemonization process and PID file management are done
automatically. Interprocess communication is used to achieve robust logging and
error reporting for both initialization and termination.

# TODO

  - Use `sigaction` and `sigqueue` to send the child process a semaphore instead
  of using `SIGTERM` and `SIGKILL`.
  - Ideally, we would use a semphore to achieve commuincation between the parent
  and child processes, but this would pose the following challenges:
    - One would have to dig through the Python source code to figure out how to
    get the internal kernel-specific handle to the semaphore, as well as any
    other required information.
    - When terminating the child process via `sigaction`, one would have to
    allocate a segment of shared memory in order to communicate this information
    to the deamon. The descriptor to write end of the pipe conveniently fits in
    the integer component of the `siginfo_t` struct.
