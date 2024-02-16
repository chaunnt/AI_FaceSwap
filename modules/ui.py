import os
import webbrowser
import customtkinter as ctk
from typing import Callable, Tuple
import cv2
from PIL import Image, ImageOps
import time
import tkinter
import modules.globals
import modules.metadata
from modules.face_analyser import get_one_face
from modules.capturer import get_video_frame, get_video_frame_total
from modules.processors.frame.core import get_frame_processors_modules
from modules.utilities import is_image, is_video, resolve_relative_path

LICENSE = "20240128"
ROOT = None
ROOT_HEIGHT = 700
ROOT_WIDTH = 600

PREVIEW = None
PREVIEW_MAX_HEIGHT = 700
PREVIEW_MAX_WIDTH = 1200

RECENT_DIRECTORY_SOURCE = "."
RECENT_DIRECTORY_TARGET = "."
RECENT_DIRECTORY_OUTPUT = "."

preview_label = None
preview_slider = None
source_label = None
target_label = None
status_label = None

img_ft, vid_ft = modules.globals.file_types


def init(start: Callable[[], None], destroy: Callable[[], None]) -> ctk.CTk:
    global ROOT, PREVIEW
    # While loop for login
    create_auth(start, destroy)
    # While loop for main window
    ROOT = create_root(start, destroy)
    PREVIEW = create_preview(ROOT)

    return ROOT


def create_auth(start: Callable[[], None], destroy: Callable[[], None]) -> ctk.CTk:
    global ROOT, PREVIEW

    def login_event():
        global ROOT, PREVIEW
        if entry_1.get() == LICENSE:  # This is just a simple demo verification,
            update_license_status(
                status_label=status_label, status_text="License đã đúng!"
            )
            root_login.destroy()  # Destroy the login window after the verification
        else:  # If password doesn't match
            entry_1.configure(text_color="red")
            update_license_status(
                status_label=status_label,
                status_text="Xin lỗi, License của bạn không đúng!",
            )

    def update_license_status(status_label, status_text):
        status_label.configure(text=status_text)
        root_login.update()

    # Define the login page window
    ctk.deactivate_automatic_dpi_awareness()
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme(resolve_relative_path("ui.json"))

    root_login = ctk.CTk()
    root_login.minsize(ROOT_WIDTH, ROOT_HEIGHT)
    root_login.title("LOGIN PAGE")
    root_login.configure()
    root_login.protocol("WM_DELETE_WINDOW", lambda: destroy())

    # Add some widgets for login page
    frame = ctk.CTkFrame(master=root_login, width=450, height=450, corner_radius=10)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    label_1 = ctk.CTkLabel(
        master=frame,
        width=400,
        height=60,
        corner_radius=10,
        fg_color=("gray70", "gray35"),
        text="Vui lòng nhập license để tiếp tục",
    )
    label_1.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

    entry_1 = ctk.CTkEntry(
        master=frame, corner_radius=20, width=400, placeholder_text="License"
    )
    entry_1.place(relx=0.5, rely=0.52, anchor=tkinter.CENTER)

    status_label = ctk.CTkLabel(root_login, text=None, justify="center")
    status_label.place(relx=0.1, rely=0.9, relwidth=0.8)

    button_login = ctk.CTkButton(
        master=frame, text="ĐĂNG NHẬP", corner_radius=6, command=login_event, width=400
    )
    button_login.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

    root_login.mainloop()
    # return root_login


def create_root(start: Callable[[], None], destroy: Callable[[], None]) -> ctk.CTk:
    global source_label, target_label, status_label

    ctk.deactivate_automatic_dpi_awareness()
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme(resolve_relative_path("ui.json"))

    root = ctk.CTk()
    root.minsize(ROOT_WIDTH, ROOT_HEIGHT)
    # root.title(f'{modules.metadata.name} {modules.metadata.version} {modules.metadata.edition}')
    root.title("Deep Face Swapping Demo")
    root.configure()
    root.protocol("WM_DELETE_WINDOW", lambda: destroy())

    source_label = ctk.CTkLabel(root, text=None)
    source_label.place(relx=0.1, rely=0.1, relwidth=0.3, relheight=0.25)

    target_label = ctk.CTkLabel(root, text=None)
    target_label.place(relx=0.6, rely=0.1, relwidth=0.3, relheight=0.25)

    source_button = ctk.CTkButton(
        root,
        text="Chọn khuôn mặt gốc",
        cursor="hand2",
        command=lambda: select_source_path(),
    )
    source_button.place(relx=0.05, rely=0.45, relwidth=0.35, relheight=0.05)

    target_button = ctk.CTkButton(
        root, text="Chọn ảnh", cursor="hand2", command=lambda: select_target_path()
    )
    target_button.place(relx=0.6, rely=0.45, relwidth=0.3, relheight=0.05)

    target_button_1 = ctk.CTkButton(
        root,
        text="Chọn video",
        cursor="hand2",
        command=lambda: select_target_video_path(),
    )
    target_button_1.place(relx=0.6, rely=0.51, relwidth=0.3, relheight=0.05)

    # keep_fps_value = ctk.BooleanVar(value=modules.globals.keep_fps)
    # keep_fps_checkbox = ctk.CTkSwitch(root, text='Keep fps', variable=keep_fps_value, cursor='hand2', command=lambda: setattr(modules.globals, 'keep_fps', not modules.globals.keep_fps))
    # keep_fps_checkbox.place(relx=0.1, rely=0.6)

    # keep_frames_value = ctk.BooleanVar(value=modules.globals.keep_frames)
    # keep_frames_switch = ctk.CTkSwitch(root, text='Keep frames', variable=keep_frames_value, cursor='hand2', command=lambda: setattr(modules.globals, 'keep_frames', keep_frames_value.get()))
    # keep_frames_switch.place(relx=0.1, rely=0.65)

    # for FRAME PROCESSOR ENHANCER tumbler:
    enhancer_value = ctk.BooleanVar(value=modules.globals.fp_ui["face_enhancer"])
    enhancer_switch = ctk.CTkSwitch(
        root,
        text="Tăng chất lượng ảnh",
        variable=enhancer_value,
        cursor="hand2",
        command=lambda: update_tumbler("face_enhancer", enhancer_value.get()),
    )
    enhancer_switch.place(relx=0.1, rely=0.6)

    # keep_audio_value = ctk.BooleanVar(value=modules.globals.keep_audio)
    # keep_audio_switch = ctk.CTkSwitch(root, text='Keep audio', variable=keep_audio_value, cursor='hand2', command=lambda: setattr(modules.globals, 'keep_audio', keep_audio_value.get()))
    # keep_audio_switch.place(relx=0.6, rely=0.6)

    # many_faces_value = ctk.BooleanVar(value=modules.globals.many_faces)
    # many_faces_switch = ctk.CTkSwitch(root, text='Many faces', variable=many_faces_value, cursor='hand2', command=lambda: setattr(modules.globals, 'many_faces', many_faces_value.get()))
    # many_faces_switch.place(relx=0.6, rely=0.6)

    # nsfw_value = ctk.BooleanVar(value=modules.globals.nsfw)
    # nsfw_switch = ctk.CTkSwitch(root, text='NSFW', variable=nsfw_value, cursor='hand2', command=lambda: setattr(modules.globals, 'nsfw', nsfw_value.get()))
    # nsfw_switch.place(relx=0.6, rely=0.7)

    start_button = ctk.CTkButton(
        root,
        text="Chuyển đổi",
        cursor="hand2",
        command=lambda: select_output_path(start),
    )
    start_button.place(relx=0.1, rely=0.80, relwidth=0.25, relheight=0.05)

    preview_button = ctk.CTkButton(
        root, text="Livestream", cursor="hand2", command=lambda: toggle_preview()
    )
    preview_button.place(relx=0.4, rely=0.80, relwidth=0.25, relheight=0.05)

    stop_button = ctk.CTkButton(
        root, text="Thoát", cursor="hand2", command=lambda: destroy()
    )
    stop_button.place(relx=0.7, rely=0.80, relwidth=0.25, relheight=0.05)

    # live_button = ctk.CTkButton(root, text='Live', cursor='hand2', command=lambda: webcam_preview())
    # live_button.place(relx=0.40, rely=0.86, relwidth=0.25, relheight=0.05)

    status_label = ctk.CTkLabel(root, text=None, justify="center")
    status_label.place(relx=0.1, rely=0.9, relwidth=0.8)

    # donate_label = ctk.CTkLabel(root, text='Deep Live Cam', justify='center', cursor='hand2')
    # donate_label.place(relx=0.1, rely=0.95, relwidth=0.8)
    # donate_label.configure(text_color=ctk.ThemeManager.theme.get('URL').get('text_color'))
    # donate_label.bind('<Button>', lambda event: webbrowser.open('https://paypal.me/hacksider'))

    return root


def create_preview(parent: ctk.CTkToplevel) -> ctk.CTkToplevel:
    global preview_label, preview_slider

    preview = ctk.CTkToplevel(parent)
    preview.withdraw()
    preview.title("Preview")
    preview.configure()
    preview.protocol("WM_DELETE_WINDOW", lambda: toggle_preview())
    preview.resizable(width=False, height=False)

    preview_label = ctk.CTkLabel(preview, text=None)
    preview_label.pack(fill="both", expand=True)

    preview_slider = ctk.CTkSlider(
        preview, from_=0, to=0, command=lambda frame_value: update_preview(frame_value)
    )

    return preview


def update_status(text: str) -> None:
    status_label.configure(text=text)
    ROOT.update()


def update_tumbler(var: str, value: bool) -> None:
    modules.globals.fp_ui[var] = value


def select_source_path() -> None:
    global RECENT_DIRECTORY_SOURCE, img_ft, vid_ft
    print(RECENT_DIRECTORY_SOURCE)
    PREVIEW.withdraw()
    source_path = ctk.filedialog.askopenfilename(
        title="select an source image",
        initialdir=RECENT_DIRECTORY_SOURCE,
        filetypes=[img_ft],
    )
    if is_image(source_path):
        modules.globals.source_path = source_path
        RECENT_DIRECTORY_SOURCE = os.path.dirname(modules.globals.source_path)
        image = render_image_preview(modules.globals.source_path, (200, 200))
        source_label.configure(image=image)
    else:
        modules.globals.source_path = None
        source_label.configure(image=None)


def select_target_path() -> None:
    global RECENT_DIRECTORY_TARGET, img_ft, vid_ft

    PREVIEW.withdraw()
    target_path = ctk.filedialog.askopenfilename(
        title="select an target image or video",
        initialdir=RECENT_DIRECTORY_TARGET,
        filetypes=[img_ft],
    )
    if is_image(target_path):
        modules.globals.target_path = target_path
        RECENT_DIRECTORY_TARGET = os.path.dirname(modules.globals.target_path)
        image = render_image_preview(modules.globals.target_path, (200, 200))
        target_label.configure(image=image)
    elif is_video(target_path):
        modules.globals.target_path = target_path
        RECENT_DIRECTORY_TARGET = os.path.dirname(modules.globals.target_path)
        video_frame = render_video_preview(target_path, (200, 200))
        target_label.configure(image=video_frame)
    else:
        modules.globals.target_path = None
        target_label.configure(image=None)


def select_target_video_path() -> None:
    global RECENT_DIRECTORY_TARGET, img_ft, vid_ft

    PREVIEW.withdraw()
    target_path = ctk.filedialog.askopenfilename(
        title="select an target image or video",
        initialdir=RECENT_DIRECTORY_TARGET,
        filetypes=[vid_ft],
    )
    if is_image(target_path):
        modules.globals.target_path = target_path
        RECENT_DIRECTORY_TARGET = os.path.dirname(modules.globals.target_path)
        image = render_image_preview(modules.globals.target_path, (200, 200))
        target_label.configure(image=image)
    elif is_video(target_path):
        modules.globals.target_path = target_path
        RECENT_DIRECTORY_TARGET = os.path.dirname(modules.globals.target_path)
        video_frame = render_video_preview(target_path, (200, 200))
        target_label.configure(image=video_frame)
    else:
        modules.globals.target_path = None
        target_label.configure(image=None)


def select_output_path(start: Callable[[], None]) -> None:
    global RECENT_DIRECTORY_OUTPUT, img_ft, vid_ft

    if is_image(modules.globals.target_path):
        output_path = ctk.filedialog.asksaveasfilename(
            title="save image output file",
            filetypes=[img_ft],
            defaultextension=".png",
            initialfile="output.png",
            initialdir=RECENT_DIRECTORY_OUTPUT,
        )
    elif is_video(modules.globals.target_path):
        output_path = ctk.filedialog.asksaveasfilename(
            title="save video output file",
            filetypes=[vid_ft],
            defaultextension=".mp4",
            initialfile="output.mp4",
            initialdir=RECENT_DIRECTORY_OUTPUT,
        )
    else:
        output_path = None
        update_status("Hãy chọn ảnh gốc và ảnh mục tiêu để tiếp tục")
    if output_path:
        modules.globals.output_path = output_path
        RECENT_DIRECTORY_OUTPUT = os.path.dirname(modules.globals.output_path)
        start()


def render_image_preview(image_path: str, size: Tuple[int, int]) -> ctk.CTkImage:
    image = Image.open(image_path)
    if size:
        image = ImageOps.fit(image, size, Image.LANCZOS)
    return ctk.CTkImage(image, size=image.size)


def render_video_preview(
    video_path: str, size: Tuple[int, int], frame_number: int = 0
) -> ctk.CTkImage:
    capture = cv2.VideoCapture(video_path)
    if frame_number:
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    has_frame, frame = capture.read()
    if has_frame:
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if size:
            image = ImageOps.fit(image, size, Image.LANCZOS)
        return ctk.CTkImage(image, size=image.size)
    capture.release()
    cv2.destroyAllWindows()


def toggle_preview() -> None:
    global BREAK_STREAM
    if PREVIEW.state() == "normal":
        BREAK_STREAM = True
        PREVIEW.withdraw()
    elif modules.globals.source_path and modules.globals.target_path:
        if is_image(modules.globals.target_path):
            # update_status("Processing the image ...")
            update_status("Đang xử lý hình ảnh ...")
            init_preview()
            update_preview()
            PREVIEW.deiconify()
        if is_video(modules.globals.target_path):
            # update_status("Processing the video ...")
            update_status("Đang xử lý video ...")
            video_preview()
    else:
        update_status("Hãy chọn ảnh gốc và ảnh mục tiêu để tiếp tục")


def init_preview() -> None:
    if is_image(modules.globals.target_path):
        preview_slider.pack_forget()
    if is_video(modules.globals.target_path):
        video_frame_total = get_video_frame_total(modules.globals.target_path)
        preview_slider.configure(to=video_frame_total)
        preview_slider.pack(fill="x")
        preview_slider.set(0)


def update_preview(frame_number: int = 0) -> None:
    if modules.globals.source_path and modules.globals.target_path:
        temp_frame = get_video_frame(modules.globals.target_path, frame_number)
        if modules.globals.nsfw == False:
            from modules.predicter import predict_frame

            if predict_frame(temp_frame):
                quit()
        for frame_processor in get_frame_processors_modules(
            modules.globals.frame_processors
        ):
            temp_frame = frame_processor.process_frame(
                get_one_face(cv2.imread(modules.globals.source_path)), temp_frame
            )
        image = Image.fromarray(cv2.cvtColor(temp_frame, cv2.COLOR_BGR2RGB))
        image = ImageOps.contain(
            image, (PREVIEW_MAX_WIDTH, PREVIEW_MAX_HEIGHT), Image.LANCZOS
        )
        image = ctk.CTkImage(image, size=image.size)
        preview_label.configure(image=image)
        update_status("Xử lý hình ảnh thành công!")


def webcam_preview():
    # Current not support
    update_status("Sorry, currently we do not support webcam")
    return
    if modules.globals.source_path is None:
        # No image selected
        return

    global preview_label, PREVIEW

    cap = cv2.VideoCapture(
        0
    )  # Use index for the webcam (adjust the index accordingly if necessary)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)  # Set the width of the resolution
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)  # Set the height of the resolution
    cap.set(cv2.CAP_PROP_FPS, 60)  # Set the frame rate of the webcam
    PREVIEW_MAX_WIDTH = 960
    PREVIEW_MAX_HEIGHT = 540

    preview_label.configure(image=None)  # Reset the preview image before startup

    PREVIEW.deiconify()  # Open preview window

    frame_processors = get_frame_processors_modules(modules.globals.frame_processors)

    source_image = None  # Initialize variable for the selected face image

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Select and save face image only once
        if source_image is None and modules.globals.source_path:
            source_image = get_one_face(cv2.imread(modules.globals.source_path))

        temp_frame = frame.copy()  # Create a copy of the frame

        for frame_processor in frame_processors:
            temp_frame = frame_processor.process_frame(source_image, temp_frame)

        image = cv2.cvtColor(
            temp_frame, cv2.COLOR_BGR2RGB
        )  # Convert the image to RGB format to display it with Tkinter
        image = Image.fromarray(image)
        image = ImageOps.contain(
            image, (PREVIEW_MAX_WIDTH, PREVIEW_MAX_HEIGHT), Image.LANCZOS
        )
        image = ctk.CTkImage(image, size=image.size)
        preview_label.configure(image=image)
        ROOT.update()

    cap.release()
    PREVIEW.withdraw()  # Close preview window when loop is finished


def video_preview():
    if not modules.globals.source_path:
        # No source and target image selected
        update_status("Please select the source image to continue")
        return

    if not modules.globals.target_path:
        # No source and target image selected
        update_status("Please select the target video to continue")
        return

    global preview_label, PREVIEW, BREAK_STREAM

    cap = cv2.VideoCapture(modules.globals.target_path)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)  # Set the width of the resolution
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)  # Set the height of the resolution
    cap.set(cv2.CAP_PROP_FPS, 60)  # Set the frame rate of the webcam
    PREVIEW_MAX_WIDTH = 960
    PREVIEW_MAX_HEIGHT = 540
    SKIP_FRAME = 3
    BREAK_STREAM = False
    preview_label.configure(image=None)  # Reset the preview image before startup

    PREVIEW.deiconify()  # Open preview window

    frame_processors = get_frame_processors_modules(modules.globals.frame_processors)

    source_image = None  # Initialize variable for the selected face image
    count = 0
    time_a_frame = []
    while True:
        ret, frame = cap.read()
        if not ret or BREAK_STREAM:
            break

        # Select and save face image only once
        if source_image is None and modules.globals.source_path:
            source_image = get_one_face(cv2.imread(modules.globals.source_path))

        temp_frame = frame.copy()  # Create a copy of the frame

        start_t = time.time()
        if count % SKIP_FRAME == 0:
            count = 0
            # temp_frame = cv2.resize(temp_frame, (1280,720))
            temp_frame = cv2.resize(temp_frame, (PREVIEW_MAX_WIDTH, PREVIEW_MAX_HEIGHT))
            for frame_processor in frame_processors:
                temp_frame = frame_processor.process_frame(source_image, temp_frame)
            # Encode to preview window
            image = cv2.cvtColor(
                temp_frame, cv2.COLOR_BGR2RGB
            )  # Convert the image to RGB format to display it with Tkinter
            image = Image.fromarray(image)
            image = ImageOps.contain(
                image, (PREVIEW_MAX_WIDTH, PREVIEW_MAX_HEIGHT), Image.LANCZOS
            )
            image = ctk.CTkImage(image, size=image.size)
            preview_label.configure(image=image)
            ROOT.update()

        count += 1
        time_a_frame.append(time.time() - start_t)
        if len(time_a_frame) == 100:
            fps = len(time_a_frame) / sum(time_a_frame)
            print(f"FPS: {fps}")
            time_a_frame = []
    update_status("Xử lý video thành công!")
    cap.release()
    PREVIEW.withdraw()  # Close preview window when loop is finished
