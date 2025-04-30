FROM  gradescope/auto-builds:ubuntu-22.04
RUN mkdir -p /autograder/source
COPY autograder.zip /tmp/autograder.zip
RUN unzip -n -d /autograder/source /tmp/autograder.zip
RUN cp /autograder/source/run_autograder /autograder/run_autograder
RUN dos2unix /autograder/run_autograder /autograder/source/setup.sh
RUN chmod +x /autograder/run_autograder
RUN bash /gradescope/setup.sh
