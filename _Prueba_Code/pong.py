import tkinter as tk

class PongGame:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, width=500, height=400, bg='black')
        self.canvas.pack()
        
        self.ball = self.canvas.create_oval(245, 195, 255, 205, fill='white')
        self.paddle_left = self.canvas.create_rectangle(20, 150, 40, 250, fill='white')
        self.paddle_right = self.canvas.create_rectangle(460, 150, 480, 250, fill='white')
        
        self.x_speed = 3
        self.y_speed = 3
        
        self.canvas.bind_all('<KeyPress-Up>', self.move_paddle_left_up)
        self.canvas.bind_all('<KeyPress-Down>', self.move_paddle_left_down)
        self.canvas.bind_all('<KeyPress-w>', self.move_paddle_right_up)
        self.canvas.bind_all('<KeyPress-s>', self.move_paddle_right_down)
        
        self.game_loop()
        
    def move_paddle_left_up(self, event):
        paddle_pos = self.canvas.coords(self.paddle_left)
        if paddle_pos[1] > 0:
            self.canvas.move(self.paddle_left, 0, -20)
        
    def move_paddle_left_down(self, event):
        paddle_pos = self.canvas.coords(self.paddle_left)
        if paddle_pos[3] < 400:
            self.canvas.move(self.paddle_left, 0, 20)
        
    def move_paddle_right_up(self, event):
        paddle_pos = self.canvas.coords(self.paddle_right)
        if paddle_pos[1] > 0:
            self.canvas.move(self.paddle_right, 0, -20)
        
    def move_paddle_right_down(self, event):
        paddle_pos = self.canvas.coords(self.paddle_right)
        if paddle_pos[3] < 400:
            self.canvas.move(self.paddle_right, 0, 20)
        
    def game_loop(self):
        self.canvas.move(self.ball, self.x_speed, self.y_speed)
        ball_pos = self.canvas.coords(self.ball)
        
        if ball_pos[1] <= 0 or ball_pos[3] >= 400:
            self.y_speed = -self.y_speed
            
        if ball_pos[0] <= 0 or ball_pos[2] >= 500:
            self.x_speed = -self.x_speed
            
        paddle_left_pos = self.canvas.coords(self.paddle_left)
        if ball_pos[0] <= paddle_left_pos[2] and ball_pos[1] >= paddle_left_pos[1] and ball_pos[3] <= paddle_left_pos[3]:
            self.x_speed = -self.x_speed
            
        paddle_right_pos = self.canvas.coords(self.paddle_right)
        if ball_pos[2] >= paddle_right_pos[0] and ball_pos[1] >= paddle_right_pos[1] and ball_pos[3] <= paddle_right_pos[3]:
            self.x_speed = -self.x_speed
            
        self.master.after(10, self.game_loop)
        
root = tk.Tk()
root.title("Pong Game")
game = PongGame(root)
root.mainloop()
