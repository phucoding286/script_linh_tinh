headers = {
  "authority": "free.netfly.top",
  "method": "POST",
  "path": "/api/openai/v1/chat/completions",
  "scheme": "https",
  "accept": "application/json, text/event-stream",
  "accept-encoding": "gzip, deflate, br, zstd",
  "accept-language": "en-US,en;q=0.9,vi;q=0.8",
  "content-length": "1814",
  "content-type": "application/json",
  "origin": "https://free.netfly.top",
  "priority": "u=1, i",
  "referer": "https://free.netfly.top/",
  "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
  "sec-ch-ua-mobile": "?1",
  "sec-ch-ua-platform": "\"Android\"",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "same-origin",
  "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36"
}

payloads = {
  "frequency_penalty": 0,
  "messages": [
    {
      "role": "system",
      "content": "Bạn là mô hình GPT3.5, Bạn đang nhận nhiệm vụ làm nhân viên hổ trợ tư vấn vấn đề tâm lý"
    },
    {
      "role": "user",
      "content": "test"
    }
  ],
  "model": "gpt-3.5-turbo",
  "presence_penalty": 1,
  "stream": True,
  "temperature": 0.8,
  "top_p": 0.9
}

api = "https://free.netfly.top/api/openai/v1/chat/completions"