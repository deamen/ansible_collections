get_git_paths() {
    if [ -f /etc/redhat-release ]; then
        if grep -q "Red Hat Enterprise Linux release 9" /etc/redhat-release; then
            COMPLETION_PATH="/usr/share/doc/git/contrib/completion"
            COMPLETION_SCRIPT="$COMPLETION_PATH/git-completion.bash"
            PROMPT_SCRIPT="$COMPLETION_PATH/git-prompt.sh"
        elif grep -q "Fedora release" /etc/redhat-release; then
            COMPLETION_SCRIPT="/usr/share/bash-completion/completions/git"
            PROMPT_SCRIPT="/usr/share/git-core/contrib/completion/git-prompt.sh"
        else
            COMPLETION_PATH="/usr/share/doc/git/contrib/completion"
            COMPLETION_SCRIPT="$COMPLETION_PATH/git-completion.bash"
            PROMPT_SCRIPT="$COMPLETION_PATH/git-prompt.sh"
        fi
    else
        COMPLETION_PATH="/usr/share/doc/git/contrib/completion"
        COMPLETION_SCRIPT="$COMPLETION_PATH/git-completion.bash"
        PROMPT_SCRIPT="$COMPLETION_PATH/git-prompt.sh"
    fi
}

set_git_prompt() {
    local prompt_script="$1"
    if test -f "$prompt_script"
    then
        . "$prompt_script"
        PS1="$PS1"'\[\033[36m\]'  # change color to cyan
        PS1="$PS1"'`__git_ps1`'   # bash function
    fi
}

set_git_completion() {
    local completion_script="$1"
    if test -f "$completion_script"
    then
        . "$completion_script"
    fi
}

if test -f ~/.config/git/git-prompt.sh
then
        . ~/.config/git/git-prompt.sh
else
        PS1='\[\033]0;$TITLEPREFIX:$PWD\007\]' # set window title
        PS1="$PS1"'\n'                 # new line
        PS1="$PS1"'\[\033[32m\]'       # change to green
        PS1="$PS1"'\u@\h '             # user@host<space>
        PS1="$PS1"'\[\033[35m\]'       # change to purple
        PS1="$PS1"'$MSYSTEM '          # show MSYSTEM
        PS1="$PS1"'\[\033[33m\]'       # change to brownish yellow
        PS1="$PS1"'\w'                 # current working directory


        get_git_paths
        set_git_prompt "$PROMPT_SCRIPT"
        set_git_completion "$COMPLETION_SCRIPT"

        PS1="$PS1"'\[\033[0m\]'        # change color
        PS1="$PS1"'\n'                 # new line
        PS1="$PS1"'$ '                 # prompt: always $
fi
