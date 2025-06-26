import os
from datetime import datetime

# Caminhos das pastas de sessão
caminho_oe = r"C:\Users\wally\Desktop\Sessoes\OE"
caminho_tp = r"C:\Users\wally\Desktop\Sessoes\TP"
caminho_sdc = r"C:\Users\wally\Desktop\Sessoes\SDC"

# Caminhos das pastas de sessão do Drive
caminho_drive_oe = r"D:\Users\wally\Desktop\Sessoes\OE"
caminho_drive_tp = r"D:\Users\wally\Desktop\Sessoes\TP"
caminho_drive_sdc = r"D:\Users\wally\Desktop\Sessoes\SDC"

# identifica o ano atual e procura uma pasta que tenha o nome de sessao + ano atual
ano_atual = datetime.now().year

pasta_oe = os.path.join(caminho_oe,"Sessao {}".format(ano_atual))
pasta_tp = os.path.join(caminho_tp,"Sessao {}".format(ano_atual))
pasta_sdc = os.path.join(caminho_sdc,"Sessao {}".format(ano_atual))

print(pasta_oe)
