FROM ubuntu
RUN apt update --fix-missing
RUN apt install -y python3 python3-pip
RUN pip3 install scikit-learn
RUN pip3 install pandas
RUN pip3 install numpy
RUN pip3 install opencv-python

CMD /bin/bash
