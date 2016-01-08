#!/bin/bash -e

while [[ $# > 0 ]]
do
    key="$1"
    case key in
        -i|--input)
            # This is the local directory to mount inside the container at
            # /data/input
            DINPUT="$2"
            shift
            ;;
        -o|--output)
            # This is the local directory to mount inside the container at
            # /data/output
            DOUTPUT="$2"
            shift
            ;;
        -f|--file)
            # The file name -- inside DINPUT -- to be used as argument to
            # for the binary (whatever it is) execd by the container.
            DFILE="$2"
            shift
            ;;
        *)
            # Name of the image to run. This name should be among the listed
            # ones within the system's config files, at $DOCKERRIDIR
            DIMAGE=$key
            ;;
    esac
    shift
done

