#!/bin/sh

ASR_MODEL_PATH='service_asr/models'
ASR_MODEL_NAME='vosk-model-small-ru-0.22'

TS_MODEL_PATH='service_text_similarity/models'
TS_MODEL_NAME='ts_model'

if [ -d "$ASR_MODEL_PATH/$ASR_MODEL_NAME" ] 
then
    echo "ASR Model directory exists." 
else
    echo "ASR Model not exists. Start downloading."
    wget https://storage.yandexcloud.net/eva-models/vosk-model-small-ru-0.22.zip -O "$ASR_MODEL_PATH/tmp.zip"
    unzip "$ASR_MODEL_PATH/tmp.zip" -d $ASR_MODEL_PATH
    rm "$ASR_MODEL_PATH/tmp.zip"
fi

if [ -d "$TS_MODEL_PATH/$TS_MODEL_NAME" ] 
then
    echo "Text similarity model directory exists." 
else
    echo "Text similarity model not exists. Start downloading."
    wget https://storage.yandexcloud.net/eva-models/ts_model.zip -O "$TS_MODEL_PATH/tmp.zip"
    unzip "$TS_MODEL_PATH/tmp.zip" -d $TS_MODEL_PATH
    rm "$TS_MODEL_PATH/tmp.zip"
fi
