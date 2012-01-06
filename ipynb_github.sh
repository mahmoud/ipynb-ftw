#!/bin/bash

function log_and_die { logger $1; exit 1; }

DATE_STR="$(date '+%l:%m%P  %B %e, %Y')"

cd /home/ipy/notebooks
if [ "$(git status -s)" ] 
    then
      git add .
      git commit -a -m "autocommit $DATE_STR" || log_and_die "IPYNB: Failed to commit ($DATE_STR)"
      COMMIT_ID="$(git rev-parse HEAD)"
      git push origin master || log_and_die "IPYNB: Failed to push ($DATE_STR)"
      logger "IPYNB: Successfully committed/pushed '$COMMIT_ID' ($DATE_STR)."
    else
      logger "IPYNB: No tracked/trackable files updated. ($DATE_STR)"
fi
