import os
import random
from difflib import SequenceMatcher


# kiểm tra thư mục bộ nhớ nếu không có sẽ tiến hành tạo
MEMORIES_DIR = "./memories"
TEMP_MEM_BACKUP_DIR = "./temp_memories_backup"

if not os.path.exists(MEMORIES_DIR):
    os.mkdir(MEMORIES_DIR)

if not os.path.exists(TEMP_MEM_BACKUP_DIR):
    os.mkdir(TEMP_MEM_BACKUP_DIR)





class SomeMethod:

    def __init__(self) -> None:
        pass

    # kiểm tra độ tương đồng
    def similiary(self, s, t):
        return SequenceMatcher(None, s, t).ratio()
    
    # xóa dấu câu
    def remove_punctuation(self, text):
        punct = """<>?"'}{|+_)(*&^%$#@!)/.,;'][\\=-`~]:"""
        for c in list(punct):
            text = text.replace(c, "")
        return text





class ReadAndActivateMem:

    def __init__(self, limit_mem_storage=4):
        # tạo danh sách tên file đã bỏ đi .txt
        self.limit_mem_storage = limit_mem_storage
    
    def read_activate_memories(self, inp): # đọc và kích hoạt bộ nhớ dự trên câu văn bản
        list_mem_name = [mem_n.replace(".txt", "") for mem_n in os.listdir(MEMORIES_DIR)]
        # tạo một set chứa các tên file bộ nhớ và mức độ tương đồng với text inp dưới dạng key value
        # mục đích là kích hoạt bộ nhớ dựa trên mức độ liên quan
        memories_act_scores = {mem:SomeMethod().similiary(inp, mem) for mem in list_mem_name}

        most_mem_n = 0
        most_mem = ""
        
        # lặp qua set và index value score để lấy giá trị lớn nhất (file ký ức liên quan nhất)
        for m in list_mem_name:
            if memories_act_scores[m] > most_mem_n:
                most_mem_n = memories_act_scores[m]
                most_mem = m
        
        # đọc tệp ký ức đã tìm thấy, nếu có lỗi sẽ trả về False
        try:

            with open(f"{MEMORIES_DIR}/{most_mem}.txt", "r", encoding="utf-8") as f:
                most_memories = f.read().splitlines()
            
            # giới hạn bộ nhớ ký ức, và lấy phần ký ức ngẫu nhiên
            if len(most_memories) > self.limit_mem_storage * 2:
                sc = random.choice([n for n in range(len(most_memories))]) - self.limit_mem_storage * 2
                most_memories = most_memories[sc : sc+self.limit_mem_storage]

            return None if str(most_memories) == "[]" else most_memories
    
        except:
            print(f"đã có lỗi khi đọc file {MEMORIES_DIR}/{most_mem}.txt")
            return None





class WriteNewMemories:
    
    def __init__(self, max_mem_context_towrite=4, s="s object: ", t="t object: "):
        # tạo danh sách tên file đã bỏ đi .txt
        self.max_mem_context_towrite = max_mem_context_towrite
        self.s = s
        self.t = t
        self.CONTEXT = []
        self.read_context_backup()
    
    def read_context_backup(self):
        if os.path.exists(f"{TEMP_MEM_BACKUP_DIR}/backup_contxt_writer.txt"):
            with open(f"{TEMP_MEM_BACKUP_DIR}/backup_contxt_writer.txt", "r", encoding="utf-8") as file:
                context_backup = file.read().splitlines()
            self.CONTEXT = context_backup

    def backup_contxt_writer(self):
        # backup lại ngữ cảnh đang duy trùy ở hiện tại, để phòng tránh trường hợp tắt bất ngờ và mất
        # thông tin đang duy trì
        with open(f"{TEMP_MEM_BACKUP_DIR}/backup_contxt_writer.txt", "w", encoding="utf-8") as file:
            context_text = "\n".join(self.CONTEXT)
            file.write(context_text)

    def w(self, inp, ans, filename: str): # ghi bộ nhớ mới vào folder memories
        inp, ans = " ".join(inp.split()), " ".join(ans.split())
        list_mem_name = [mem_n.replace(".txt", "") for mem_n in os.listdir(MEMORIES_DIR)]
        # tạo một set chứa các tên file bộ nhớ và mức độ tương đồng với text inp dưới dạng key value
        # mục đích là kích hoạt bộ nhớ dựa trên mức độ liên quan
        memories_act_scores = {mem:SomeMethod().similiary(" ".join(inp.split()[:10]), mem) for mem in list_mem_name}
        
        most_mem_n = 0
        most_mem = ""
        
        # lặp qua set và index value score để lấy giá trị lớn nhất (file ký ức liên quan nhất)
        for m in list_mem_name:
            if memories_act_scores[m] > most_mem_n:
                most_mem_n = memories_act_scores[m]
                most_mem = m
        
        """
        lưu đầu vào và đầu ra vào file đã tồn tại nếu file đã tồn tại có độ tương đồng cao 0.5 (50%)
        so với input
        """
        if most_mem_n > 0.5:
            with open(f"{MEMORIES_DIR}/{most_mem}.txt", "a", encoding="utf-8") as f:
                f.write(f"{inp}\n{ans}\n")
        
        # nếu độ tương đồng không cao hơn 50% sẽ tajo file ký ức mới và lưu các ký ức mới vào
        else:
            with open(f"{MEMORIES_DIR}/{filename}.txt", "a", encoding="utf-8") as f:
                f.write(f"{inp}\n{ans}\n")

    def write_new_mem(self, inp, ans):
        """
        hàm đặc biệt này sẽ giới hạn số lượng ngữ cảnh tối đa trước khi ghi, để ký ức không chỉ là
        những gì đã diễn ra trong một lần, mà nó còn bao gồm ngữ cảnh
        """
        inp, ans = " ".join(inp.split()), " ".join(ans.split())
        # thêm input và ans vào ngữ cảnh sau mỗi bước thời gian
        self.CONTEXT.append(self.s+inp)
        self.CONTEXT.append(self.t+ans)
        
        # tiến hành lưu nếu số lượng ngữ cảnh đạt chỉ tiêu
        if len(self.CONTEXT) > self.max_mem_context_towrite:
            # lấy vị trí index đầu tiên trong ngữ cảnh làm tên file ký ức
            # xử lý trước tên file
            filename = self.CONTEXT[0].replace(self.s, "").replace(self.t, "")
            filename = " ".join(SomeMethod().remove_punctuation(filename).split()[:10])
            filename = filename.strip()

            # lưu vào bộ nhớ, bao gồm cả ngữ cảnh
            n=0
            for _ in range(self.max_mem_context_towrite-1):
                self.w(self.CONTEXT[n], self.CONTEXT[n+1], filename)
                n = (n+1)+1

            # cập nhật cắt bớt ngữ cảnh lại
            self.CONTEXT = self.CONTEXT[ len(self.CONTEXT)-self.max_mem_context_towrite: ]
    
        self.backup_contxt_writer()




class ShortContextManager:
    
    def __init__(self, s, t, max_limit_short_mem_contxt=4):
        self.max_limit_short_mem_contxt = max_limit_short_mem_contxt
        self.s = s
        self.t = t
        self.context = []
        self.read_backup()

    def read_backup(self):
        # gán lại ngữ cảnh ngắn hạn đã sao lưu nếu có
        if os.path.exists(f"{TEMP_MEM_BACKUP_DIR}/short_context_backup.txt"):
            with open(f"{TEMP_MEM_BACKUP_DIR}/short_context_backup.txt", "r", encoding="utf-8") as f:
                short_context = f.read().strip().splitlines()
            self.context = short_context

    def backup_short_context_writer(self):
        # sao lưu ngữ cảnh ngắn hạn
        with open(f"{TEMP_MEM_BACKUP_DIR}/short_context_backup.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(self.context))

    def storage_short_context(self, inp, ans):
        # chuẩn hóa inp và ans
        inp, ans = " ".join(inp.split()), " ".join(ans.split())
        
        # thêm inp và ans của bước thời gian hiện tại vào ngữ cảnh
        self.context.append(self.s+inp)
        self.context.append(self.t+ans)

        if len(self.context) > self.max_limit_short_mem_contxt:
            self.context = self.context[ len(self.context)-self.max_limit_short_mem_contxt: ]
        
        # liên tục sao lưu ngữ cảnh
        self.backup_short_context_writer()
    
    def short_context_reader(self):
        return None if str(self.context) == "[]" else self.context