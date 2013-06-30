# Pre-requisites

It is assumed that you have a Raspberry Pi computer and an attached stepper motor (more detail needed...).

# Installing

To keep the files together whilst not making the installation needlessly complicated, make a folder:

    sudo mkdir /usr/local/bin/whereclock

Copy the little webserver and the stepper motor driver in there:

    sudo cp whereclock.py /usr/local/bin/whereclock
    sudo cp Stepper.py /usr/local/bin/whereclock

To make it start and stop nicely there is an init script provided.  This needs putting in the right place:

    sudo cp whereclock.sh /etc/init.d

To activate the script we need one more command which adds symbolic links in the right places in the /etc/rc.x directories:

    sudo update-rc.d whereclock.sh defaults

Next time the Raspberry Pi boots, the whereclock will start up.

# Running

Rebooting the Raspberry Pi should start it up but you can also start and stop it mnually using these two commands:

    sudo /etc/init.d/whereclock.sh start
    sudo /etc/init.d/whereclock.sh stop

