import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import conclusions 

def create_main_form():
    root = tk.Tk()
    root.title("Chẩn đoán tình trạng xe")
    root.geometry("700x400")

    # Đọc ảnh và thay đổi kích thước ảnh nền
    image = Image.open(r'C:\Users\Admin\Desktop\BTL\hechuyengia\he chuyen gia\HeChuyenGia\Background-home.png')
    resized_image = image.resize((700, 400), Image.LANCZOS)
    background_image = ImageTk.PhotoImage(resized_image)

    # Tạo canvas để đặt ảnh nền và vẽ chữ
    canvas = tk.Canvas(root, width=700, height=400)
    canvas.pack(fill="both", expand=True)

    canvas.create_image(0, 0, image=background_image, anchor="nw")
    canvas.create_text(50, 150, text="Chào mừng đến với hệ thống chẩn đoán xe", font=("Times New Roman", 15, "bold"), fill="black", anchor="w")

    # Nút bắt đầu
    get_started_button = tk.Button(root, text="Get Started", font=("Times New Roman", 15), 
                                command=lambda: open_diagnostic_form(root), 
                                bg="#FF4500", fg="black")
    canvas.create_window(50, 200, anchor='w', window=get_started_button)

    root.mainloop()

def open_diagnostic_form(root):
    root.destroy()
    form = tk.Tk()
    form.title("Chẩn đoán tình trạng xe")
    form.geometry("800x600")

    title_label = tk.Label(form, text="Hãy trả lời các câu hỏi dưới đây", font=("Times New Roman", 24))
    title_label.pack(pady=10)

    main_frame = tk.Frame(form)
    main_frame.pack(pady=20, fill="both", expand=True)

    question_frame = tk.Frame(main_frame)
    question_frame.pack(side="left", fill="both", expand=True)

    canvas = tk.Canvas(question_frame)
    scroll_y = tk.Scrollbar(question_frame, orient="vertical", command=canvas.yview)
    scroll_y.pack(side="right", fill="y")

    canvas.pack(side="left", fill="both", expand=True)
    canvas.configure(yscrollcommand=scroll_y.set)

    inner_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor='nw')

    questions = [
        ("Loại xe:", [("Xe du lịch cỡ nhỏ", "E1"), ("Xe sedan cỡ trung", "E2"), ("Xe SUV/Crossover", "E3"), 
                    ("Xe bán tải", "E4"), ("Xe tải nhỏ", "E5")]),
        ("Mức sử dụng xe:", [("Dưới 20.000 km", "D1"), ("Từ 20.000 đến 50.000 km", "D2"), 
                            ("Từ 50.000 đến 100.000 km", "D3"), ("Trên 100.000 km", "D4")]),
        ("Khu vực hỏng hóc:", [("Hệ thống động cơ", "B1"), ("Hệ thống phanh", "B2"), ("Hệ thống lái", "B3"), 
                                ("Hệ thống điện", "B4"), ("Hệ thống điều hòa", "B5"), ("Hệ thống nhiên liệu", "B6"), 
                                ("Hệ thống treo", "B7"), ("Hệ thống truyền động", "B8")]),
        ("Triệu chứng:", [("Xe không khởi động được", "C1"), ("Đèn báo lỗi bật sáng", "C2"), 
                        ("Tiếng động lạ phát ra từ động cơ", "C3"), ("Xe mất kiểm soát khi phanh", "C4"), 
                        ("Vô lăng rung lắc mạnh", "C5"), ("Xe tiêu tốn nhiên liệu bất thường", "C6"), 
                        ("Xe chạy không êm", "C7"), ("Điều hòa không hoạt động", "C8")]),
        ("Mức độ nghiêm trọng:", [("Hỏng hóc nhẹ", "A1"), ("Hỏng hóc trung bình", "A2"), 
                                ("Hỏng hóc nghiêm trọng", "A3"), ("Hỏng hóc rất nghiêm trọng", "A4"), 
                                ("Hỏng hóc toàn diện", "A5")])
    ]

    string_vars = []
    question_frames = []

    for question, options in questions:
        frame = tk.LabelFrame(inner_frame, text=question, font=("Times New Roman", 14), padx=10, pady=10)
        frame.pack(fill="both", expand=True, padx=20, pady=10)
        question_frames.append(frame)

        var = tk.StringVar(value="")
        string_vars.append(var)

        for option, code in options:
            rb = tk.Radiobutton(frame, text=f"{option} ({code})", variable=var, value=code, font=("Times New Roman", 12))
            rb.pack(anchor='w')

    inner_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    result_frame = tk.Frame(main_frame)
    result_frame.pack(side="right", fill="y", padx=10)

    result_text = tk.Text(result_frame, width=90, height=10, font=("Times New Roman", 12))
    result_text.pack(pady=10)

    def find_conclusion():
        for key, value in conclusions.conclusions.items():
            if (value["car_type"] in string_vars[0].get() and
                value["mileage"] in string_vars[1].get() and
                value["part"] in string_vars[2].get() and
                value["symptom"] in string_vars[3].get() and
                value["severity"] in string_vars[4].get()):
                return value["description"]
        return "Không có kết luận phù hợp."

    def get_conclusion():
        result_text.delete(1.0, tk.END)
        for i, frame in enumerate(question_frames):
            selected_option = string_vars[i].get()
            # Lấy phần mô tả (tức là phần văn bản, không phải mã)
            description = next((desc for desc, code in questions[i][1] if code == selected_option), "")
            result_text.insert(tk.END, f"{frame.cget('text')} {description} ({selected_option})\n")

        conclusion = find_conclusion()
        result_text.insert(tk.END, f"Kết luận: {conclusion}")


    consult_button = tk.Button(result_frame, text="Tư vấn", font=("Times New Roman", 16), 
                               command=get_conclusion, 
                               bg="#e67e22", fg="#ffffff")
    consult_button.pack(pady=20)

    form.mainloop()

create_main_form()
