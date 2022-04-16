from dataclasses import dataclass
import webbrowser


@dataclass
class Addition:
  """Classe generica apenas para indicar uma adição"""
  value: str
  def __init__(self, value):
    self.value = value


@dataclass
class Removal:
  """Classe generica apenas para indicar uma adição"""
  value: str
  def __init__(self, value):
    self.value = value


@dataclass
class Unchanged:
  """Classe generica apenas para indicar uma adição"""
  value: str
  def __init__(self, value):
    self.value = value

def createFile(content):
  with open('result.html', 'w') as file:
    file.write(content)
    file.close();

def openFileInBrowser():
  print("Se nada acontecer, mude o caminho do arquivo no método 'openFileInBrowser'");
  filename = '/Users/albino/Documents/unb/htmlDiff/result.html'
  webbrowser.open_new_tab(filename)

def get_lcs_len(text1, text2):
    n = len(text1)
    m = len(text2)

    lcs = [[None for _ in range(m+1)] for _ in range(n+1)]; # inicia uma matrix mxn vazia

    for i in range(0, n+1):
        for j in range(0, m+1):
            if i == 0 or j == 0:
                lcs[i][j] = 0
            elif text1[i-1] == text2[j-1]:
                lcs[i][j] = 1 + lcs[i-1][j-1]
            else:
                lcs[i][j] = max(lcs[i-1][j], lcs[i][j-1])

    return lcs

def find_lcs_string(text1, text2):
  result = ""
  lcs = get_lcs_len(text1, text2)

  results = []

  i = len(text1)
  j = len(text2)

  while i != 0 or j != 0:
    #Quando uma das strings acabam, adicione a outra como adição ou subtração
    if i == 0:
      results.append(Addition(text2[j - 1]))
      j -= 1
    elif j == 0:
      results.append(Removal(text1[i - 1]))
      i -= 1
    # Se for um caractere igual, então adicionamos como unchanged
    elif text1[i - 1] == text2[j - 1]:
      results.append(Unchanged(text1[i - 1]))
      i -= 1
      j -= 1
    # Se for um caractere diferente, adicionamos como adição ou remoção
    elif lcs[i - 1][j] <= lcs[i][j - 1]:
      results.append(Addition(text2[j - 1]))
      j -= 1
    else:
      results.append(Removal(text1[i - 1]))
      i -= 1

  #retorna reverso pois teramos de traz pra frente da string;
  return list(reversed(results))



def diffToHtml(diff):
  diffHtml = ""
  lastClass = ""
  for char in diff:
    if lastClass != type(char).__name__:
      if lastClass != "":
        diffHtml += "</div>"
      diffHtml += f"<div class=\"{type(char).__name__}\">{char.value}";    
      lastClass = type(char).__name__
    else:
      diffHtml += char.value
  if len(diffHtml) > 0:
    diffHtml += "</div>"
  css = "<style>.diff > div{border: solid #333;border-width: 1px 1px 0px 1px; line-heigth: 18px} .diff{border-bottom: 1px solid black;}.Addition{background: green}.Addition::before{content:' + '}.Removal{background: red}.Removal::before{content:' - ';font-size:18px}.Unchanged{background: #888}</style>"
  html = f"<html><head>{css}</head><body><div class=\"diff\">{diffHtml}</div></body></html>"
  return html

diff = find_lcs_string("asdfaaa", "afdsbaa")
htmlContent = diffToHtml(diff)
createFile(htmlContent)
openFileInBrowser()
