FROM is-face-detector/dev
WORKDIR /opt/is

RUN wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml  
COPY src/ src
COPY setup.py ./
COPY etc/conf/options.json ./

RUN pip install .

CMD ["is-face-detector"]