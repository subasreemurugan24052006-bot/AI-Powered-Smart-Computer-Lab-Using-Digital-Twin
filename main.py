# Install required packages
!pip install -q ultralytics opencv-python-headless matplotlib pandas numpy plotly gradio
import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from ultralytics import YOLO
from google.colab import files
from IPython.display import display, Image
import ultralytics

print("Ultralytics version:", ultralytics.__version__)
print("Installation successful!")
# Load YOLO11 model

model = YOLO("yolo11s.pt")

print("YOLO11 model loaded successfully!")
# Display YOLO class names

class_names = model.names

print("Number of classes:", len(class_names))

for class_id, class_name in class_names.items():
    print(class_id, "->", class_name)
print("Upload an image or video of your computer lab.")

uploaded = files.upload()

input_file = list(uploaded.keys())[0]

print("Uploaded file:", input_file)
image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]
video_extensions = [".mp4", ".avi", ".mov", ".mkv"]

file_extension = os.path.splitext(input_file)[1].lower()

if file_extension in image_extensions:
    input_type = "image"

elif file_extension in video_extensions:
    input_type = "video"

else:
    raise ValueError("Unsupported file format")

print("Input type:", input_type)
# Objects important for our computer lab

LAB_OBJECTS = [
    "person",
    "laptop",
    "chair",
    "backpack",
    "tv",
    "cell phone",
    "keyboard",
    "mouse"
]

print("Objects monitored by the system:")

for obj in LAB_OBJECTS:
    print("-", obj)
def detect_image(image_path, confidence=0.40):

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Unable to read image")

    # Run YOLO detection
    results = model.predict(
        source=image,
        conf=confidence,
        verbose=False
    )

    result = results[0]

    # Annotated image
    annotated_image = result.plot()

    # Convert BGR to RGB
    annotated_image = cv2.cvtColor(
        annotated_image,
        cv2.COLOR_BGR2RGB
    )

    return result, annotated_image
    if input_type == "image":

    result, annotated_image = detect_image(
        input_file,
        confidence=0.40
    )

    plt.figure(figsize=(14, 8))

    plt.imshow(annotated_image)
    plt.axis("off")
    plt.title("AI Computer Lab Object Detection")

    plt.show()
    if input_type == "image":

    detected_objects = []

    boxes = result.boxes

    for box in boxes:

        class_id = int(box.cls[0])
        confidence = float(box.conf[0])

        class_name = model.names[class_id]

        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

        detected_objects.append({
            "Object": class_name,
            "Confidence": round(confidence, 3),
            "X1": int(x1),
            "Y1": int(y1),
            "X2": int(x2),
            "Y2": int(y2)
        })

    detection_df = pd.DataFrame(detected_objects)

    display(detection_df)
    if input_type == "image":

    if len(detection_df) > 0:

        object_counts = (
            detection_df["Object"]
            .value_counts()
            .reset_index()
        )

        object_counts.columns = [
            "Object",
            "Count"
        ]

        display(object_counts)

    else:

        print("No objects detected.")
    TOTAL_SEATS = 30

if input_type == "image":

    people_count = 0

    if len(detection_df) > 0:

        people_count = (
            detection_df["Object"] == "person"
        ).sum()

    occupancy_percentage = (
        people_count / TOTAL_SEATS
    ) * 100

    occupancy_percentage = min(
        occupancy_percentage,
        100
    )

    print("People detected:", people_count)
    print("Total lab seats:", TOTAL_SEATS)
    print(
        f"Lab occupancy: {occupancy_percentage:.2f}%"
    )
    def get_occupancy_status(percentage):

    if percentage == 0:
        return "EMPTY"

    elif percentage < 40:
        return "LOW OCCUPANCY"

    elif percentage < 80:
        return "MODERATE OCCUPANCY"

    else:
        return "HIGH OCCUPANCY"


    if input_type == "image":

    occupancy_status = get_occupancy_status(
        occupancy_percentage
    )

    print("Occupancy Status:", occupancy_status)
    # Computer lab digital twin layout

    lab_objects = {
    "Door": (1, 8),
    "Teacher Desk": (8, 8),
    "Projector": (8, 9),
    "Computer 1": (3, 6),
    "Computer 2": (5, 6),
    "Computer 3": (7, 6),
    "Computer 4": (9, 6),
    "Computer 5": (11, 6),
    "Computer 6": (3, 3),
    "Computer 7": (5, 3),
    "Computer 8": (7, 3),
    "Computer 9": (9, 3),
    "Computer 10": (11, 3)
    }
    def create_digital_twin(
    people_count,
    total_seats
):

    occupancy = (
        people_count / total_seats
    ) * 100

    occupancy = min(occupancy, 100)

    fig = go.Figure()

    # Lab boundary
    fig.add_shape(
        type="rect",
        x0=0,
        y0=0,
        x1=14,
        y1=10,
        line=dict(width=3)
    )

    # Add computer desks
    for name, (x, y) in lab_objects.items():

        if "Computer" in name:

            fig.add_shape(
                type="rect",
                x0=x - 0.7,
                y0=y - 0.5,
                x1=x + 0.7,
                y1=y + 0.5,
                line=dict(width=2)
            )

            fig.add_annotation(
                x=x,
                y=y,
                text=name.replace("Computer ", "PC "),
                showarrow=False,
                font=dict(size=9)
            )

    # Door
    fig.add_annotation(
        x=1,
        y=8,
        text="🚪 Door",
        showarrow=False
    )

    # Teacher desk
    fig.add_annotation(
        x=8,
        y=8,
        text="Teacher Desk",
        showarrow=False
    )

    # Occupancy information
    fig.add_annotation(
        x=7,
        y=10.5,
        text=(
            f"<b>AI SMART COMPUTER LAB</b><br>"
            f"People: {people_count}<br>"
            f"Occupancy: {occupancy:.1f}%"
        ),
        showarrow=False,
        font=dict(size=16)
    )

    fig.update_xaxes(
        range=[0, 14],
        visible=False
    )

    fig.update_yaxes(
        range=[0, 11],
        visible=False
    )

    fig.update_layout(
        width=1000,
        height=700,
        title="Digital Twin – Smart Computer Lab",
        showlegend=False
    )

    return fig
    if input_type == "image":

    digital_twin = create_digital_twin(
        people_count,
        TOTAL_SEATS
    )

    digital_twin.show()
    if input_type == "image" and len(detection_df) > 0:

    counts = (
        detection_df["Object"]
        .value_counts()
    )

    fig = go.Figure(
        data=[
            go.Bar(
                x=counts.index,
                y=counts.values
            )
        ]
    )

    fig.update_layout(
        title="Detected Objects in Computer Lab",
        xaxis_title="Object",
        yaxis_title="Number of Objects"
    )

    fig.show()
    if input_type == "image":

    print("=" * 50)
    print("AI SMART COMPUTER LAB DIGITAL TWIN")
    print("=" * 50)

    print(f"People detected     : {people_count}")
    print(f"Total seats         : {TOTAL_SEATS}")
    print(f"Occupancy           : {occupancy_percentage:.2f}%")
    print(f"Status              : {occupancy_status}")

    print("=" * 50)
    if input_type == "image":

    # Save annotated image

    output_image = "lab_detection_result.jpg"

    cv2.imwrite(
        output_image,
        cv2.cvtColor(
            annotated_image,
            cv2.COLOR_RGB2BGR
        )
    )

    # Save CSV
    detection_df.to_csv(
        "lab_detection_results.csv",
        index=False
    )

    print("Files created:")
    print("-", output_image)
    print("- lab_detection_results.csv")
    if input_type == "image":

    files.download("lab_detection_result.jpg")
    files.download("lab_detection_results.csv")
    print("Upload your computer lab CCTV/video.")

    video_upload = files.upload()

    video_file = list(video_upload.keys())[0]

    print("Video:", video_file)
    def process_lab_video(
    video_path,
    output_path="lab_detected_output.mp4",
    confidence=0.40
):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError("Unable to open video")

    width = int(
        cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    )

    height = int(
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    )

    fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    if fps <= 0:
        fps = 25

    fourcc = cv2.VideoWriter_fourcc(
        *"mp4v"
    )

    writer = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (width, height)
    )

    frame_number = 0

    occupancy_records = []

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_number += 1

        results = model.predict(
            source=frame,
            conf=confidence,
            verbose=False
        )

        result = results[0]

        annotated_frame = result.plot()

        person_count = 0

        for box in result.boxes:

            class_id = int(box.cls[0])

            class_name = model.names[class_id]

            if class_name == "person":
                person_count += 1

        occupancy = (
            person_count /
            TOTAL_SEATS
        ) * 100

        occupancy = min(
            occupancy,
            100
        )

        # Add information to video
        cv2.putText(
            annotated_frame,
            f"People: {person_count}",
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

        cv2.putText(
            annotated_frame,
            f"Occupancy: {occupancy:.1f}%",
            (30, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

        writer.write(
            annotated_frame
        )

        occupancy_records.append({
            "Frame": frame_number,
            "People": person_count,
            "Occupancy_Percentage": occupancy
        })

    cap.release()
    writer.release()

    occupancy_df = pd.DataFrame(
        occupancy_records
    )

    return occupancy_df
    video_results = process_lab_video(
    video_file,
    output_path="lab_detected_output.mp4",
    confidence=0.40
    )

    print("Video processing completed.")

    display(
    video_results.head()
    )
    print(
    "Total processed frames:",
    len(video_results)
)

    print(
    "Average people detected:",
    video_results["People"].mean()
    )

    print(
    "Average occupancy:",
    video_results[
        "Occupancy_Percentage"
    ].mean()
    )
    fig = go.Figure()

    fig.add_trace(
    go.Scatter(
        x=video_results["Frame"],
        y=video_results["Occupancy_Percentage"],
        mode="lines",
        name="Occupancy"
    )
    )

    fig.update_layout(
    title="Computer Lab Occupancy Over Time",
    xaxis_title="Video Frame",
    yaxis_title="Occupancy (%)"
    )

    fig.show()
    video_results.to_csv(
    "lab_occupancy_results.csv",
    index=False
    )

    print(
    "Saved: lab_occupancy_results.csv"
    )
    files.download(
    "lab_detected_output.mp4"
)
files.download(
    "lab_occupancy_results.csv"
)
average_people = video_results["People"].mean()

maximum_people = video_results["People"].max()

average_occupancy = (
    video_results[
        "Occupancy_Percentage"
    ].mean()
)

maximum_occupancy = (
    video_results[
        "Occupancy_Percentage"
    ].max()
)

print("=" * 60)
print("AI-POWERED SMART COMPUTER LAB DIGITAL TWIN")
print("=" * 60)

print(
    f"Average people detected : "
    f"{average_people:.2f}"
)

print(
    f"Maximum people detected : "
    f"{maximum_people}"
)

print(
    f"Average occupancy       : "
    f"{average_occupancy:.2f}%"
)

print(
    f"Maximum occupancy       : "
    f"{maximum_occupancy:.2f}%"
)

print("=" * 60)
final_people = int(round(average_people))

final_twin = create_digital_twin(
    final_people,
    TOTAL_SEATS
)

final_twin.show()
final_twin.write_html(
    "computer_lab_digital_twin.html"
)

print(
    "Digital twin saved as:"
)

print(
    "computer_lab_digital_twin.html"
)
final_twin.write_html(
    "computer_lab_digital_twin.html"
)

print(
    "Digital twin saved as:"
)

print(
    "computer_lab_digital_twin.html"
)
files.download(
    "computer_lab_digital_twin.html"
)

