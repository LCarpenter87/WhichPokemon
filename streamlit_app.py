import streamlit as st
import threading
import cv2
import numpy as np
from keras.models import load_model
from streamlit_webrtc import webrtc_streamer, RTCConfiguration, WebRtcMode
import av
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

model = load_model('keras_model.h5', compile = False)
lock = threading.Lock() 
img_container = {'img':None}

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    with lock:
        img_container['img'] = img
    return frame


st.title('Is it Pikachu or Eevee!?')
st.header('The image detection tool you definitely do not need in your life')

ctx = webrtc_streamer(key="example", 
                video_frame_callback=video_frame_callback,
                rtc_configuration = RTC_CONFIGURATION,
                mode=WebRtcMode.SENDRECV)


while ctx.state.playing:
    with lock: 
        img = img_container['img']
    if img is None:
        continue
    img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
    img = np.asarray(img, dtype=np.float32).reshape(1, 224, 224, 3)
    img = (img / 127.5) - 1
    probabilities = model.predict(image)

    if probabilities[0,0] > 0.8:
        prob = round(probabilities[0,0] * 100,2)
        st.write(f"I'm {prob}% sure that's Pikachu!")
        st.balloons()
    elif probabilities[0,1] > 0.8:
        prob = round(probabilities[0,1] * 100,2)
        st.write(f"I'm {prob}% pretty sure that's Eevee!")
        st.balloons()
    else:
        st.write("I have no idea what this is")
