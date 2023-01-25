import streamlit as st
import cv2
import skvideo.io
import pickle, os

from PIL import Image
process_image_stack= st.empty()



def upload():
    dashboards = ("Neuron_TTX-CNQX.avi", "spiking_neuron.avi")
    load_options = dict()
    load_options["toy_dataset"] = st.sidebar.checkbox(
        "Load a uploaded dataset",
        True,
        help="Select this option if you want to work with uploaded Dataset",
    )
    if load_options["toy_dataset"]:
        dataset_name = st.selectbox(
            "Select a uploaded dataset",
            options=dashboards,
            help="Select the dataset you want to work with",
        )
        outputfile = open(os.path.join("assets/videos/", dataset_name),"wb")
        st.write("{} has been uploaded".format(dataset_name))
    else:
        try:
            uploaded_videos = st.sidebar.file_uploader("Please upload a video", type=["mp4", "avi"])
            st.write("{} has been uploaded".format(uploaded_video.name))
        except Exception as err:
            st.write("{} is not the proper file format".format(uploaded_video.name))
    return outputfile 


#######################################################################################################
# Sidebar
######################################################################################################
st.sidebar.image("assets/images/Logo.png", use_column_width='auto')
uploaded_video = upload()
window_size =  st.sidebar.number_input("Window Size", value = 12)
col1, col2, col3 = st.sidebar.columns([1,3,1])
process_image_stack = st.empty()
with col2:
    roi =  st.checkbox("ROI analysis")
    process_image_stack = st.button("Process Image Stack")
signal_to_noise_ratio =  st.sidebar.number_input("Signal to Noise Ratio", value = 3)
signal_average_threshold =  st.sidebar.number_input("Signal Average Threshold", value = 15)
col1, col2, col3 = st.sidebar.columns([0.5,3,0.5])
with col2:
    general_activity_tracker =  st.checkbox("General Activity Tracker")
    include_variance =  st.checkbox("Include Variance")
    if include_variance:
        variance =  st.sidebar.number_input("Variance value", value = 1)
minimum_activity_counts =  st.sidebar.number_input("Minimum activity counts", value = 1)
col1, col2 = st.sidebar.columns([1,0.5])
with col1:
    detect_activity = st.button("Detect Activty")
with col2:
    reset = st.button("Reset")
######################################################################################################
    
# Upload Video
stack_images, stack_frames = {}, {}

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
        print('frame: {}'.format(cur_frame))
        if  success:
            pil_img = Image.fromarray(frame) # convert opencv frame (with type()==numpy) into PIL Image
            writer.writeFrame(pil_img)
            stack_images[f'Frame {cur_frame+1}'] = pil_img
            stack_frames[f'Frame {cur_frame+1}'] = frame
            cur_frame += 1
    writer.close()
    st.video(outputfile)
    
if process_image_stack:
    with open('data.pkl', 'wb') as files:
        pickle.dump(stack_frames, files)
    for name, frame_ in stack_images.items():
        st.write(name)
        st.image(frame_)
