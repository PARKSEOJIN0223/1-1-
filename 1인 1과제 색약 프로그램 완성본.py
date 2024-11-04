import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import requests
from io import BytesIO
import random

# Unsplash API 설정
UNSPLASH_ACCESS_KEY = "GVK2EZ2q4RcpeXMXcCi0si-hS7GQhPCSQnSOc4rwnJ8"

class ColorQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("색상 및 색상 퀴즈")
        self.color_name = ""

        # 안내 라벨
        self.instruction = tk.Label(root, text="버튼을 클릭하여 색상을 선택하거나 퀴즈를 시작하세요!")
        self.instruction.pack(pady=10)

        # 색상 선택 버튼
        self.pick_color_btn = tk.Button(root, text="색상 선택", command=self.pick_color)
        self.pick_color_btn.pack(pady=10)

        # 퀴즈 버튼
        self.quiz_btn = tk.Button(root, text="퀴즈 시작", command=self.start_quiz)
        self.quiz_btn.pack(pady=10)

        # 결과 라벨
        self.result_label = tk.Label(root, text="")
        self.result_label.pack(pady=10)

        # 이미지 라벨
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

    def pick_color(self):
        """색상 선택 대화창 대신 기본 색상 중 하나만 선택하게 함 (색 이름 없이 색상만 표시)"""
        colors = {
            "빨간색": "#FF0000",
            "주황색": "#FFA500",
            "노란색": "#FFFF00",
            "초록색": "#008000",
            "파란색": "#0000FF",
            "남색": "#000080",
            "보라색": "#800080"
        }

        # 색상 선택 메뉴 생성
        color_menu = tk.Toplevel(self.root)
        color_menu.title("색상 선택")
       
        for color_name, hex_code in colors.items():
            btn = tk.Button(color_menu, bg=hex_code, command=lambda c=color_name: self.show_color_name(c))
            btn.pack(fill=tk.BOTH, expand=True)

    def show_color_name(self, color_name):
        """선택한 색상 이름을 보여주는 함수"""
        self.result_label.config(text=f"선택한 색상: {color_name}")
       
    def download_image_from_unsplash(self, query, hex_code):
        """Unsplash API를 사용하여 이미지를 검색 및 다운로드하는 함수 (한 가지 색상만 포함된 이미지)"""
        url = f"https://api.unsplash.com/photos/random?query={query}&color={hex_code.lstrip('#')}&client_id={UNSPLASH_ACCESS_KEY}"
        response = requests.get(url)

        # 응답 상태 코드 확인
        if response.status_code != 200:
            messagebox.showerror("오류", "Unsplash API 요청에 실패했습니다.")
            return None

        data = response.json()

        # 이미지 URL 확인
        if 'urls' not in data or 'regular' not in data['urls']:
            messagebox.showerror("오류", "이미지를 가져오는 데 실패했습니다.")
            return None

        image_url = data['urls']['regular']
        image_response = requests.get(image_url)

        img_data = BytesIO(image_response.content)
        img = Image.open(img_data)
        return img

    def start_quiz(self):
        """퀴즈 시작 함수 - 정답 색상과 오답 색상 이미지를 혼합한 퀴즈"""
        colors = {
            "빨간색": ("red", "#FF0000"),
            "주황색": ("orange", "#FFA500"),
            "노란색": ("yellow", "#FFFF00"),
            "초록색": ("green", "#008000"),
            "파란색": ("blue", "#0000FF"),
            "남색": ("navy", "#000080"),
            "보라색": ("purple", "#800080")
        }

        # 정답 색상과 랜덤 오답 색상 선택
        correct_color_name, (correct_color_query, correct_color_hex) = random.choice(list(colors.items()))
        wrong_color_name, (wrong_color_query, wrong_color_hex) = random.choice(list(colors.items()))

        while wrong_color_name == correct_color_name:  # 정답과 오답이 같으면 다른 오답 선택
            wrong_color_name, (wrong_color_query, wrong_color_hex) = random.choice(list(colors.items()))

        # 정답 이미지 대신 오답 이미지를 다운받을 확률을 50%로 설정
        show_wrong_image = random.choice([True, False])

        if show_wrong_image:
            img = self.download_image_from_unsplash(wrong_color_query, wrong_color_hex)
            displayed_color_name = wrong_color_name
        else:
            img = self.download_image_from_unsplash(correct_color_query, correct_color_hex)
            displayed_color_name = correct_color_name

        if img:
            img = img.resize((300, 200))  # 이미지 크기 조정
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk  # 이미지 유지

            # 주요 색상이 무엇인지 질문 (오답 이미지를 보여주는 경우도 포함)
            question = f"이 그림의 주요 색상이 {correct_color_name}인가요?"

            answer = messagebox.askquestion("퀴즈", question)

            # 정답 체크: displayed_color_name이 정답이면 yes가 정답, 아니면 no가 정답
            if (answer == 'yes' and displayed_color_name == correct_color_name) or (answer == 'no' and displayed_color_name != correct_color_name):
                messagebox.showinfo("결과", "정답입니다!")
            else:
                messagebox.showinfo("결과", f"틀렸습니다!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorQuizApp(root)
    root.mainloop()
