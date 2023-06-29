import streamlit as st
from PIL import Image
import cv2 as cv
import tempfile

st.write("""
# 从视频合成长曝光照片
没有单反, 没有灰度滤光镜, 使用手机也能拍出 ___星轨___ 和 ___瀑布___ 摄影作品, 来看看效果吧
""")

st.write("""
## 星轨
""")

col1, col2 = st.columns(2)

video_file = open('samples/star-trails.mp4', 'rb')
video_bytes = video_file.read()

with col1:
    st.video(video_bytes, format="video/mp4", start_time=0)

image = Image.open('samples/star-trails.png')
with col2:
    st.image(image)

st.write("""
## 瀑布
""")

col3, col4 = st.columns(2)

video_file3 = open('samples/waterfall.mp4', 'rb')
video_bytes3 = video_file3.read()

with col3:
    st.video(video_bytes3, format="video/mp4", start_time=0)

image3 = Image.open('samples/waterfall.png')
with col4:
    st.image(image3)

st.write("""
## 开始创作你的作品
""")

@staticmethod
def averager():
    """Calculate the average using a clojure."""
    count = 0
    total = 0.0

    def average(value):
        nonlocal count, total
        count += 1
        total += value
        return total / count

    return average

@staticmethod
def maxer():
    """Calculate the max using a clojure."""
    maxium = 0.0

    def maxer(value):
        nonlocal maxium
        maxium = cv.max(maxium, value)
        return maxium

    return maxer

optioncol1, optioncol2 = st.columns(2)

with optioncol1:
    uploaded_file = st.file_uploader("上传固定机位拍摄的视频文件", type=['mp4'])

with optioncol2:
    mode = st.radio(
    "选择生成效果",
    ('星轨', '瀑布'), horizontal=True)

if uploaded_file is not None:
    data = uploaded_file.getvalue()
    st.video(data, format="video/mp4", start_time=0)

    # 上传视频放入OpenCV进行处理
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    videoCap = cv.VideoCapture(tfile.name)

    if videoCap.isOpened() == True:

        # 分辨率
        width = int(videoCap.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(videoCap.get(cv.CAP_PROP_FRAME_HEIGHT))
        # 帧率
        fps = videoCap.get(cv.CAP_PROP_FPS)
        # 总帧数
        frames = videoCap.get(cv.CAP_PROP_FRAME_COUNT)
        # 编码格式
        fourcc = int(videoCap.get(cv.CAP_PROP_FOURCC))

        framesRange = st.slider(
            '选择视频范围',
            0, int(frames), (0, 256), step = 1)

        start, end = framesRange

        if (end - start) > 256:
            end = start + 255

        r, g, b = None, None, None
        if mode == "星轨":
            r_avg, g_avg, b_avg = maxer(), maxer(), maxer()
        else:
            r_avg, g_avg, b_avg = averager(), averager(), averager()

        mergedResult = None
        ret, frame = videoCap.read()

        count = 1
        while ret: 

            # 控制处理帧范围
            if start > count:
                ret, frame = videoCap.read()
                count += 1
                continue

            if end < count:
                break

            # Get the current RGB
            b_curr, g_curr, r_curr = cv.split(frame.astype("float"))
            r, g, b = r_avg(r_curr), g_avg(g_curr), b_avg(b_curr)

            ret, frame = videoCap.read()
            count += 1

        print("处理结束")
        videoCap.release()
        mergedResult = cv.merge([b, g, r]).astype("uint8")

        toImage = Image.fromarray(cv.cvtColor(mergedResult, cv.COLOR_BGR2RGB))
        st.image(toImage)
else:
    st.video(video_bytes, format="video/mp4", start_time=0)

    st.image(image)