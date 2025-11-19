# -*- coding: utf-8 -*-
"""
자료구조 10가지 GUI 학습 도구 (Python + Tkinter, 탭 + 애니메이션)

기능 요약
- 상단에서 "10개의 정수"를 공백/콤마 구분으로 입력하여 공통 데이터로 사용
- 각 자료구조는 별도의 탭(Tab)
- 탭마다:
    - 수동 삽입/삭제/검색/초기화
    - "10개 값 애니메이션" 버튼: 입력된 10개 정수를 한 개씩 삽입하며 상태를 갱신
- 자료구조 목록 (10개)
  1) Array (배열/리스트)
  2) Stack
  3) Queue
  4) Deque
  5) Singly Linked List
  6) Binary Search Tree
  7) Min Heap
  8) Hash Table
  9) Set
 10) Graph (노드와 간선, 애니메이션 시 연속된 정수들끼리 간선 연결)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
import heapq


# ==========================
# 자료구조 클래스들
# ==========================

class BaseStructure:
    """공통 인터페이스: insert, delete, search, clear, get_state"""

    name = "Base"

    def insert(self, value):
        raise NotImplementedError

    def delete(self, value=None) -> str:
        raise NotImplementedError

    def search(self, value) -> bool:
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def get_state(self) -> str:
        raise NotImplementedError


class ArrayStructure(BaseStructure):
    name = "Array (배열/리스트)"

    def __init__(self):
        self.data: list[int] = []

    def insert(self, value: int):
        self.data.append(value)

    def delete(self, value: int | None = None) -> str:
        if not self.data:
            return "배열이 비어 있습니다."
        if value is None:
            removed = self.data.pop()
            return f"마지막 원소 {removed} 삭제"
        else:
            if value in self.data:
                self.data.remove(value)
                return f"값 {value} 삭제"
            else:
                return f"값 {value} 를 찾을 수 없습니다."

    def search(self, value: int) -> bool:
        return value in self.data

    def clear(self):
        self.data = []

    def get_state(self) -> str:
        return f"배열(Array) 내용:\n{self.data}"


class StackStructure(BaseStructure):
    name = "Stack (스택)"

    def __init__(self):
        self.stack: list[int] = []

    def insert(self, value: int):
        self.stack.append(value)  # push

    def delete(self, value=None) -> str:
        if not self.stack:
            return "스택이 비어 있습니다."
        removed = self.stack.pop()
        return f"pop: {removed} 제거"

    def search(self, value: int) -> bool:
        return value in self.stack

    def clear(self):
        self.stack = []

    def get_state(self) -> str:
        return f"스택(top 오른쪽):\n{self.stack}"


class QueueStructure(BaseStructure):
    name = "Queue (큐 - FIFO)"

    def __init__(self):
        self.q: deque[int] = deque()

    def insert(self, value: int):
        self.q.append(value)  # enqueue

    def delete(self, value=None) -> str:
        if not self.q:
            return "큐가 비어 있습니다."
        removed = self.q.popleft()
        return f"dequeue: {removed} 제거"

    def search(self, value: int) -> bool:
        return value in self.q

    def clear(self):
        self.q = deque()

    def get_state(self) -> str:
        return f"큐(front 왼쪽 → back 오른쪽):\n{list(self.q)}"


class DequeStructure(BaseStructure):
    name = "Deque (데크)"

    def __init__(self):
        self.d: deque[int] = deque()

    def insert(self, value: int):
        self.d.append(value)  # 오른쪽에 추가

    def delete(self, value: int | None = None) -> str:
        if not self.d:
            return "데크가 비어 있습니다."
        if value is None:
            removed = self.d.popleft()
            return f"왼쪽에서 {removed} 제거"
        else:
            try:
                self.d.remove(value)
                return f"값 {value} 제거"
            except ValueError:
                return f"값 {value} 를 찾을 수 없습니다."

    def search(self, value: int) -> bool:
        return value in self.d

    def clear(self):
        self.d = deque()

    def get_state(self) -> str:
        return f"데크(왼쪽 ↔ 오른쪽):\n{list(self.d)}"


class LinkedListNode:
    def __init__(self, value: int):
        self.value: int = value
        self.next: "LinkedListNode | None" = None


class LinkedListStructure(BaseStructure):
    name = "Singly Linked List (단일 연결 리스트)"

    def __init__(self):
        self.head: LinkedListNode | None = None

    def insert(self, value: int):
        new_node = LinkedListNode(value)
        if self.head is None:
            self.head = new_node
            return
        cur = self.head
        while cur.next is not None:
            cur = cur.next
        cur.next = new_node

    def delete(self, value: int | None = None) -> str:
        if self.head is None:
            return "리스트가 비어 있습니다."
        if value is None:
            removed = self.head.value
            self.head = self.head.next
            return f"head 노드 {removed} 제거"
        prev = None
        cur = self.head
        while cur is not None:
            if cur.value == value:
                if prev is None:
                    self.head = cur.next
                else:
                    prev.next = cur.next
                return f"값 {value} 노드 제거"
            prev = cur
            cur = cur.next
        return f"값 {value} 를 찾을 수 없습니다."

    def search(self, value: int) -> bool:
        cur = self.head
        while cur is not None:
            if cur.value == value:
                return True
            cur = cur.next
        return False

    def clear(self):
        self.head = None

    def get_state(self) -> str:
        values: list[int] = []
        cur = self.head
        while cur is not None:
            values.append(cur.value)
            cur = cur.next
        return "Linked List (head → tail):\n" + " -> ".join(map(str, values)) if values else "리스트가 비어 있습니다."


class BSTNode:
    def __init__(self, value: int):
        self.value: int = value
        self.left: "BSTNode | None" = None
        self.right: "BSTNode | None" = None


class BSTStructure(BaseStructure):
    name = "Binary Search Tree (이진 탐색 트리)"

    def __init__(self):
        self.root: BSTNode | None = None

    def _insert_node(self, node: BSTNode | None, value: int) -> BSTNode:
        if node is None:
            return BSTNode(value)
        if value < node.value:
            node.left = self._insert_node(node.left, value)
        elif value > node.value:
            node.right = self._insert_node(node.right, value)
        # 같은 값은 무시
        return node

    def insert(self, value: int):
        self.root = self._insert_node(self.root, value)

    def _find_min(self, node: BSTNode) -> BSTNode:
        while node.left is not None:
            node = node.left
        return node

    def _delete_node(self, node: BSTNode | None, value: int) -> tuple[BSTNode | None, bool]:
        if node is None:
            return None, False
        deleted = False
        if value < node.value:
            node.left, deleted = self._delete_node(node.left, value)
        elif value > node.value:
            node.right, deleted = self._delete_node(node.right, value)
        else:
            deleted = True
            if node.left is None:
                return node.right, True
            elif node.right is None:
                return node.left, True
            min_node = self._find_min(node.right)
            node.value = min_node.value
            node.right, _ = self._delete_node(node.right, min_node.value)
        return node, deleted

    def delete(self, value: int | None = None) -> str:
        if value is None:
            return "BST 삭제는 반드시 값이 필요합니다."
        self.root, deleted = self._delete_node(self.root, value)
        return f"값 {value} 삭제" if deleted else f"값 {value} 를 찾을 수 없습니다."

    def _search_node(self, node: BSTNode | None, value: int) -> bool:
        if node is None:
            return False
        if value == node.value:
            return True
        if value < node.value:
            return self._search_node(node.left, value)
        return self._search_node(node.right, value)

    def search(self, value: int) -> bool:
        return self._search_node(self.root, value)

    def clear(self):
        self.root = None

    def _inorder(self, node: BSTNode | None, res: list[int]):
        if node is None:
            return
        self._inorder(node.left, res)
        res.append(node.value)
        self._inorder(node.right, res)

    def get_state(self) -> str:
        if self.root is None:
            return "BST가 비어 있습니다."
        res: list[int] = []
        self._inorder(self.root, res)
        return "BST 중위순회(in-order):\n" + " , ".join(map(str, res))


class HeapStructure(BaseStructure):
    name = "Min Heap (최소 힙)"

    def __init__(self):
        self.heap: list[int] = []

    def insert(self, value: int):
        heapq.heappush(self.heap, value)

    def delete(self, value=None) -> str:
        if not self.heap:
            return "힙이 비어 있습니다."
        v = heapq.heappop(self.heap)
        return f"pop(min): {v} 제거"

    def search(self, value: int) -> bool:
        return value in self.heap

    def clear(self):
        self.heap = []

    def get_state(self) -> str:
        if not self.heap:
            return "힙이 비어 있습니다."
        return "Min Heap 내용(내부 배열 상태):\n" + str(self.heap)


class HashTableStructure(BaseStructure):
    name = "Hash Table (해시 테이블 - 체이닝)"

    def __init__(self, size: int = 10):
        self.size = size
        self.table: list[list[int]] = [[] for _ in range(size)]

    def _hash(self, value: int) -> int:
        return hash(value) % self.size

    def insert(self, value: int):
        idx = self._hash(value)
        if value not in self.table[idx]:
            self.table[idx].append(value)

    def delete(self, value: int | None = None) -> str:
        if value is None:
            return "해시 테이블 삭제는 반드시 값이 필요합니다."
        idx = self._hash(value)
        if value in self.table[idx]:
            self.table[idx].remove(value)
            return f"값 {value} 삭제 (bucket {idx})"
        else:
            return f"값 {value} 를 찾을 수 없습니다."

    def search(self, value: int) -> bool:
        idx = self._hash(value)
        return value in self.table[idx]

    def clear(self):
        self.table = [[] for _ in range(self.size)]

    def get_state(self) -> str:
        lines = ["Hash Table 상태:"]
        for i, bucket in enumerate(self.table):
            lines.append(f"Bucket {i}: {bucket}")
        return "\n".join(lines)


class SetStructure(BaseStructure):
    name = "Set (집합)"

    def __init__(self):
        self.s: set[int] = set()

    def insert(self, value: int):
        self.s.add(value)

    def delete(self, value: int | None = None) -> str:
        if value is None:
            return "집합 삭제는 반드시 값이 필요합니다."
        if value in self.s:
            self.s.remove(value)
            return f"값 {value} 제거"
        else:
            return f"값 {value} 를 찾을 수 없습니다."

    def search(self, value: int) -> bool:
        return value in self.s

    def clear(self):
        self.s = set()

    def get_state(self) -> str:
        return f"집합(Set) 내용:\n{sorted(self.s)}"


class GraphStructure(BaseStructure):
    """
    그래프는 문자열 노드로 관리 (정수는 str로 변환해서 사용)
    - 수동 입력: "1" = 노드 추가, "1-2" = 간선 추가(무방향)
    - 애니메이션: 입력된 정수 리스트의 각 값을 노드로 추가하고,
                 연속된 값들 사이에 간선 연결 (v[i-1] - v[i])
    """
    name = "Graph (그래프 - 인접 리스트)"

    def __init__(self):
        self.adj: dict[str, set[str]] = {}

    def insert(self, value: str):
        value = value.strip()
        if not value:
            raise ValueError("그래프 입력이 비어 있습니다.")
        if "-" in value:
            a, b = value.split("-", 1)
            a, b = a.strip(), b.strip()
            if not a or not b:
                raise ValueError("간선은 'A-B' 형태로 입력해야 합니다.")
            if a not in self.adj:
                self.adj[a] = set()
            if b not in self.adj:
                self.adj[b] = set()
            self.adj[a].add(b)
            self.adj[b].add(a)
        else:
            if value not in self.adj:
                self.adj[value] = set()

    # 애니메이션 전용: int 기반 노드/간선 추가
    def insert_node_edge_by_ints(self, prev_int: int | None, cur_int: int):
        cur = str(cur_int)
        if cur not in self.adj:
            self.adj[cur] = set()
        if prev_int is not None:
            prev = str(prev_int)
            if prev not in self.adj:
                self.adj[prev] = set()
            self.adj[prev].add(cur)
            self.adj[cur].add(prev)

    def delete(self, value: str | None = None) -> str:
        if value is None or value.strip() == "":
            return "그래프 삭제는 '노드' 또는 'A-B' 형태가 필요합니다."
        value = value.strip()
        if "-" in value:
            a, b = value.split("-", 1)
            a, b = a.strip(), b.strip()
            if a in self.adj:
                self.adj[a].discard(b)
            if b in self.adj:
                self.adj[b].discard(a)
            return f"간선 {a}-{b} 제거(존재했다면)"
        else:
            v = value
            if v in self.adj:
                for nbr in list(self.adj[v]):
                    self.adj[nbr].discard(v)
                del self.adj[v]
                return f"노드 {v} 및 연결 간선 제거"
            else:
                return f"노드 {v} 를 찾을 수 없습니다."

    def search(self, value: str) -> bool:
        value = value.strip()
        if "-" in value:
            a, b = value.split("-", 1)
            a, b = a.strip(), b.strip()
            return a in self.adj and b in self.adj[a]
        else:
            return value in self.adj

    def clear(self):
        self.adj = {}

    def get_state(self) -> str:
        if not self.adj:
            return "그래프가 비어 있습니다."
        lines = ["그래프 인접 리스트:"]
        for node in sorted(self.adj.keys(), key=lambda x: int(x) if x.isdigit() else x):
            neighbors = sorted(self.adj[node], key=lambda x: int(x) if x.isdigit() else x)
            lines.append(f"{node} -> {neighbors}")
        return "\n".join(lines)


# ==========================
# 탭 하나를 담당하는 클래스
# ==========================

class DataStructureTab:
    def __init__(self, parent, root, name: str, structure: BaseStructure,
                 get_input_list_callback, is_graph: bool = False):
        """
        parent: Notebook의 탭 Frame
        root  : Tk root (after() 호출용)
        name  : 탭 이름
        structure: 자료구조 인스턴스
        get_input_list_callback: 10개 int 리스트를 반환하는 함수
        is_graph: 그래프 탭인지 여부 (입력 처리 방식이 다름)
        """
        self.frame = parent
        self.root = root
        self.name = name
        self.ds = structure
        self.get_input_list = get_input_list_callback
        self.is_graph = is_graph

        # 애니메이션 상태
        self.anim_running = False
        self.anim_index = 0

        self._build_widgets()
        self.refresh_view("탭이 초기화되었습니다.")

    def _build_widgets(self):
        # 설명 라벨
        self.info_label = ttk.Label(self.frame, text=self._get_info_text(), foreground="gray")
        self.info_label.pack(anchor="w", pady=(5, 5))

        # 입력 + 버튼 영역
        input_frame = ttk.Frame(self.frame)
        input_frame.pack(fill="x", pady=(0, 5))

        ttk.Label(input_frame, text="값 입력:").grid(row=0, column=0, sticky="w")
        self.value_entry = ttk.Entry(input_frame, width=20)
        self.value_entry.grid(row=0, column=1, padx=5)

        self.insert_btn = ttk.Button(input_frame, text="삽입 / 추가", command=self.on_insert)
        self.insert_btn.grid(row=0, column=2, padx=3)

        self.delete_btn = ttk.Button(input_frame, text="삭제 / Pop", command=self.on_delete)
        self.delete_btn.grid(row=0, column=3, padx=3)

        self.search_btn = ttk.Button(input_frame, text="검색", command=self.on_search)
        self.search_btn.grid(row=0, column=4, padx=3)

        self.clear_btn = ttk.Button(input_frame, text="초기화 (Clear)", command=self.on_clear)
        self.clear_btn.grid(row=0, column=5, padx=3)

        # 애니메이션 버튼
        self.anim_btn = ttk.Button(
            input_frame,
            text="10개 값 애니메이션",
            command=self.start_animation
        )
        self.anim_btn.grid(row=0, column=6, padx=8)

        # 결과 메시지
        self.result_label = ttk.Label(self.frame, text="", foreground="blue")
        self.result_label.pack(anchor="w", pady=(0, 5))

        # 상태 표시 Text
        text_frame = ttk.Frame(self.frame)
        text_frame.pack(fill="both", expand=True)

        ttk.Label(text_frame, text="현재 자료구조 상태:").pack(anchor="w")

        self.text = tk.Text(text_frame, height=14, wrap="none")
        self.text.pack(fill="both", expand=True)

        y_scroll = ttk.Scrollbar(text_frame, orient="vertical", command=self.text.yview)
        y_scroll.pack(side="right", fill="y")
        self.text.configure(yscrollcommand=y_scroll.set)

    def _get_info_text(self) -> str:
        if isinstance(self.ds, StackStructure):
            return "스택: LIFO 구조. 값 없이 삭제 시 top을 pop."
        if isinstance(self.ds, QueueStructure):
            return "큐: FIFO 구조. 값 없이 삭제 시 front를 dequeue."
        if isinstance(self.ds, DequeStructure):
            return "데크: 값 없이 삭제 시 왼쪽 pop, 값 입력 시 해당 값 제거."
        if isinstance(self.ds, LinkedListStructure):
            return "단일 연결 리스트: 값 없이 삭제 시 head 제거."
        if isinstance(self.ds, BSTStructure):
            return "BST: 정렬된 이진 트리. 삭제/검색은 반드시 값 필요."
        if isinstance(self.ds, HeapStructure):
            return "최소 힙: 항상 가장 작은 값이 먼저 나온다."
        if isinstance(self.ds, HashTableStructure):
            return "해시 테이블: 체이닝 방식. 버킷에 값이 저장된다."
        if isinstance(self.ds, SetStructure):
            return "집합: 중복이 없다. 삭제/검색 시 값 필요."
        if isinstance(self.ds, GraphStructure):
            return "그래프: '1' = 노드 추가, '1-2' = 간선 추가 (무방향). 애니메이션 시 정수들 간 연속 간선 연결."
        return "배열/리스트: 끝에 삽입/삭제, 특정 값 삭제도 가능."

    def refresh_view(self, msg: str | None = None):
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, self.ds.get_state())
        if msg is not None:
            self.result_label.config(text=msg)
        else:
            self.result_label.config(text="")

    # -------- 수동 연산 --------

    def _parse_int_from_entry(self) -> int | None:
        """그래프가 아닐 때, 입력값을 int로 파싱"""
        raw = self.value_entry.get().strip()
        if raw == "":
            return None
        try:
            return int(raw)
        except ValueError:
            messagebox.showerror("입력 오류", "정수를 입력해주세요.")
            return None

    def on_insert(self):
        try:
            if self.is_graph:
                raw = self.value_entry.get().strip()
                if raw == "":
                    messagebox.showwarning("입력 필요", "노드 또는 '1-2' 형태의 값을 입력해주세요.")
                    return
                self.ds.insert(raw)
                self.refresh_view(f"[삽입] '{raw}' 추가/반영 완료.")
            else:
                val = self._parse_int_from_entry()
                if val is None:
                    return
                self.ds.insert(val)
                self.refresh_view(f"[삽입] {val} 추가 완료.")
        except Exception as e:
            messagebox.showerror("삽입 오류", str(e))

    def on_delete(self):
        try:
            if self.is_graph:
                raw = self.value_entry.get().strip()
                msg = self.ds.delete(raw if raw != "" else None)
                self.refresh_view(f"[삭제] {msg}")
            else:
                val = self._parse_int_from_entry()
                msg = self.ds.delete(val)
                self.refresh_view(f"[삭제] {msg}")
        except Exception as e:
            messagebox.showerror("삭제 오류", str(e))

    def on_search(self):
        try:
            if self.is_graph:
                raw = self.value_entry.get().strip()
                if raw == "":
                    messagebox.showwarning("입력 필요", "검색할 노드 또는 '1-2' 형태의 값을 입력해주세요.")
                    return
                found = self.ds.search(raw)
                msg = f"'{raw}' 를 찾았습니다. ✅" if found else f"'{raw}' 를 찾을 수 없습니다. ❌"
                self.refresh_view(f"[검색] {msg}")
            else:
                val = self._parse_int_from_entry()
                if val is None:
                    messagebox.showwarning("입력 필요", "검색할 정수를 입력해주세요.")
                    return
                found = self.ds.search(val)
                msg = f"{val} 을(를) 찾았습니다. ✅" if found else f"{val} 을(를) 찾을 수 없습니다. ❌"
                self.refresh_view(f"[검색] {msg}")
        except Exception as e:
            messagebox.showerror("검색 오류", str(e))

    def on_clear(self):
        self.ds.clear()
        self.refresh_view("[초기화] 자료구조를 비웠습니다.")

    # -------- 애니메이션 --------

    def start_animation(self):
        if self.anim_running:
            return  # 이미 실행 중이면 무시
        values = self.get_input_list()
        if not values:
            messagebox.showwarning("입력값 필요", "상단에 10개의 정수를 먼저 입력 후 '적용' 버튼을 눌러주세요.")
            return
        if len(values) != 10:
            # 꼭 10개일 필요는 없지만, 사용자가 헷갈리지 않게 경고만 주고 진행은 가능
            if not messagebox.askyesno(
                "개수 확인",
                f"현재 {len(values)}개의 값이 있습니다. 그대로 애니메이션을 진행할까요?"
            ):
                return

        # 구조 초기화 후 0번째부터 삽입 시작
        self.ds.clear()
        self.anim_index = 0
        self.anim_running = True
        self.result_label.config(text="애니메이션 시작: 값들을 하나씩 삽입합니다...")
        self._animate_step(values)

    def _animate_step(self, values: list[int]):
        if self.anim_index >= len(values):
            self.anim_running = False
            self.refresh_view("애니메이션 완료!")
            return

        cur_val = values[self.anim_index]

        # 그래프일 때는 연속된 값들 사이에 간선을 연결
        if isinstance(self.ds, GraphStructure):
            prev_val = values[self.anim_index - 1] if self.anim_index > 0 else None
            self.ds.insert_node_edge_by_ints(prev_val, cur_val)
            msg = f"[애니메이션] 노드 {cur_val}" + (f" 및 간선 {prev_val}-{cur_val} 추가" if prev_val is not None else " 추가")
        else:
            self.ds.insert(cur_val)
            msg = f"[애니메이션] {cur_val} 삽입"

        self.anim_index += 1
        self.refresh_view(msg)

        # 0.7초 간격으로 다음 값 삽입
        self.root.after(700, lambda: self._animate_step(values))


# ==========================
# 전체 GUI
# ==========================

class DataStructureGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("자료구조 10가지 학습 도구 (탭 + 10개 정수 애니메이션)")

        # 상단 공통 입력(10개의 정수)
        self.input_values: list[int] = []

        self._build_top_input()
        self._build_tabs()

    # -------- 상단: 10개 정수 입력 --------

    def _build_top_input(self):
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="10개 정수 입력 (공백/콤마 구분):").grid(row=0, column=0, sticky="w")
        self.global_entry = ttk.Entry(top, width=60)
        self.global_entry.grid(row=0, column=1, padx=5)

        self.apply_btn = ttk.Button(top, text="입력 값 적용", command=self.on_apply_values)
        self.apply_btn.grid(row=0, column=2, padx=5)

        self.global_info_label = ttk.Label(
            top,
            text="예: 5 1 9 3 7 2 8 6 4 0",
            foreground="gray"
        )
        self.global_info_label.grid(row=1, column=0, columnspan=3, sticky="w", pady=(5, 0))

    def _parse_int_list(self, text: str) -> list[int]:
        # 콤마를 공백으로 치환 후 split
        text = text.replace(",", " ")
        tokens = [t for t in text.split() if t]
        if not tokens:
            return []
        values: list[int] = []
        for t in tokens:
            values.append(int(t))
        return values

    def on_apply_values(self):
        raw = self.global_entry.get().strip()
        if not raw:
            messagebox.showwarning("입력 필요", "10개의 정수를 공백 또는 콤마로 구분하여 입력해주세요.")
            return
        try:
            values = self._parse_int_list(raw)
        except ValueError:
            messagebox.showerror("입력 오류", "모든 값이 정수인지 확인해주세요.")
            return

        if len(values) != 10:
            # 꼭 10개로 강제하지는 않지만, 안내 메시지
            if not messagebox.askyesno(
                "개수 확인",
                f"현재 {len(values)}개의 값이 있습니다. 그래도 이 값들을 사용할까요?"
            ):
                return

        self.input_values = values
        self.global_info_label.config(text=f"현재 입력된 값: {self.input_values}", foreground="blue")

    def get_input_list(self) -> list[int]:
        return self.input_values

    # -------- 탭 생성 --------

    def _build_tabs(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # 자료구조 인스턴스 준비
        structures: list[tuple[str, BaseStructure, bool]] = [
            ("Array (배열/리스트)", ArrayStructure(), False),
            ("Stack (스택)", StackStructure(), False),
            ("Queue (큐)", QueueStructure(), False),
            ("Deque (데크)", DequeStructure(), False),
            ("Linked List", LinkedListStructure(), False),
            ("BST", BSTStructure(), False),
            ("Min Heap", HeapStructure(), False),
            ("Hash Table", HashTableStructure(), False),
            ("Set", SetStructure(), False),
            ("Graph", GraphStructure(), True),  # is_graph=True
        ]

        self.tabs: list[DataStructureTab] = []

        for title, struct, is_graph in structures:
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=title)
            tab = DataStructureTab(
                parent=frame,
                root=self.root,
                name=title,
                structure=struct,
                get_input_list_callback=self.get_input_list,
                is_graph=is_graph
            )
            self.tabs.append(tab)


if __name__ == "__main__":
    root = tk.Tk()
    app = DataStructureGUI(root)
    root.mainloop()
