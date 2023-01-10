import streamlit as st
import cv2
import numpy as np
from keras.models import load_model
from streamlit_webrtc import webrtc_streamer

webrtc_streamer(key="example")

st.title('Is it Pikachu or Eevee!?')
st.header('The image detection tool you definitely do not need in your life')

model = load_model('keras_model.h5', compile = False)
img_file_buffer = st.camera_input("Take a picture")


if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    image = cv2.resize(cv2_img, (224, 224), interpolation=cv2.INTER_AREA)
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    image = (image / 127.5) - 1
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
