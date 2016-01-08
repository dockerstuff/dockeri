#!/bin/bash -e

# Read INI config file
#
config_parser()
{
    ini="$(<$1)"                # read the file
    ini="${ini//[/\[}"          # escape [
    ini="${ini//]/\]}"          # escape ]
    #OLDIFS=$IFS
    IFS=$'\n' && ini=( ${ini} ) # convert to line-array
    ini=( ${ini[*]//;*/} )      # remove comments with ;
    ini=( ${ini[*]/\    =/=} )  # remove tabs before =
    ini=( ${ini[*]/=\   /=} )   # remove tabs be =
    ini=( ${ini[*]/\ =\ /=} )   # remove anything with a space around =
    ini=( ${ini[*]/#\\[/\}$'\n'cfg.section.} ) # set section prefix
    ini=( ${ini[*]/%\\]/ \(} )    # convert text2function (1)
    ini=( ${ini[*]/=/=\( } )    # convert item to array
    ini=( ${ini[*]/%/ \)} )     # close array parenthesis
    ini=( ${ini[*]/%\\ \)/ \\} ) # the multiline trick
    ini=( ${ini[*]/%\( \)/\(\) \{} ) # convert text2function (2)
    ini=( ${ini[*]/%\} \)/\}} ) # remove extra parenthesis
    ini[0]="" # remove first element
    ini[${#ini[*]} + 1]='}'    # add the last brace
    #IFS=$OLDIFS
    eval "$(echo "${ini[*]}")" # eval the result
}

read_config(){
    _img="$1"
    _file="$2"
    config_parser $_file
    if [[ cfg.section.main ]]
    then
        IMGNAME=$image
    else
        IMGNAME=$_img
    fi
    if [[ cfg.section.volumes ]]
    then
        INPUT=${input-""}
        OUTPUT=${output-""}
        X11=${x11-""}
    fi
}

# Verify the existence of the variable locating the config files.
# If not defined, try to see if there is the default location.
#
config_location(){
    if [[ -z "$DOCKERRIDIR" ]]
    then
        _DRIDIR="${HOME}/.dockerri"
        if [[ ! -d "${_DRIDIR}" ]]
        then
            return 1
        fi
        DOCKERRIDIR=$_DRIDIR
        export DOCKERRIDIR
    fi
    return 0
}

# Read the image config files inside $DOCKERRIDIR, if it is defined.
# Otherwise, try to run an image from the hub named as given
#
_imglistdir="images.list.d"
search_config(){
    # 1st argument is the name of the image
    _IMG="$1"
    [[ config_location ]] || return 1
    DRIIMGLIST="${DOCKERRIDIR}/${_imglistdir}"
    for f in `ls -1 $DRIIMGLIST`
    do
        _fimg=$(echo $f | cut -d"." -f1)
        if [[ "$_fimg" = "$_IMG" ]]
        then
            read_config $_IMG $f
        fi
    done
}
