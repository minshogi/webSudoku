import json
import numpy as np
import random
import json

check = np.arange(1, 10)
ijs = []
for i in range(9):
    for j in range(9):
        ijs.append((i, j))


def filled_in_rule(array):
    if array.size != 9:
        return False
    for i in check:
        if i not in array:
            print(i)
            return False
    return True


def isAcceptMini(board, i):
    j = int(i / 3) * 3
    k = i % 3 * 3
    #print('j:{}, k:{}'.format(j, k))
    mini = board[j:j+3, k:k+3]
    # print(mini)
    if filled_in_rule(mini) == False:
        return False
    return True


def isAcceptRows(board):
    for i in range(9):
        row = board[i]
        if filled_in_rule(row) == False:
            return False
    return True


def isAcceptCols(board):
    return isAcceptRows(np.transpose(board))


def isPassed(board, ci=0, cj=0):
    # dealing list as np array. it is okay if already np array type.
    board = np.array(board)
    """if ci * cj != 0:
        # TODO
        pass"""
    for i in range(9):
        if isAcceptMini(board, i) == False:
            print('ㅎㅇ', i)
            return False
    return isAcceptRows(board) and isAcceptCols(board)


def gen_initial_sudoku():
    board = np.zeros([9, 9], dtype=int)
    for i in range(9):
        board[i] = np.arange(1, 10)
    for i in range(1, 9):
        board[i] = np.concatenate((board[i-1][3:], board[i-1][:3]), axis=None)
        if i % 3 == 0:
            board[i] = np.concatenate(
                (board[i-1][1:], board[i-1][:1]), axis=None)

    return board


def rotate(board, angle, size=9):
    angle = np.radians(angle)
    M = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle), np.cos(angle)]])
    new_board = np.zeros([size, size], dtype=int)
    for i in range(size):
        for j in range(size):
            value = board[i][j]
            tv = np.array([[i - int(size/2), j - int(size/2)]])
            k = M @ tv.transpose()
            k = k.reshape(2)
            print(k)
            k = np.array([int(k[0]), int(k[1])])

            new_board[k[0] + int(size/2)][k[1] + int(size/2)] = value

    return new_board


def get_shuffled_sudoku(board):
    samples = random.sample(range(1, 10), 8)
    for i in range(4):
        first, second = samples[i*2], samples[i*2+1]
        #print('first : ', first)
        #print('second : ', second)
        flist = np.where(board == first)
        slist = np.where(board == second)
        fi_idx_list = flist[0]
        fj_idx_list = flist[1]
        si_idx_list = slist[0]
        sj_idx_list = slist[1]
        fi_idx_list, si_idx_list = si_idx_list, fi_idx_list
        fj_idx_list, sj_idx_list = sj_idx_list, fj_idx_list
        #print('fi_idx_list', fi_idx_list)
        #print('fj_idx_list', fj_idx_list)
        for k in range(fi_idx_list.size):
            fi = fi_idx_list[k]
            fj = fj_idx_list[k]
            si = si_idx_list[k]
            sj = sj_idx_list[k]
            board[fi][fj] = first
            board[si][sj] = second

    n = random.randint(0, 3) * 90
    #print('n:', n)
    # board = rotate(board, n)   TODO
    return board


def convert_sparse_matrix(board, num):
    num %= 81  # scaling
    slist = random.sample(ijs, num)  # list of tuples
    ret = board
    for idx in slist:
        ret[idx[0]][idx[1]] = 0
    return ret


"""
1. table 쓰기 (표) 9행 9열짜리 표, 입력받는 칸은 두고 입력 못받는 칸은 우리가 정해진 숫자 넣고
ㄴ 9x9형태로 커뮤니케이션 일어날 수 있는 오브젝트 아무거나
2. 유저가 모두 입력받고 제출 누르면 스도쿠 조건 만족하는지 체크
ㄴ 만족하면 Clear
ㄴ 만족하지면 못하면? 다시 하라고 해야지
ㄴㄴ 어디 때문에 만족이 안 되는지 : backend에서 체크하면서 false 반환 되는 부분 '모두' 인덱싱
ㄴㄴ 인덱싱을 토대로 해당 table(표) 셀에 색칠(붉은색)
3. 색상 초기화(붉은색 표기 후 유저 입력하는 도중에 언제 원래 색으로 표현할지) // 이번주 목(4.8) 여기까진 되게끔.
4. 힌트(확률?)
ㄴ 이에 의하면 2번은 수정될 수 있다.
ㄴ 유저 입력 도중에(빈칸 있음), 한 2~3칸 정도만 힌트 줌(각 칸 당 들어올 수 있는 것들 중 한 개씩 숫자만)
ㄴ 확률 모델은 톡방에서 어떻게 하라고 하는지 힌트 얻기(목)
"""


def lambda_handler(event, context):
    # TODO implement
    body = {}
    board = gen_initial_sudoku()
    board = get_shuffled_sudoku(board)
    body['board'] = board.tolist()
    nanido = int(event["Level"])
    num = nanido * 20 + 5
    usr_board = convert_sparse_matrix(board, num)
    body['usr_board'] = usr_board.tolist()
    ret = {
        'statusCode': 200,
        'body': json.dumps(body)
    }
    return ret


print(lambda_handler(event={"Level": '1'}, context=""))
