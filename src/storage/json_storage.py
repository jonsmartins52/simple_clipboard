import json
import os

class JsonStorage:
  def __init__(self, filename="clipboard_history.json"):
    self.path = os.path.join(
      os.path.expanduser("~/.config/clipboard-manager"),
      filename
    )
    os.makedirs(os.path.dirname(self.path), exist_ok=True)

  def load(self):
    if not os.path.exists(self.path):
      return []
    
    try:
      with open(self.path, "r", encoding="utf-8") as f:
        return json.load(f)
    except:
      return []
    
  def save(self, data: list[str]):
    try:
      with open(self.path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
      print("Erro ao salvar histórico: ", e)