#!/bin/bash
while read str
 do echo ${str};
    /usr/bin/python interface.py route ${str};
    sleep 1s;
done < resource
