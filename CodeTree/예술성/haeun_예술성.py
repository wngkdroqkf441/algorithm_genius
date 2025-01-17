import sys
from collections import deque
from itertools import combinations

answer = 0

N = int(sys.stdin.readline().rstrip())
grid = list(list(map(int, sys.stdin.readline().split())) for _ in range(N))
drs = [-1, 1, 0, 0]
dcs = [0, 0, -1, 1]

cross_pos = set()
halfN = N // 2
for n in range(N):
    cross_pos.add((n, halfN))
    cross_pos.add((halfN, n))


class Group:
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos


def print_grid():
    print("+++++++++++++++++++++++++++++++++++++++++++")
    for line in grid:
        print(*line)
    print("+++++++++++++++++++++++++++++++++++++++++++")


def is_group(row, col, color, visited):
    if not (0 <= row < N and 0 <= col < N):
        return False
    if visited[row][col]:
        return False
    if color != grid[row][col]:
        return False
    return True


def grouping():
    # BFS로 그룹을 찾아냅니다.
    visited = [[0] * N for _ in range(N)]
    groups = []

    for r in range(N):
        for c in range(N):
            if not visited[r][c]:
                group_pos = [(r, c)]
                visited[r][c] = 1
                q = deque([(r, c)])
                color = grid[r][c]

                while q:
                    now_r, now_c = q.popleft()

                    for dr, dc in zip(drs, dcs):
                        new_r, new_c = now_r + dr, now_c + dc
                        if not is_group(new_r, new_c, color, visited):
                            continue
                        visited[new_r][new_c] = 1
                        group_pos.append((new_r, new_c))
                        q.append((new_r, new_c))

                # 각 그룹별 값과 위치 정보를 저장합니다.
                group = Group(color, group_pos)
                groups.append(group)
    return groups


def calculate(groups):
    groups_cnt = len(groups)
    balance_score = 0

    for a, b in combinations(range(groups_cnt), 2):
        group_a, group_b = groups[a], groups[b]
        connected_edges = 0

        # groupA와 groupB가 맞닿아있는 변의 수...
        # 한 자리씩 보면서 거리가 1이 차이나는지 봐야할듯
        for r_a, c_a in group_a.pos:
            for r_b, c_b in group_b.pos:
                if 1 == abs(r_a - r_b) + abs(c_a - c_b):
                    connected_edges += 1
        score = (len(group_a.pos) + len(group_b.pos)) \
                         * group_a.color * group_b.color * connected_edges
        if score:
            balance_score += score
    return balance_score


def clock(r_grid, s_r, s_c):
    size = halfN
    for r in range(s_r, s_r+size):
        for c in range(s_c, s_c+size):
            # O점으로 옮겨준다.
            # 그냥 원점으로 옮기면 되는거였다고?? 나는 이 고생을 했는데..?
            o_r, o_c = r - s_r, c - s_c
            # 회전하면 c, size - r - 1이 됨
            r_r, r_c = o_c, size - o_r -1
            # 다시 start 값을 더해줌
            r_grid[r_r+s_r][r_c+s_c] = grid[r][c]


def rotate():
    r_grid = [[0] * N for _ in range(N)]
    # 십자 모양 = 반시계방향
    for r, c in cross_pos:
        r_grid[N-1-c][r] = grid[r][c]
    # 그 외
    clock(r_grid, 0, 0)
    clock(r_grid, 0, halfN+1)
    clock(r_grid, halfN+1, 0)
    clock(r_grid, halfN+1, halfN+1)

    return r_grid


for turn in range(4):
    now_groups = grouping()
    answer += calculate(now_groups)
    if turn > 2:
        break
    grid = rotate()


print(answer)
