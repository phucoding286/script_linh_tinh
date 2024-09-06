from llm_module.llm import LLM
# from t5_llm import LLM
from llm_module.memories_system import WriteNewMemories, ReadAndActivateMem, ShortContextManager

llm = LLM("198067086eb0b1d85287db55979bc5531ea56dec", "k3NyFkaY9zso0TeSUXNKq4xAJJ2omkMpldUr7oUnfI0")
# llm = LLM()
writer_mem = WriteNewMemories(max_mem_context_towrite=4,
                              s="ký ức phản hồi người dùng: ",
                              t="ký ức phản hồi hệ thống: ")
reader_mem = ReadAndActivateMem(limit_mem_storage=15)
short_context = ShortContextManager(s="ngữ cảnh phản hồi trước đó của người dùng: ",
                                    t="ngữ cảnh phản hồi trước đó của hệ thống: ",
                                    max_limit_short_mem_contxt=15)

def send_message(txt_inp):
    reader_op = reader_mem.read_activate_memories(txt_inp)
    reader_op = "hiện tại hệ thống chưa có đủ ký ức để kích hoạt!" if reader_op is None else "\n".join(reader_op)
    reader_op = f"bộ nhớ đã được kích hoạt hiện tại:\n{reader_op}"

    short_context_op = short_context.short_context_reader()
    short_context_op = "ngữ cảnh ngắn hạn hiện tại đang trống!" if short_context_op is None else "\n".join(short_context_op)
    short_context_op = f"ngữ cảnh ngắn hạn của các phản hồi trước đó:\n{short_context_op}"

    pac_input = f"{reader_op}\n\n{short_context_op}\n\nđầu vào hiện tại: {txt_inp}"
    with open("log.txt", 'w', encoding="utf-8") as f:
        f.write(pac_input)
    return llm.predict(pac_input)

def predict(inp):
    output = send_message(inp)

    writer_mem.write_new_mem(inp, output)
    short_context.storage_short_context(inp, output)

    return output