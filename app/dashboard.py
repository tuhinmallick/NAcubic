import streamlit as st
import cv2
import skvideo.io

from PIL import Image

uploaded_video = st.sidebar.file_uploader("Choose video", type=["mp4", "avi"])
 
frame_skip = 300 # display every 300 frames
window_size =  st.sidebar.number_input("Window Size", value = 12)
roi =  st.sidebar.checkbox("ROI analysis")
process_image_stack = st.empty()
process_image_stack = st.sidebar.button("Process Image Stack")
signal_to_noise_ratio =  st.sidebar.number_input("Signal to Noise Ratio", value = 3)
signal_average_threshold =  st.sidebar.number_input("Signal Average Threshold", value = 15)
general_activity_tracker =  st.sidebar.checkbox("General Activity Tracker")
include_variance =  st.sidebar.checkbox("Include Variance")
if include_variance:
    variance =  st.sidebar.number_input("Variance value", value = 1)
minimum_activity_counts =  st.sidebar.number_input("Minimum activity counts", value = 1)
col1, col2 = st.sidebar.columns(2)
with col1:
    detect_activity = st.sidebar.button("Detect Activty")
with col2:
    reset = st.sidebar.button("Reset")

if uploaded_video is not None: # run only when user uploads video
    vid = uploaded_video.name
    outputfile = "/tmp/video.mp4"
    writer = skvideo.io.FFmpegWriter(outputfile, outputdict={'-vcodec': 'libx264'})
    with open(vid, mode='wb') as f:
        f.write(uploaded_video.read()) # save video to disk
    st.markdown(f"""
    ### Files
    - {vid}
    """,
    unsafe_allow_html=True) # display file name
    vidcap = cv2.VideoCapture(vid) # load video from disk
    cur_frame = 0
    success = True
    while success:
        success, frame = vidcap.read() # get next frame from video
        if cur_frame % frame_skip == 0: # only analyze every n=300 frames
            print('frame: {}'.format(cur_frame)) 
            pil_img = Image.fromarray(frame) # convert opencv frame (with type()==numpy) into PIL Image
            writer.writeFrame(pil_img)
            #st.image(pil_img)
        cur_frame += 1
    writer.close()
    st.video(outputfile)
stack_images = {}
if process_image_stack is not None and uploaded_video is not None: # run only when user uploads video
    vid = uploaded_video.name
    vidcap = cv2.VideoCapture(vid) # load video from disk
    cur_frame = 0
    success = True
    while success:
        success, frame = vidcap.read() # get next frame from video
        if cur_frame % frame_skip == 0: # only analyze every n=300 frames
            print('frame: {}'.format(cur_frame)) 
            pil_img = Image.fromarray(frame) # convert opencv frame (with type()==numpy) into PIL Image
            stack_images[f'Frame {cur_frame+1}'] = pil_img
            #st.image(pil_img)
        cur_frame += 1
    writer.close()
    for name, frame_ in stack_images.items():
        st.write(name)
        st.image(frame_)