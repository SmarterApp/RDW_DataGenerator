#!/usr/bin/env bash
#
# Script to prepare the output files for submission. By pairs, it tars them, encrypts them and ftps them
# NOTE: this script isn't very robust, use with care and insight.
#
# The gpg environment must be set up to allow encrypt/sign by a known user for the proper recipient.
# Make sure that is so and modify the gpg command as necessary. For example, if there is a single private
# key configured in the config/gpg folder and the recipient is the usual production value:
#   gpg --homedir ../../config/gpg --no-permission-warning -q -e -r sbac_data_provider@sbac.com -o "$gpgfile" "$tarfile"
# If your system has multiple private keys in the usual gpg location and this is for PoC:
#   gpg --batch --no-tty --yes -q --passphrase ca_user -u ca_user -r sbacdw -es -o "$gpgfile" "$tarfile"
#
# The ftp expect script must be set up for the environment.

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

pushd "$SCRIPT_DIR/../out"

for csv in ASMT*.csv; do
    base="${csv%.*}"
    tarfile="$base.tar.gz"
    gpgfile="$tarfile.gpg"
    if [ ! -f "$gpgfile" ]; then
        if [ ! -f "$base.json" ]; then
            echo "skipping unpaired file $csv"
            continue
        else
            tar czf "$tarfile" "$base.csv" "$base.json"
            gpg --batch --no-tty --yes -q --passphrase ca_user -u ca_user -r sbacdw -es -o "$gpgfile" "$tarfile"
            rm "$tarfile"
        fi
    fi
    echo "submitting $gpgfile"
    "$SCRIPT_DIR/ftp.exp" "$gpgfile"
#    sleep 2
done

popd
