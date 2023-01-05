from process import ini_process, csv_process, end_process

ALMONTE = [37.3592723, -5.9833488, 17]
ARQUEROS = [37.3761966, -5.9982708, 20.58]
CAVABIANCA = [41.9747355, 12.4894753, 17.83]
VILLATEVERE = [41.9218339, 12.4838577, 21]
CREATOR = "Andrés M. Jiménez"


def poetry(title="POESÍA", file="import_poetry"):
    notebook = ini_process(title)
    csv_process('files/poetry_alm.csv', ALMONTE, CREATOR, notebook)
    csv_process('files/poetry_arq.csv', ARQUEROS, CREATOR, notebook)
    csv_process('files/poetry_cab.csv', CAVABIANCA, CREATOR, notebook)
    return end_process(file)


def spirituality(title="ESPIRITUAL", file="import_access"):
    notebook = ini_process(title)
    csv_process('files/almonte.csv', ALMONTE, CREATOR, notebook)
    csv_process('files/arqueros.csv', ARQUEROS, CREATOR, notebook)
    return end_process(file)


def literature(title="LITERATURA", file="import_kindle"):
    notebook = ini_process(title)
    csv_process('files/kindle_arq.csv', ALMONTE, CREATOR, notebook)
    csv_process('files/kindle_cb.csv', CAVABIANCA, CREATOR, notebook, delimiter=';')
    csv_process('files/kindle_vt.csv', VILLATEVERE, CREATOR, notebook, delimiter=';')
    return end_process(file)


if __name__ == '__main__':
    poetry()
    spirituality()
    literature()

