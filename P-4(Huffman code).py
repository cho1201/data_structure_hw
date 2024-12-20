# heappush 함수
def heappush(heap, n):
    heap.append(n)            # 맨 마지막 노드로 일단 삽입
    i = len(heap) - 1         # 노드 n의 위치
    while i != 1:             # n이 루트가 아니면 
        pi = i // 2           # 부모 노드의 위치
        if heap[pi] <= n:     # 부모보다 크면 up-heap 종료
            break
        heap[i] = heap[pi]    # 부모를 끌어내림
        i = pi                # i가 부모의 인덱스가 됨
    heap[i] = n               # 마지막 위치에 n 삽입

# heappop 함수
def heappop(heap):
    size = len(heap) - 1      # 노드의 개수
    if size == 0:             # 공백상태
        return None

    root = heap[1]            # 삭제할 루트 노드(사장)
    last = heap[size]         # 마지막 노드(말단사원)

    pi = 1                    # 부모 노드의 인덱스
    i = 2                     # 자식 노드의 인덱스

    while i <= size:          # 마지막 노드 이전까지
        if i < size and heap[i] > heap[i+1]:  # left가 더 크면 i를 1 증가
            i += 1            # 비교할 자식은 오른쪽 자식
        if last <= heap[i]:   # 자식이 더 크면 down-heap 종료 
            break
        heap[pi] = heap[i]    # 아니면 down-heap 계속
        pi = i                
        i *= 2
        
    heap[pi] = last           # 맨 마지막 노드를 parent 위치에 복사
    heap.pop()                # 맨 마지막 노드 삭제
    return root               # 저장해두었던 루트를 반환


# Node 클래스 정의
class Node:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right

    # 노드 비교를 위한 비교 연산자 구현
    def __lt__(self, other):
        return self.freq < other.freq
    
    def __eq__(self, other):
        return self.freq == other.freq
    
    def __le__(self, other):
        return self.freq <= other.freq

# 허프만 코딩 트리 생성
def huffman_tree(frequencies):
    heap = [None]  # 인덱스 1부터 시작하기 위해 None 추가
    for char, freq in frequencies.items():
        heappush(heap, Node(freq, char))
    
    while len(heap) > 2:  # 루트 노드만 남을 때까지
        left = heappop(heap)
        right = heappop(heap)
        merged = Node(left.freq + right.freq, left=left, right=right)
        heappush(heap, merged)
    
    return heappop(heap)  # 최종 루트 노드 반환

# 허프만 코드 생성
def huffman_codes(root):
    codes = {}
    
    def generate_codes(node, code=""):
        if node is not None:
            if node.char is not None:
                codes[node.char] = code
            generate_codes(node.left, code + "0")
            generate_codes(node.right, code + "1")
    
    generate_codes(root)
    return codes

# 입력 메시지 및 유효성 검사
def get_valid_input(codes):
    while True:
        text = input("Please a word: ").strip()
        if all(char in codes for char in text):
            return text
        else:
            print("Illegal character")

# 압축률 계산
def calculate_compression(text, codes):
    original_bits = len(text) * 8
    encoded_bits = sum(len(codes[char]) for char in text)
    compression_rate = (1 - (encoded_bits / original_bits)) * 100
    return encoded_bits, compression_rate

# 메인 프로그램
def main():
    frequencies = {'k': 10, 'o': 5, 'r': 2, 'e': 15, 'a': 18, 't': 4, 'c': 7, 'h': 11}
    
    # 허프만 트리 생성 및 코드 생성
    root = huffman_tree(frequencies)
    codes = huffman_codes(root)
    
    # 허프만 코드 출력
    print("Huffman Codes:", codes)
    
    # 유효한 입력 받기
    text = get_valid_input(codes)
    
    # 허프만 인코딩 결과 출력
    encoded_text = ''.join(codes[char] for char in text)
    print("결과 비트열:", encoded_text)
    
    # 압축률 계산 및 출력
    encoded_bits, compression_rate = calculate_compression(text, codes)
    print(f"압축률: {compression_rate:.2f}%")
    print(f"원본 비트: {len(text) * 8}, 인코드된 비트: {encoded_bits}")

# 프로그램 실행
main()
