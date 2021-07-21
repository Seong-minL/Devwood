import pygame
import os

# 버블 클래스 생성
class Bubble(pygame.sprite.Sprite):
    def __init__(self, image, color, position):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position)

# 발사대 클래스 생성
class Pointer(pygame.sprite.Sprite):
    def __init__(self, image, position, angle):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        self.angle = angle
        self.original_image = image
        self.position = position
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def rotate(self, angle):
        self.angle += angle
        if self.angle > 170:
            self.angle = 170
        elif self.angle < 10:
            self.angle = 10

        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.position)
        

# 맵 만들기
def setup():
    global map
    map = [
        list('RRYYBBGG'),
        list('RRYYBBG/'),  # / : 버블이 위치할 수 없다.
        list('BBGGRRYY'),
        list('BGGRRYY/'),
        list('........'),  # . : 비어있는 곳
        list('......./'),
        list('........'),
        list('......./'),
        list('........'),
        list('......./'),
        list('........')
    ]

    for row_idx, row in enumerate(map):
        for col_idx, col in enumerate(row):
            if col in './':
                continue
            position = get_bubble_position(row_idx, col_idx)
            image = get_bubble_image(col)
            bubble_group.add(Bubble(image, col, position))

def get_bubble_position(row_idx, col_idx):
    global cell_size
    pos_x = col_idx * cell_size + (bubble_width // 2)
    pos_y = row_idx * cell_size + (bubble_height // 2)
    if row_idx % 2 == 1:
        pos_x += cell_size // 2
    return pos_x, pos_y

def get_bubble_image(color):
    global bubble_images
    if color == 'R':
        return bubble_images[0]
    elif color == 'Y':
        return bubble_images[1]
    elif color == 'B':
        return bubble_images[2]
    elif color == 'G':
        return bubble_images[3]
    elif color == 'P':
        return bubble_images[4]
    else:
        return bubble_images[-1]

# 기본설정
pygame.init()
screen_width = 448
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Puzzle Bobble')
clock = pygame.time.Clock()

# 배경 만들기
current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, 'background.png'))

# 버블 만들기
bubble_images = [
    pygame.image.load(os.path.join(current_path, 'red.png')).convert_alpha(),
    pygame.image.load(os.path.join(current_path, 'yellow.png')).convert_alpha(),
    pygame.image.load(os.path.join(current_path, 'blue.png')).convert_alpha(),
    pygame.image.load(os.path.join(current_path, 'green.png')).convert_alpha(),
    pygame.image.load(os.path.join(current_path, 'purple.png')).convert_alpha(),
    pygame.image.load(os.path.join(current_path, 'black.png')).convert_alpha()
]

# 발사대 만들기
pointer_image = pygame.image.load(os.path.join(current_path, 'pointer.png'))
pointer = Pointer(pointer_image, (screen_width // 2, 624), 90)

# 게임 관련 변수
cell_size = 56
bubble_width = 56
bubble_height = 62
map = []  # 게임 맵
bubble_group = pygame.sprite.Group()
# to_angle = 0
to_angle_left = 0
to_angle_right = 0
angle_speed = 1.5

setup()

# 게임 실행
running = True
while running:
    clock.tick(60)  # FPS = 60

    # 이벤트 체크
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_angle_left += angle_speed
            elif event.key == pygame.K_RIGHT:
                to_angle_right -= angle_speed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_angle_left = 0
            elif event.key == pygame.K_RIGHT:
                to_angle_right = 0
    
    # 오브젝트 그리기
    screen.blit(background, (0, 0))  # 배경
    bubble_group.draw(screen)
    pointer.rotate(to_angle_left + to_angle_right)
    pointer.draw(screen)

    # 화면 업데이트
    pygame.display.update()

pygame.quit()