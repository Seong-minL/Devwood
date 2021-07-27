import pygame
import os, random, math, time

# 버블 클래스 생성
class Bubble(pygame.sprite.Sprite):
    def __init__(self, image, color, position=(0,0), row_idx=-1, col_idx=-1):
        super().__init__()
        self.image = image
        self.color = color
        self.rect = image.get_rect(center=position)
        self.radius = 16
        self.row_idx = row_idx
        self.col_idx = col_idx

    def set_rect(self, position):
        self.rect = self.image.get_rect(center=position)

    def draw(self, screen, to_x=None):
        if to_x:
            screen.blit(self.image, (self.rect.x + to_x, self.rect.y))
        else:
            screen.blit(self.image, self.rect)

    def set_angle(self, angle):
        self.angle = angle
        self.rad_angle = math.radians(self.angle)

    def move(self):
        to_x = self.radius * math.cos(self.rad_angle)
        to_y = self.radius * math.sin(self.rad_angle) * -1
        self.rect.x += to_x
        self.rect.y += to_y

        if (self.rect.left < 0) or (self.rect.right > screen_width):
            self.set_angle(180 - self.angle)
    
    def set_map_index(self, row_idx, col_idx):
        self.row_idx = row_idx
        self.col_idx = col_idx

    def drop_downward(self, height):
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery + height))

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
        list('PPYYBBGG'),  # . : 비어있는 곳
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
            bubble_group.add(Bubble(image, col, position, row_idx, col_idx))

def get_bubble_position(row_idx, col_idx):
    global cell_size
    pos_x = col_idx * cell_size + (bubble_width // 2)
    pos_y = row_idx * cell_size + (bubble_height // 2) + wall_height
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

def prepare_bubbles():
    global current_bubble, next_bubble
    if next_bubble:
        current_bubble = next_bubble
    else:
        current_bubble = create_bubble()  # 새 버블 만들기
    
    current_bubble.set_rect((screen_width // 2, 624))
    next_bubble = create_bubble()
    next_bubble.set_rect((screen_width // 4, 688))

def create_bubble():
    color = get_random_bubble_color()
    image = get_bubble_image(color)
    return Bubble(image, color)

def get_random_bubble_color():
    colors = []
    for row in map:
        for col in row:
            if (col not in colors) and (col not in './'):
                colors.append(col)
    return random.choice(colors)

def process_collision():
    global current_bubble, fire, current_fire_count
    hit_bubble = pygame.sprite.spritecollideany(current_bubble, bubble_group, pygame.sprite.collide_mask)
    if hit_bubble or current_bubble.rect.top <= wall_height:
        row_idx, col_idx = get_map_index(*current_bubble.rect.center)
        place_bubble(current_bubble, row_idx, col_idx)
        remove_adjacent_bubbles(row_idx, col_idx, current_bubble.color)
        current_bubble = None
        fire = False
        current_fire_count -= 1

def get_map_index(x, y):
    row_idx = (y - wall_height) // cell_size
    if row_idx % 2 == 1:
        col_idx = (x - (cell_size // 2)) // cell_size
        if col_idx < 0:
            col_idx = 0
        elif col_idx > map_column_count - 2:
            col_idx = map_column_count - 2
    else:
        col_idx = x // cell_size
    return row_idx, col_idx

def place_bubble(bubble, row_idx, col_idx):
    map[row_idx][col_idx] = bubble.color
    position = get_bubble_position(row_idx, col_idx)
    bubble.set_rect(position)
    bubble.set_map_index(row_idx, col_idx)
    bubble_group.add(bubble)

def remove_adjacent_bubbles(row_idx, col_idx, color):
    global visited
    visited.clear()
    visit(row_idx, col_idx, color)
    if len(visited) >= 3:
        remove_visited_bubbles()
        remove_hanging_bubbles()

def visit(row_idx, col_idx, color=None):
    global visited
    # 맵 범위 벗어나는지 확인
    if (row_idx < 0) or (row_idx >= map_row_count) or (col_idx < 0) or (col_idx >= map_column_count):
        return
    # 현재 셀의 색상이 color와 같은지
    if color and (map[row_idx][col_idx] != color):
        return
    # 빈공간이거나 버블이 존재할수 없는 곳인지 확인
    if map[row_idx][col_idx] in './':
        return
    if (row_idx, col_idx) in visited:
        return
    # 방문처리
    visited.append((row_idx, col_idx))
    
    if row_idx % 2 == 1:
        rows = [0, -1, -1, 0, 1, 1]
        cols = [-1, 0, 1, 1, 1, 0]
    else:
        rows = [0, -1, -1, -0, 1, 1]
        cols = [-1, -1, 0, 1, 0, -1]

    for i in range(len(rows)):
        visit(row_idx + rows[i], col_idx + cols[i], color)

def remove_visited_bubbles():
    global visited, bubble_group
    bubbles_to_remove = [b for b in bubble_group if (b.row_idx, b.col_idx) in visited]
    for bubble in bubbles_to_remove:
        map[bubble.row_idx][bubble.col_idx] = "."
        bubble_group.remove(bubble)

def remove_not_visited_bubbles():
    global visited, bubble_group
    bubbles_to_remove = [b for b in bubble_group if (b.row_idx, b.col_idx) not in visited]
    for bubble in bubbles_to_remove:
        map[bubble.row_idx][bubble.col_idx] = "."
        bubble_group.remove(bubble)

def remove_hanging_bubbles():
    global visited
    visited.clear()
    for col_idx in range(map_column_count):
        if map[0][col_idx] != '.':
            visit(0, col_idx)
    remove_not_visited_bubbles()

def draw_bubbles():
    global current_fire_count, bubble_group
    to_x = None
    if current_fire_count == 2:
        to_x = random.randint(0, 2) - 1  # -1 ~ 1
    elif current_fire_count == 1:
        to_x = random.randint(0, 8) - 4  # -4 ~ 4
    
    for bubble in bubble_group:
        bubble.draw(screen, to_x)

def drop_wall():
    global wall_height, bubble_group, current_fire_count, fire_count
    wall_height += cell_size
    for bubble in bubble_group:
        bubble.drop_downward(cell_size)
    current_fire_count = fire_count

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
wall = pygame.image.load(os.path.join(current_path, 'wall.png'))  # 벽 이미지

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
to_angle_left = 0
to_angle_right = 0
angle_speed = 1.5
map_row_count = 11
map_column_count = 8
visited = []  # 방문위치기록
fire_count = 7

current_bubble = None  # 이번에 쏠 버블
next_bubble = None  # 다음에 쏠 버블
fire = False  # 발사 여부
current_fire_count = fire_count
wall_height = 0  # 화면에 보여지는 벽의 높이

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
            elif event.key == pygame.K_SPACE:
                if current_bubble and (not fire):
                    fire = True
                    current_bubble.set_angle(pointer.angle)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_angle_left = 0
            elif event.key == pygame.K_RIGHT:
                to_angle_right = 0

    if not current_bubble:
        prepare_bubbles()

    if fire:
        process_collision()  # 충돌 처리

    if current_fire_count == 0:
        drop_wall()
    
    # 오브젝트 그리기
    screen.blit(background, (0, 0))  # 배경
    screen.blit(wall, (0, wall_height - screen_height))
    draw_bubbles()
    pointer.rotate(to_angle_left + to_angle_right)
    pointer.draw(screen)
    if current_bubble:
        if fire:
            current_bubble.move()
        current_bubble.draw(screen)
        
    if next_bubble:
        next_bubble.draw(screen)

    # 화면 업데이트
    pygame.display.update()

pygame.quit()