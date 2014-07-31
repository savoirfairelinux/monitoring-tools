#! /bin/sh

STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2
STATE_UNKNOWN=3
STATE_DEPENDENT=4

print_revision() {
    echo ""
	echo "$1 v$2 (sfl-shinken-plugins)"
    echo ""
	echo "The SFL Shinken Plugins come with ABSOLUTELY NO WARRANTY. You may redistribute"
    echo "copies of the plugins under the terms of the GNU General Public License."
    echo "For more information about these matters, see the file named COPYING."
}

support() {
	echo "Send email to thibault.cohen@savoirfairelinux.com if you have questions"
    echo "regarding use of this software."
    echo "To submit patches or suggest improvements, "
    echo "send email to thibault.cohen@savoirfairelinux.com"
    echo "Please include version information with all correspondence (when "
    echo "possible, use output from the --version option of the plugin itself)."
}

