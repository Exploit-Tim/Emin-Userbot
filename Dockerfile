#==============×==============#
#      Created by: Alfa-Ex
#=========× AyiinXd ×=========#
# Izzy Ganteng

FROM ayiinxd/ayiin:xd

RUN git clone -b Emin-Userbot https://github.com/iniemin/Emin-Userbot /home/eminuserbot/ \
    && chmod 777 /home/eminuserbot \
    && mkdir /home/eminuserbot/bin/

#COPY ./sample.env ./.env* /home/ayiinuserbot/

WORKDIR /home/eminuserbot/

RUN pip install -r requirements.txt

CMD ["bash","start"]
